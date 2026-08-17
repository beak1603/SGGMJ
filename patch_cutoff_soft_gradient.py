from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''      background: linear-gradient(135deg, #a93631 0%, #c84a40 48%, #b23a34 100%) !important;\n      background-image: linear-gradient(135deg, #a93631 0%, #c84a40 48%, #b23a34 100%) !important;\n      box-shadow:\n        inset 0 1px 0 rgba(255,255,255,.16),\n        0 2px 7px rgba(126, 35, 31, .14) !important;'''

new = '''      background: linear-gradient(90deg, #b65b54 0%, #c66a61 28%, #cf756b 50%, #c66a61 72%, #b65b54 100%) !important;\n      background-image: linear-gradient(90deg, #b65b54 0%, #c66a61 28%, #cf756b 50%, #c66a61 72%, #b65b54 100%) !important;\n      box-shadow:\n        inset 0 1px 0 rgba(255,255,255,.12),\n        0 1px 5px rgba(117, 48, 43, .09) !important;'''

if old not in text:
    raise SystemExit('soft cutoff gradient anchor not found')

text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
