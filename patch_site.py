from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Supabase public connection settings.
text = text.replace(
"""      proxyBase: '',\n      adminCodeHash: '0f65f55c87c47704194741c1dd4aa83401188ffea90cd881e0733059481dcdba'\n""",
"""      proxyBase: '',\n      supabaseUrl: 'https://ezpfongqfmaczftwleog.supabase.co',\n      supabasePublishableKey: 'sb_publishable_t25xim64x_XQJxwleaA57w_WGINOMrW',\n      adminCodeHash: '0f65f55c87c47704194741c1dd4aa83401188ffea90cd881e0733059481dcdba'\n""",
1,
)

text = text.replace(
"""      loadSeq: 0,\n      isAdmin: false\n    };\n\n    const STORAGE_KEY = 'soop-rank-manual-gender-v1';\n    const ADMIN_SESSION_KEY = 'soop-rank-admin-session-v1';\n""",
"""      loadSeq: 0,\n      isAdmin: false,\n      adminCode: ''\n    };\n\n    const STORAGE_KEY = 'soop-rank-manual-gender-v1';\n    const ADMIN_SESSION_KEY = 'soop-rank-admin-session-v1';\n    const ADMIN_CODE_SESSION_KEY = 'soop-rank-admin-code-session-v1';\n""",
1,
)

admin_anchor = """    function saveAdminSession(enabled) {\n      try {\n        if (enabled) sessionStorage.setItem(ADMIN_SESSION_KEY, '1');\n        else sessionStorage.removeItem(ADMIN_SESSION_KEY);\n      } catch {}\n    }\n\n"""
admin_extra = admin_anchor + """    function loadAdminCodeSession() {\n      try { return sessionStorage.getItem(ADMIN_CODE_SESSION_KEY) || ''; }\n      catch { return ''; }\n    }\n\n    function saveAdminCodeSession(code) {\n      try {\n        if (code) sessionStorage.setItem(ADMIN_CODE_SESSION_KEY, code);\n        else sessionStorage.removeItem(ADMIN_CODE_SESSION_KEY);\n      } catch {}\n    }\n\n"""
text = text.replace(admin_anchor, admin_extra, 1)

text = text.replace(
"""    function setAdminMode(enabled) {\n      state.isAdmin = Boolean(enabled);\n      saveAdminSession(state.isAdmin);\n      updateAdminUi();\n      render();\n    }\n""",
"""    function setAdminMode(enabled) {\n      state.isAdmin = Boolean(enabled);\n      saveAdminSession(state.isAdmin);\n      if (!state.isAdmin) {\n        state.adminCode = '';\n        saveAdminCodeSession('');\n      }\n      updateAdminUi();\n      render();\n    }\n""",
1,
)

text = text.replace(
"""      if (enteredHash === CONFIG.adminCodeHash) {\n        setAdminMode(true);\n        closeAdminModal();\n""",
"""      if (enteredHash === CONFIG.adminCodeHash) {\n        state.adminCode = adminCodeInput.value;\n        saveAdminCodeSession(state.adminCode);\n        setAdminMode(true);\n        closeAdminModal();\n        syncAllLocalOverridesToCloud();\n""",
1,
)

save_anchor = """    function saveManualGenderOverrides() {\n      try {\n        localStorage.setItem(STORAGE_KEY, JSON.stringify(state.manualGenderOverrides));\n      } catch (err) {\n        console.warn('수동 성별 분류 저장 실패', err);\n      }\n    }\n\n"""
cloud_code = save_anchor + """    async function fetchCloudGenderMap() {\n      const response = await fetch(\n        `${CONFIG.supabaseUrl}/rest/v1/gender_overrides?select=applicant_key,gender,nickname`,\n        {\n          headers: { apikey: CONFIG.supabasePublishableKey },\n          cache: 'no-store'\n        }\n      );\n      if (!response.ok) throw new Error(`HTTP ${response.status}`);\n      const rows = await response.json();\n      const cloud = {};\n      for (const row of Array.isArray(rows) ? rows : []) {\n        const key = String(row?.applicant_key || '').trim();\n        const gender = String(row?.gender || '').trim();\n        if (key && (gender === 'female' || gender === 'male' || gender === 'unknown')) cloud[key] = gender;\n      }\n      return cloud;\n    }\n\n    async function loadCloudGenderOverrides() {\n      try {\n        const cloud = await fetchCloudGenderMap();\n        // 서버 값을 우선해서 PC/모바일/다른 브라우저가 같은 분류를 표시합니다.\n        state.manualGenderOverrides = { ...state.manualGenderOverrides, ...cloud };\n        saveManualGenderOverrides();\n        if (!state.loading) render();\n        return cloud;\n      } catch (err) {\n        console.warn('공용 성별 분류 불러오기 실패', err);\n        return null;\n      }\n    }\n\n    async function syncGenderOperation(payload) {\n      if (!state.isAdmin || !state.adminCode) return false;\n      try {\n        const response = await fetch(`${CONFIG.supabaseUrl}/functions/v1/gender-sync`, {\n          method: 'POST',\n          headers: {\n            'Content-Type': 'application/json',\n            apikey: CONFIG.supabasePublishableKey\n          },\n          body: JSON.stringify({ adminCode: state.adminCode, ...payload })\n        });\n        if (!response.ok) throw new Error(`HTTP ${response.status}`);\n        return true;\n      } catch (err) {\n        console.warn('성별 분류 동기화 실패', err);\n        return false;\n      }\n    }\n\n    async function syncGenderForItem(item, gender) {\n      const keys = manualGenderKeys(item);\n      if (!keys.length) return false;\n      return syncGenderOperation({ operation: 'set', keys, gender, nickname: item?.nickname || '' });\n    }\n\n    async function syncStandaloneGenderKey(key, gender, nickname = '') {\n      if (!key) return false;\n      return syncGenderOperation({ operation: 'set', keys: [key], gender, nickname });\n    }\n\n    async function syncAllLocalOverridesToCloud() {\n      if (!state.isAdmin || !state.adminCode) return;\n      try {\n        const cloud = await fetchCloudGenderMap();\n        // 기존 PC의 분류는 최초 1회 클라우드로 옮기되, 이미 서버에 있는 값은 덮어쓰지 않습니다.\n        for (const [key, gender] of Object.entries(state.manualGenderOverrides)) {\n          if (key in cloud) continue;\n          if (gender !== 'female' && gender !== 'male' && gender !== 'unknown') continue;\n          await syncStandaloneGenderKey(key, gender);\n        }\n        await loadCloudGenderOverrides();\n      } catch (err) {\n        console.warn('기존 수동 분류 이전 실패', err);\n      }\n    }\n\n"""
text = text.replace(save_anchor, cloud_code, 1)

# Sync every administrator change to the shared database.
old = """          saveManualGenderOverrides();\n          render();\n"""
new = """          saveManualGenderOverrides();\n          if (item) syncGenderForItem(item, 'unknown');\n          else syncStandaloneGenderKey(key, 'unknown');\n          render();\n"""
text = text.replace(old, new, 1)

marker = "const genderBtn = e.target.closest('[data-manual-gender]');"
pos = text.find(marker)
if pos != -1:
    hit = text.find(old, pos)
    if hit != -1:
        new2 = """          saveManualGenderOverrides();\n          if (item) syncGenderForItem(item, gender);\n          else syncStandaloneGenderKey(key, gender);\n          render();\n"""
        text = text[:hit] + new2 + text[hit + len(old):]

text = text.replace(
"""        state.manualGenderOverrides = {};\n        saveManualGenderOverrides();\n        render();\n""",
"""        state.manualGenderOverrides = {};\n        saveManualGenderOverrides();\n        syncGenderOperation({ operation: 'reset' });\n        render();\n""",
1,
)

text = text.replace(
"""        saveManualGenderOverrides();\n        render();\n      }\n      draggedKey = '';\n""",
"""        saveManualGenderOverrides();\n        if (item) syncGenderForItem(item, gender);\n        else syncStandaloneGenderKey(key, gender);\n        render();\n      }\n      draggedKey = '';\n""",
1,
)

text = text.replace(
"""    state.isAdmin = loadAdminSession();\n    updateAdminUi();\n    state.manualGenderOverrides = loadManualGenderOverrides();\n    loadComments();\n""",
"""    state.isAdmin = loadAdminSession();\n    state.adminCode = loadAdminCodeSession();\n    if (state.isAdmin && !state.adminCode) state.isAdmin = false;\n    updateAdminUi();\n    state.manualGenderOverrides = loadManualGenderOverrides();\n    loadCloudGenderOverrides();\n    if (state.isAdmin) syncAllLocalOverridesToCloud();\n    loadComments();\n""",
1,
)

text = text.replace(
"""      if (!document.hidden && !state.loading) loadComments({ silent: true });\n    }, 60_000);\n""",
"""      if (!document.hidden && !state.loading) {\n        loadComments({ silent: true });\n        loadCloudGenderOverrides();\n      }\n    }, 60_000);\n""",
1,
)

mobile_css = r"""
    /* ===== Mobile readability fix ===== */
    @media (max-width: 640px) {
      .wrap { width: calc(100% - 14px) !important; }
      .split { grid-template-columns: minmax(0, 1fr) !important; gap: 12px !important; }
      .board, .female-board, .male-board, .single {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
      }
      .board-head { padding-left: 14px !important; padding-right: 14px !important; }
      .rank-row {
        width: 100%; min-width: 0;
        grid-template-columns: 34px 40px minmax(0, 1fr) auto !important;
        gap: 8px !important; padding: 0 12px !important;
      }
      .rank-row.has-admin-action, .single .rank-row.has-admin-action {
        grid-template-columns: 34px 40px minmax(0, 1fr) auto 28px !important;
      }
      .rank-num { width: 30px !important; height: 30px !important; font-size: 12px !important; }
      .avatar-wrap { width: 36px !important; height: 36px !important; }
      .name, .name-wrap, .applicant-info { min-width: 0 !important; max-width: 100% !important; }
      .name {
        display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
        font-size: 13px !important;
      }
      .likes { min-width: 50px !important; white-space: nowrap; }
      .unknown-row {
        width: 100%; min-width: 0;
        grid-template-columns: 34px 40px minmax(0, 1fr) auto !important;
        padding-left: 12px !important; padding-right: 12px !important;
      }
      .unknown-row .gender-actions { min-width: 0; flex-wrap: wrap; }
      .toolbar { grid-template-columns: minmax(0,1fr) minmax(0,1fr) !important; }
      .toolbar > * { min-width: 0; }
    }

"""
text = text.replace('</style>', mobile_css + '</style>', 1)

p.write_text(text, encoding='utf-8')
