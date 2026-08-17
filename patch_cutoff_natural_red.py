from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''      border: 0 !important;\n      border-radius: 0 !important;\n      background: #e23b3b !important;\n      background-image: none !important;\n      box-shadow: none !important;\n      color: #fff !important;'''
new = '''      border: 0 !important;\n      border-radius: 0 !important;\n      background: linear-gradient(135deg, #a93631 0%, #c84a40 48%, #b23a34 100%) !important;\n      background-image: linear-gradient(135deg, #a93631 0%, #c84a40 48%, #b23a34 100%) !important;\n      box-shadow:\n        inset 0 1px 0 rgba(255,255,255,.16),\n        0 2px 7px rgba(126, 35, 31, .14) !important;\n      color: #fff !important;'''

if old not in text:
    raise SystemExit('cutoff color anchor not found')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
