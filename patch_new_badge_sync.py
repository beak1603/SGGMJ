from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

text = text.replace(
"""      isAdmin: false,\n      adminCode: ''\n    };\n""",
"""      isAdmin: false,\n      adminCode: '',\n      sharedNewApplicants: new Set()\n    };\n""",
1,
)

text = text.replace(
"""        `${CONFIG.supabaseUrl}/rest/v1/gender_overrides?select=applicant_key,gender,nickname`,\n""",
"""        `${CONFIG.supabaseUrl}/rest/v1/gender_overrides?select=applicant_key,gender,nickname,new_until`,\n""",
1,
)

old_loop = """      const cloud = {};\n      for (const row of Array.isArray(rows) ? rows : []) {\n        const key = String(row?.applicant_key || '').trim();\n        const gender = String(row?.gender || '').trim();\n        if (key && (gender === 'female' || gender === 'male' || gender === 'unknown')) cloud[key] = gender;\n      }\n      return cloud;\n"""
new_loop = """      const cloud = {};\n      const sharedNew = new Set();\n      const now = Date.now();\n      for (const row of Array.isArray(rows) ? rows : []) {\n        const key = String(row?.applicant_key || '').trim();\n        const gender = String(row?.gender || '').trim();\n        if (key && (gender === 'female' || gender === 'male' || gender === 'unknown')) cloud[key] = gender;\n        const newUntil = row?.new_until ? Date.parse(row.new_until) : 0;\n        if (key && Number.isFinite(newUntil) && newUntil > now) sharedNew.add(key);\n      }\n      state.sharedNewApplicants = sharedNew;\n      return cloud;\n"""
text = text.replace(old_loop, new_loop, 1)

text = text.replace(
"""            p_gender: String(payload?.gender || ''),\n            p_nickname: String(payload?.nickname || '')\n""",
"""            p_gender: String(payload?.gender || ''),\n            p_nickname: String(payload?.nickname || ''),\n            p_mark_new: Boolean(payload?.markNew)\n""",
1,
)

text = text.replace(
"""    async function syncGenderForItem(item, gender) {\n      const keys = manualGenderKeys(item);\n      if (!keys.length) return false;\n      return syncGenderOperation({ operation: 'set', keys, gender, nickname: item?.nickname || '' });\n    }\n""",
"""    async function syncGenderForItem(item, gender, markNew = false) {\n      const keys = manualGenderKeys(item);\n      if (!keys.length) return false;\n      return syncGenderOperation({ operation: 'set', keys, gender, nickname: item?.nickname || '', markNew });\n    }\n""",
1,
)

text = text.replace(
"""    function badgeHtml(item) {\n      const key = itemKey(item);\n      const dragged = state.newDraggedApplicants.has(key) ? `<span class=\\\"new-badge\\\">NEW!</span>` : '';\n      const fresh = state.newApplicants.has(key) ? `<span class=\\\"fresh-badge\\\">신규</span>` : '';\n      return dragged + fresh;\n    }\n""",
"""    function badgeHtml(item) {\n      const key = itemKey(item);\n      const sharedNew = manualGenderKeys(item).some(k => state.sharedNewApplicants.has(k));\n      const dragged = (state.newDraggedApplicants.has(key) || sharedNew) ? `<span class=\\\"new-badge\\\">NEW!</span>` : '';\n      const fresh = state.newApplicants.has(key) ? `<span class=\\\"fresh-badge\\\">신규</span>` : '';\n      return dragged + fresh;\n    }\n""",
1,
)

# Mark NEW only for drag-and-drop manual reclassification, preserving original semantics.
needle = """        if (item) syncGenderForItem(item, gender);\n        else syncStandaloneGenderKey(key, gender);\n        render();\n      }\n      draggedKey = '';\n"""
replacement = """        if (item) syncGenderForItem(item, gender, true);\n        else syncGenderOperation({ operation: 'set', keys: [key], gender, nickname: '', markNew: true });\n        render();\n      }\n      draggedKey = '';\n"""
text = text.replace(needle, replacement, 1)

# Make NEW! visible in the very narrow mobile two-column layout instead of being clipped by nickname overflow.
mobile_anchor = """      .split .name {\n        display: block !important;\n        overflow: hidden !important;\n        text-overflow: ellipsis !important;\n        white-space: nowrap !important;\n        font-size: 10px !important;\n"""
mobile_replace = """      .split .name {\n        display: flex !important;\n        align-items: center !important;\n        gap: 2px !important;\n        overflow: visible !important;\n        white-space: nowrap !important;\n        font-size: 10px !important;\n"""
text = text.replace(mobile_anchor, mobile_replace, 1)

css_insert = """
      .split .name-link {
        min-width: 0 !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
      }
      .split .new-badge {
        display: inline-block !important;
        flex: 0 0 auto !important;
        margin-left: 1px !important;
        font-size: 7px !important;
        line-height: 1 !important;
        padding: 0 !important;
      }
"""
marker = """      .split .likes {\n"""
idx = text.find(marker)
if idx != -1:
    text = text[:idx] + css_insert + text[idx:]

p.write_text(text, encoding='utf-8')
