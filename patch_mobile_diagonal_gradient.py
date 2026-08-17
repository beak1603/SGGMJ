from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''    /* ===== Mobile page background gradient ===== */
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

new = '''    /* ===== Mobile page background gradient: top-right to bottom-left ===== */
    @media (max-width: 640px) {
      html {
        background-color: #eef7fc !important;
        background-image: linear-gradient(to bottom left,
          #cfeeff 0%,
          #def3ff 28%,
          #edf9ff 58%,
          #f9fcff 100%) !important;
        background-size: 100vw 100vh !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
      }
      body,
      body.top100-mode {
        min-height: 100vh !important;
        color-scheme: only light !important;
        background-color: transparent !important;
        background-image: linear-gradient(to bottom left,
          rgba(196, 233, 253, .88) 0%,
          rgba(222, 243, 255, .78) 30%,
          rgba(239, 249, 255, .70) 60%,
          rgba(250, 253, 255, .58) 100%) !important;
        background-size: 100vw 100vh !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
      }
    }
'''

if old not in text:
    raise SystemExit('mobile gradient block not found')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
