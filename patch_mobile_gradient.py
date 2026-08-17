from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '\n</style>'
css = r'''

    /* ===== Mobile page background gradient ===== */
    @media (max-width: 640px) {
      html {
        background: #eef7fc !important;
        background-image:
          radial-gradient(circle at 8% 0%, rgba(118, 207, 255, .30) 0%, rgba(118, 207, 255, 0) 36%),
          radial-gradient(circle at 96% 20%, rgba(184, 226, 250, .22) 0%, rgba(184, 226, 250, 0) 34%),
          linear-gradient(180deg, #fbfeff 0%, #f4fbff 34%, #edf7fc 72%, #e7f2f9 100%) !important;
        background-color: #eef7fc !important;
      }
      body,
      body.top100-mode {
        min-height: 100vh !important;
        color-scheme: only light !important;
        background:
          radial-gradient(circle at 8% 0%, rgba(118, 207, 255, .30) 0%, rgba(118, 207, 255, 0) 36%),
          radial-gradient(circle at 96% 20%, rgba(184, 226, 250, .22) 0%, rgba(184, 226, 250, 0) 34%),
          linear-gradient(180deg, #fbfeff 0%, #f4fbff 34%, #edf7fc 72%, #e7f2f9 100%) !important;
        background-color: #eef7fc !important;
        background-attachment: scroll !important;
      }
    }
'''

if '/* ===== Mobile page background gradient ===== */' not in text:
    text = text.replace(marker, css + marker, 1)
p.write_text(text, encoding='utf-8')
