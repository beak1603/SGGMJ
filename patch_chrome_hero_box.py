from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

css = r'''

    /* ===== Cross-browser hero background normalization ===== */
    /* Chrome/Edge/OS color-scheme differences must not create a white panel. */
    .hero {
      background: transparent !important;
      background-color: transparent !important;
      background-image: none !important;
      border-color: transparent !important;
      box-shadow: none !important;
      -webkit-backdrop-filter: none !important;
      backdrop-filter: none !important;
    }
    .hero::before,
    .hero::after {
      display: none !important;
      content: none !important;
      background: none !important;
      box-shadow: none !important;
    }

    @media (prefers-color-scheme: dark) {
      .hero {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
      }
    }
'''

marker = '/* ===== Cross-browser hero background normalization ===== */'
if marker not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

p.write_text(text, encoding='utf-8')
