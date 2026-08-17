from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Strongly declare this site as a light-color site so mobile/browser dark mode
# does not auto-transform decorative gradients into a black vignette.
if '<meta name="color-scheme" content="only light" />' not in text:
    text = text.replace(
        '<meta name="theme-color" content="#eaf7ff" />',
        '<meta name="theme-color" content="#eaf7ff" />\n  <meta name="color-scheme" content="only light" />',
        1,
    )
text = text.replace('html { color-scheme: light; }', 'html { color-scheme: only light; }', 1)

css = r'''

    /* ===== Dark-mode forced-vignette prevention ===== */
    @media (prefers-color-scheme: dark) {
      html,
      body,
      body.top100-mode {
        color-scheme: only light !important;
        background: #f4f9fd !important;
        background-image: none !important;
        color: #183047 !important;
      }
      body::before,
      body::after,
      .hero::before,
      .hero::after {
        display: none !important;
        content: none !important;
      }
      .hero {
        background: #ffffff !important;
        background-image: none !important;
      }
    }
'''
if '/* ===== Dark-mode forced-vignette prevention ===== */' not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

# Track the exact cloud NEW version that has been seen in this browser tab.
old_state = """      adminCode: '',
      sharedNewApplicants: new Set()
    };

    const STORAGE_KEY = 'soop-rank-manual-gender-v1';
    const ADMIN_SESSION_KEY = 'soop-rank-admin-session-v1';
    const ADMIN_CODE_SESSION_KEY = 'soop-rank-admin-code-session-v1';
"""
new_state = """      adminCode: '',
      sharedNewApplicants: new Set(),
      sharedNewVersions: {}
    };

    const STORAGE_KEY = 'soop-rank-manual-gender-v1';
    const ADMIN_SESSION_KEY = 'soop-rank-admin-session-v1';
    const ADMIN_CODE_SESSION_KEY = 'soop-rank-admin-code-session-v1';
    const NEW_SEEN_SESSION_KEY = 'soop-rank-seen-new-v1';
"""
if old_state not in text:
    raise SystemExit('state/constants target not found')
text = text.replace(old_state, new_state, 1)

# Helpers: shared NEW is shown once per browser tab, and is dismissed on a
# real page refresh / navigation or the site's refresh button.
anchor = """    function saveAdminCodeSession(code) {
      try {
        if (code) sessionStorage.setItem(ADMIN_CODE_SESSION_KEY, code);
        else sessionStorage.removeItem(ADMIN_CODE_SESSION_KEY);
      } catch {}
    }

"""
helpers = anchor + """    function loadSeenNewVersions() {
      try {
        const saved = JSON.parse(sessionStorage.getItem(NEW_SEEN_SESSION_KEY) || '{}');
        return saved && typeof saved === 'object' ? saved : {};
      } catch { return {}; }
    }

    function saveSeenNewVersions(value) {
      try { sessionStorage.setItem(NEW_SEEN_SESSION_KEY, JSON.stringify(value || {})); }
      catch {}
    }

    function dismissCurrentNewBadges(renderNow = false) {
      const seen = loadSeenNewVersions();
      const fallbackUntil = Date.now() + 31 * 60 * 1000;

      for (const key of state.sharedNewApplicants) {
        const version = Number(state.sharedNewVersions?.[key] || 0);
        seen[key] = Math.max(Number(seen[key] || 0), version || fallbackUntil);
      }
      // Locally dragged rows may not have re-fetched their cloud new_until yet.
      // A slightly-longer local marker guarantees that the next reload does not
      // resurrect the same NEW! badge from the shared database.
      for (const key of state.newDraggedApplicants) {
        seen[key] = Math.max(Number(seen[key] || 0), fallbackUntil);
        const item = state.comments.find(x => itemKey(x) === key);
        if (item) {
          for (const alias of manualGenderKeys(item)) {
            seen[alias] = Math.max(Number(seen[alias] || 0), fallbackUntil);
          }
        }
      }

      saveSeenNewVersions(seen);
      state.newDraggedApplicants.clear();
      state.sharedNewApplicants.clear();
      state.sharedNewVersions = {};
      if (renderNow && !state.loading) render();
    }

"""
if anchor not in text:
    raise SystemExit('admin session helper anchor not found')
text = text.replace(anchor, helpers, 1)

# Cloud NEW rows are only re-shown if the database has a newer new_until than
# the version this tab already dismissed.
old_cloud = """      const cloud = {};
      const sharedNew = new Set();
      const now = Date.now();
      for (const row of Array.isArray(rows) ? rows : []) {
        const key = String(row?.applicant_key || '').trim();
        const gender = String(row?.gender || '').trim();
        if (key && (gender === 'female' || gender === 'male' || gender === 'unknown')) cloud[key] = gender;
        const newUntil = row?.new_until ? Date.parse(row.new_until) : 0;
        if (key && Number.isFinite(newUntil) && newUntil > now) sharedNew.add(key);
      }
      state.sharedNewApplicants = sharedNew;
      return cloud;
"""
new_cloud = """      const cloud = {};
      const sharedNew = new Set();
      const sharedNewVersions = {};
      const seenNew = loadSeenNewVersions();
      const now = Date.now();
      for (const row of Array.isArray(rows) ? rows : []) {
        const key = String(row?.applicant_key || '').trim();
        const gender = String(row?.gender || '').trim();
        if (key && (gender === 'female' || gender === 'male' || gender === 'unknown')) cloud[key] = gender;
        const newUntil = row?.new_until ? Date.parse(row.new_until) : 0;
        if (key && Number.isFinite(newUntil) && newUntil > now) {
          sharedNewVersions[key] = newUntil;
          if (newUntil > Number(seenNew[key] || 0)) sharedNew.add(key);
        }
      }
      state.sharedNewApplicants = sharedNew;
      state.sharedNewVersions = sharedNewVersions;
      return cloud;
"""
if old_cloud not in text:
    raise SystemExit('cloud NEW target not found')
text = text.replace(old_cloud, new_cloud, 1)

# The site's refresh button explicitly dismisses NEW! first.
old_refresh = "    $('#refreshBtn').addEventListener('click', () => loadComments({ silent: state.comments.length > 0 }));"
new_refresh = """    $('#refreshBtn').addEventListener('click', () => {
      dismissCurrentNewBadges(true);
      loadComments({ silent: state.comments.length > 0 });
      loadCloudGenderOverrides();
    });"""
if old_refresh not in text:
    raise SystemExit('refresh button target not found')
text = text.replace(old_refresh, new_refresh, 1)

# A browser page reload/navigation fires pagehide, so remember the currently
# displayed NEW! versions before the next page boots.
startup_anchor = """    state.isAdmin = loadAdminSession();
    state.adminCode = loadAdminCodeSession();
"""
startup_replacement = """    window.addEventListener('pagehide', () => dismissCurrentNewBadges(false));

    state.isAdmin = loadAdminSession();
    state.adminCode = loadAdminCodeSession();
"""
if startup_anchor not in text:
    raise SystemExit('startup anchor not found')
text = text.replace(startup_anchor, startup_replacement, 1)

p.write_text(text, encoding='utf-8')
