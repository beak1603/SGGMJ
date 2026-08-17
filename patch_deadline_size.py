from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '\n</style>'
css = '''\n\n    /* Larger application deadline countdown */\n    .deadline-countdown {\n      padding: 12px 16px !important;\n      gap: 10px !important;\n    }\n    .deadline-countdown .deadline-label {\n      font-size: 13px !important;\n    }\n    .deadline-countdown strong {\n      font-size: 24px !important;\n    }\n    .deadline-countdown .deadline-date {\n      font-size: 12px !important;\n    }\n    @media (max-width: 640px) {\n      .deadline-countdown {\n        padding: 9px 11px !important;\n        gap: 6px 8px !important;\n      }\n      .deadline-countdown .deadline-label {\n        font-size: 10px !important;\n      }\n      .deadline-countdown strong {\n        font-size: 18px !important;\n      }\n      .deadline-countdown .deadline-date {\n        font-size: 9px !important;\n      }\n    }\n'''
if '/* Larger application deadline countdown */' not in text:
    text = text.replace(marker, css + marker, 1)
p.write_text(text, encoding='utf-8')
