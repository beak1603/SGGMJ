from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

if 'Application deadline countdown' not in text:
    css = r'''

    /* ===== Application deadline countdown ===== */
    .deadline-countdown {
      width: fit-content;
      max-width: 100%;
      margin: -8px 0 17px;
      display: flex;
      align-items: baseline;
      gap: 8px;
      flex-wrap: wrap;
      padding: 9px 12px;
      border: 1px solid #cfe8f6;
      border-radius: 12px;
      background: rgba(239, 249, 255, .82);
      color: #426c84;
      box-shadow: 0 4px 14px rgba(50, 126, 168, .055);
      font-variant-numeric: tabular-nums;
    }
    .deadline-countdown .deadline-label {
      font-size: 11px;
      font-weight: 850;
      white-space: nowrap;
    }
    .deadline-countdown strong {
      color: #167eae;
      font-size: 17px;
      font-weight: 950;
      letter-spacing: -.015em;
      white-space: nowrap;
    }
    .deadline-countdown .deadline-date {
      color: #78909e;
      font-size: 10px;
      font-weight: 750;
      white-space: nowrap;
    }
    .deadline-countdown.is-warning {
      border-color: #f0d5a2;
      background: rgba(255, 249, 236, .92);
      color: #9a6a25;
    }
    .deadline-countdown.is-warning strong { color: #dc861a; }
    .deadline-countdown.is-urgent {
      border-color: #efb9b9;
      background: rgba(255, 243, 243, .95);
      color: #a84949;
    }
    .deadline-countdown.is-urgent strong { color: #d94848; }
    .deadline-countdown.is-closed {
      border-color: #d9e2e8;
      background: rgba(246, 249, 251, .94);
      color: #697e8b;
    }
    .deadline-countdown.is-closed strong { color: #405b6a; }
    @media (max-width: 640px) {
      .deadline-countdown {
        margin-top: -4px;
        margin-bottom: 14px;
        gap: 5px 7px;
        padding: 7px 9px;
        border-radius: 10px;
      }
      .deadline-countdown .deadline-label { font-size: 9px; }
      .deadline-countdown strong { font-size: 13px; }
      .deadline-countdown .deadline-date { font-size: 8px; }
    }
'''
    text = text.replace('</style>', css + '\n</style>', 1)

    html_anchor = '      </h1>\n      <div class="hero-meta" aria-label="참가자 통계">'
    html_insert = '''      </h1>\n      <div id="deadlineCountdown" class="deadline-countdown" role="status" aria-live="polite">\n        <span class="deadline-label">신청 마감까지</span>\n        <strong id="deadlineTime">계산 중...</strong>\n        <span class="deadline-date">8월 21일 23:59 마감</span>\n      </div>\n      <div class="hero-meta" aria-label="참가자 통계">'''
    if html_anchor not in text:
        raise SystemExit('HTML anchor not found')
    text = text.replace(html_anchor, html_insert, 1)

    state_anchor = '    const state = {'
    deadline_const = "    const APPLICATION_DEADLINE = new Date('2026-08-21T23:59:59+09:00').getTime();\n\n"
    if state_anchor not in text:
        raise SystemExit('state anchor not found')
    text = text.replace(state_anchor, deadline_const + state_anchor, 1)

    function_anchor = '    function loadAdminSession() {'
    deadline_function = r'''    function updateDeadlineCountdown() {
      const box = $('#deadlineCountdown');
      const timeEl = $('#deadlineTime');
      if (!box || !timeEl) return;

      const remaining = APPLICATION_DEADLINE - Date.now();
      box.classList.remove('is-warning', 'is-urgent', 'is-closed');

      if (remaining <= 0) {
        timeEl.textContent = '신청이 마감되었습니다';
        box.classList.add('is-closed');
        return;
      }

      const totalSeconds = Math.floor(remaining / 1000);
      const days = Math.floor(totalSeconds / 86400);
      const hours = Math.floor((totalSeconds % 86400) / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;

      timeEl.textContent = `${days}일 ${String(hours).padStart(2, '0')}시간 ${String(minutes).padStart(2, '0')}분 ${String(seconds).padStart(2, '0')}초`;

      if (remaining < 3 * 60 * 60 * 1000) box.classList.add('is-urgent');
      else if (remaining < 24 * 60 * 60 * 1000) box.classList.add('is-warning');
    }

'''
    if function_anchor not in text:
        raise SystemExit('function anchor not found')
    text = text.replace(function_anchor, deadline_function + function_anchor, 1)

    init_anchor = "    window.addEventListener('pagehide', () => dismissCurrentNewBadges(false));"
    init_insert = "    updateDeadlineCountdown();\n    setInterval(updateDeadlineCountdown, 1000);\n\n" + init_anchor
    if init_anchor not in text:
        raise SystemExit('init anchor not found')
    text = text.replace(init_anchor, init_insert, 1)

    p.write_text(text, encoding='utf-8')
else:
    print('Deadline countdown already present; no changes made.')
