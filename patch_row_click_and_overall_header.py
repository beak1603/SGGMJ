from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# 1) Make nickname a plain span so mobile long-press does not open the browser link menu.
name_pattern = re.compile(r"    function nameHtml\(item\) \{.*?^    \}\n\n    function badgeHtml", re.S | re.M)
name_replacement = '''    function nameHtml(item) {
      const label = esc(item.nickname);
      return `<span class="name-link">${label}</span>`;
    }

    function badgeHtml'''
text, n = name_pattern.subn(name_replacement, text, count=1)
if n != 1:
    raise SystemExit('nameHtml patch target not found')

# 2) Add the comment URL to every normal ranking row.
old_rank = '      return `<div class="rank-row${topClass}${actionClass}"${dragAttrs}>'
new_rank = '      return `<div class="rank-row${topClass}${actionClass}"${dragAttrs} data-comment-url="${esc(commentUrl(item))}" role="link" tabindex="0">'
if old_rank not in text:
    raise SystemExit('rank-row opening target not found')
text = text.replace(old_rank, new_rank, 1)

# 3) Add the comment URL to rows in the 신규 신청자 section too.
old_unknown = '      return `<div class="unknown-row">'
new_unknown = '      return `<div class="unknown-row" data-comment-url="${esc(commentUrl(item))}" role="link" tabindex="0">'
if old_unknown not in text:
    raise SystemExit('unknown-row opening target not found')
text = text.replace(old_unknown, new_unknown, 1)

# 4) Row click: anywhere except admin buttons opens the original SOOP comment.
click_anchor = """    contentEl.addEventListener('click', (e) => {\n      const unclassifyBtn = e.target.closest('[data-unclassify]');\n"""
click_replacement = """    contentEl.addEventListener('click', (e) => {\n      const rowLink = e.target.closest('[data-comment-url]');\n      if (rowLink && !e.target.closest('button')) {\n        const url = rowLink.dataset.commentUrl || '';\n        if (url) {\n          window.open(url, '_blank', 'noopener,noreferrer');\n          return;\n        }\n      }\n\n      const unclassifyBtn = e.target.closest('[data-unclassify]');\n"""
if click_anchor not in text:
    raise SystemExit('content click handler target not found')
text = text.replace(click_anchor, click_replacement, 1)

# Keyboard support for the new full-row link behavior.
keyboard_js = """

    contentEl.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      if (e.target.closest('button')) return;
      const rowLink = e.target.closest('[data-comment-url]');
      if (!rowLink) return;
      const url = rowLink.dataset.commentUrl || '';
      if (!url) return;
      e.preventDefault();
      window.open(url, '_blank', 'noopener,noreferrer');
    });
"""
marker = "    let draggedKey = '';"
if keyboard_js.strip() not in text:
    if marker not in text:
        raise SystemExit('keyboard insert marker not found')
    text = text.replace(marker, keyboard_js + '\n' + marker, 1)

# 5) Clean up the overall board header/count. The total count becomes simple text, not a dark pill.
css = r'''

    /* ===== Overall board header cleanup ===== */
    .single .board-head {
      background: #f8fcff !important;
      background-image: none !important;
      border-bottom-color: #dceaf3 !important;
      color: #183047 !important;
      box-shadow: inset 0 -1px 0 rgba(214, 231, 241, .55);
      forced-color-adjust: none;
    }
    .single .board-title strong {
      color: #2f6f92 !important;
    }
    .single .board-title:first-child > span {
      margin-left: 2px !important;
      padding: 0 !important;
      border: 0 !important;
      border-radius: 0 !important;
      background: transparent !important;
      background-image: none !important;
      box-shadow: none !important;
      color: #6a8291 !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      line-height: 1 !important;
      forced-color-adjust: none;
    }
    .single .board-head > .board-title:last-child > span {
      background: #eef8fe !important;
      background-image: none !important;
      border-color: #cfe7f4 !important;
      color: #4b7790 !important;
      box-shadow: none !important;
      forced-color-adjust: none;
    }

    /* Rows are full click targets, but keep the existing visual cursor behavior. */
    .rank-row[data-comment-url],
    .unknown-row[data-comment-url] {
      outline: none;
    }
    .rank-row[data-comment-url]:focus-visible,
    .unknown-row[data-comment-url]:focus-visible {
      box-shadow: inset 0 0 0 2px rgba(57, 175, 240, .28);
    }
'''
if '/* ===== Overall board header cleanup ===== */' not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

p.write_text(text, encoding='utf-8')
