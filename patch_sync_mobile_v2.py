from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old_sync = '''    async function syncGenderOperation(payload) {
      if (!state.isAdmin || !state.adminCode) return false;
      try {
        const response = await fetch(`${CONFIG.supabaseUrl}/functions/v1/gender-sync`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            apikey: CONFIG.supabasePublishableKey
          },
          body: JSON.stringify({ adminCode: state.adminCode, ...payload })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return true;
      } catch (err) {
        console.warn('성별 분류 동기화 실패', err);
        return false;
      }
    }
'''

new_sync = '''    async function syncGenderOperation(payload) {
      if (!state.isAdmin || !state.adminCode) return false;
      try {
        const operation = String(payload?.operation || '');
        let rpcName = '';
        let rpcBody = {};

        if (operation === 'set') {
          rpcName = 'set_gender_override';
          rpcBody = {
            p_admin_code: state.adminCode,
            p_keys: Array.isArray(payload?.keys) ? payload.keys : [],
            p_gender: String(payload?.gender || ''),
            p_nickname: String(payload?.nickname || '')
          };
        } else if (operation === 'reset') {
          rpcName = 'reset_gender_overrides';
          rpcBody = { p_admin_code: state.adminCode };
        } else {
          return false;
        }

        const response = await fetch(`${CONFIG.supabaseUrl}/rest/v1/rpc/${rpcName}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            apikey: CONFIG.supabasePublishableKey
          },
          cache: 'no-store',
          body: JSON.stringify(rpcBody)
        });
        if (!response.ok) {
          const detail = await response.text().catch(() => '');
          throw new Error(`HTTP ${response.status}${detail ? ` · ${detail}` : ''}`);
        }
        return true;
      } catch (err) {
        console.warn('성별 분류 동기화 실패', err);
        return false;
      }
    }
'''

if old_sync not in text:
    raise SystemExit('syncGenderOperation block not found')
text = text.replace(old_sync, new_sync, 1)

old_keys = '''    function manualGenderKeys(item) {
      const keys = [];
      if (item?.userId) keys.push(`uid:${String(item.userId).toLocaleLowerCase('en')}`);
      if (item?.nickname) keys.push(`nick:${String(item.nickname).normalize('NFKC').toLocaleLowerCase('ko')}`);
      return [...new Set(keys)];
    }

    function getManualGender(item) {
      for (const key of manualGenderKeys(item)) {
        const value = state.manualGenderOverrides[key];
        if (value === 'female' || value === 'male' || value === 'unknown') return value;
      }
      return '';
    }
'''

new_keys = '''    function manualGenderKeys(item) {
      const keys = [];
      if (item?.userId) keys.push(`uid:${String(item.userId).toLocaleLowerCase('en')}`);
      if (item?.nickname) keys.push(`nick:${String(item.nickname).normalize('NFKC').toLocaleLowerCase('ko')}`);
      return [...new Set(keys)];
    }

    function legacyManualGenderKeys(item) {
      const keys = [];
      if (item?.userId) {
        keys.push(String(item.userId));
        keys.push(String(item.userId).toLocaleLowerCase('en'));
      }
      if (item?.nickname) {
        keys.push(String(item.nickname));
        keys.push(String(item.nickname).normalize('NFKC').toLocaleLowerCase('ko'));
      }
      return [...new Set(keys.filter(Boolean))];
    }

    function getManualGender(item) {
      for (const key of [...manualGenderKeys(item), ...legacyManualGenderKeys(item)]) {
        const value = state.manualGenderOverrides[key];
        if (value === 'female' || value === 'male' || value === 'unknown') return value;
      }
      return '';
    }
'''

if old_keys not in text:
    raise SystemExit('manualGenderKeys block not found')
text = text.replace(old_keys, new_keys, 1)

old_reconcile_call = '''        state.comments = applicants.sort(compareRankItems);
        reconcileManualGenderOverrides(state.comments);
        if (previousKeys) {
'''
new_reconcile_call = '''        state.comments = applicants.sort(compareRankItems);
        reconcileManualGenderOverrides(state.comments);
        if (state.isAdmin && state.adminCode) syncAllLocalOverridesToCloud();
        if (previousKeys) {
'''
if old_reconcile_call not in text:
    raise SystemExit('reconcile call block not found')
text = text.replace(old_reconcile_call, new_reconcile_call, 1)

start_marker = '    /* ===== Mobile readability fix ===== */\n'
end_marker = '\n</style>'
start = text.find(start_marker)
if start == -1:
    raise SystemExit('mobile CSS marker not found')
end = text.find(end_marker, start)
if end == -1:
    raise SystemExit('style end not found')

mobile_css = '''    /* ===== Mobile two-column compact layout ===== */
    @media (max-width: 640px) {
      .wrap { width: calc(100% - 10px) !important; }

      /* 모바일에서도 여자/남자 랭킹은 좌우 2열을 유지합니다. */
      .split {
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        gap: 6px !important;
        align-items: stretch !important;
      }
      .split > .board {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
      }

      .split .board-head {
        height: 48px !important;
        padding: 0 7px !important;
        gap: 3px !important;
      }
      .split .board-title { gap: 3px !important; min-width: 0 !important; }
      .split .board-title strong {
        font-size: 11px !important;
        white-space: nowrap !important;
      }
      .split .board-title span {
        font-size: 9px !important;
        white-space: nowrap !important;
      }
      .split .board-head > .board-title:last-child span {
        font-size: 8px !important;
      }

      .split .rank-row {
        width: 100% !important;
        min-width: 0 !important;
        height: 52px !important;
        grid-template-columns: 22px 28px minmax(0, 1fr) auto !important;
        gap: 3px !important;
        padding: 0 5px !important;
      }
      .split .rank-row.has-admin-action {
        grid-template-columns: 22px 28px minmax(0, 1fr) auto 20px !important;
      }
      .split .rank-num {
        width: 22px !important;
        min-width: 22px !important;
        height: 22px !important;
        font-size: 9px !important;
      }
      .split .avatar-wrap {
        width: 28px !important;
        min-width: 28px !important;
        height: 28px !important;
      }
      .split .name,
      .split .name-wrap,
      .split .applicant-info {
        min-width: 0 !important;
        max-width: 100% !important;
      }
      .split .name {
        display: block !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        font-size: 10px !important;
        line-height: 1.2 !important;
      }
      .split .likes {
        min-width: 0 !important;
        gap: 1px !important;
        padding-left: 1px !important;
        font-size: 10px !important;
        white-space: nowrap !important;
      }
      .split .heart { font-size: 11px !important; }
      .split .rank-move { font-size: 8px !important; margin-left: 2px !important; }
      .split .badge,
      .split .new-badge { font-size: 7px !important; padding: 1px 3px !important; }
      .split .undo-gender-btn {
        width: 20px !important;
        min-width: 20px !important;
        height: 20px !important;
        padding: 0 !important;
        font-size: 10px !important;
      }

      /* 신규 신청자 영역은 전체 폭을 사용합니다. */
      .unknown-section .board,
      .single .board {
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
      }
      .unknown-section .rank-row,
      .unknown-row,
      .single .rank-row {
        min-width: 0 !important;
      }
      .unknown-row {
        grid-template-columns: 30px 36px minmax(0, 1fr) auto !important;
        gap: 6px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
      }
      .unknown-row .gender-actions { min-width: 0 !important; flex-wrap: wrap !important; }

      .toolbar { grid-template-columns: minmax(0,1fr) minmax(0,1fr) !important; }
      .toolbar > * { min-width: 0 !important; }
    }
'''

text = text[:start] + mobile_css + text[end:]
p.write_text(text, encoding='utf-8')
