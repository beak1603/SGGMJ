from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''      <h1 class="site-title" aria-label="스까묵자 배그 신청자 랭킹">
        <strong>스까묵자</strong><span> 배그 신청자 랭킹</span>
      </h1>'''
new = '''      <h1 class="site-title logo-title" aria-label="스까묵자 배그">
        <img class="site-title-logo" src="assets/sgmj-title.png" alt="스까묵자 배그" />
      </h1>'''

if old not in text:
    raise SystemExit('title block not found')
text = text.replace(old, new, 1)

marker = '\n</style>'
css = r'''

    /* ===== Generated SGMJ brush logo title ===== */
    .site-title.logo-title {
      margin: -2px 0 14px !important;
      padding: 0 !important;
      width: min(540px, calc(100% - 380px)) !important;
      max-width: 100% !important;
      display: block !important;
      line-height: 0 !important;
      background: transparent !important;
    }
    .site-title.logo-title::before,
    .site-title.logo-title::after {
      display: none !important;
      content: none !important;
    }
    .site-title-logo {
      display: block !important;
      width: 100% !important;
      height: auto !important;
      max-width: 100% !important;
      object-fit: contain !important;
      user-select: none !important;
      -webkit-user-drag: none !important;
      filter: none !important;
    }
    @media (max-width: 640px) {
      .site-title.logo-title {
        width: min(92vw, 390px) !important;
        margin: 0 0 12px !important;
      }
    }
'''

if '/* ===== Generated SGMJ brush logo title ===== */' not in text:
    text = text.replace(marker, css + marker, 1)

p.write_text(text, encoding='utf-8')
