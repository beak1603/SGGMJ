from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

css = r'''

    /* ===== Restore subtle page gradient across browsers ===== */
    html {
      background: #eef6fb !important;
    }
    body,
    body.top100-mode {
      background:
        radial-gradient(circle at 12% -4%, rgba(143, 216, 255, .20) 0%, rgba(143, 216, 255, 0) 33%),
        linear-gradient(180deg, #f9fdff 0%, #f4faff 48%, #eef6fb 100%) !important;
      background-color: #f4faff !important;
      background-attachment: fixed !important;
    }
    @media (prefers-color-scheme: dark) {
      html {
        background: #eef6fb !important;
      }
      body,
      body.top100-mode {
        color-scheme: only light !important;
        background:
          radial-gradient(circle at 12% -4%, rgba(143, 216, 255, .20) 0%, rgba(143, 216, 255, 0) 33%),
          linear-gradient(180deg, #f9fdff 0%, #f4faff 48%, #eef6fb 100%) !important;
        background-color: #f4faff !important;
        background-attachment: fixed !important;
      }
      .hero {
        background: transparent !important;
        background-image: none !important;
      }
    }
'''

marker = '/* ===== Restore subtle page gradient across browsers ===== */'
if marker not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

p.write_text(text, encoding='utf-8')
