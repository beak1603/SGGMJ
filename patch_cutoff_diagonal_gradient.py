from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''      background: linear-gradient(90deg, #b65b54 0%, #c66a61 28%, #cf756b 50%, #c66a61 72%, #b65b54 100%) !important;\n      background-image: linear-gradient(90deg, #b65b54 0%, #c66a61 28%, #cf756b 50%, #c66a61 72%, #b65b54 100%) !important;\n      box-shadow:\n        inset 0 1px 0 rgba(255,255,255,.12),\n        0 1px 5px rgba(117, 48, 43, .09) !important;'''

new = '''      background: linear-gradient(135deg, #9f4742 0%, #ad514a 30%, #bd6056 64%, #c96d61 100%) !important;\n      background-image:\n        linear-gradient(180deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,0) 58%),\n        linear-gradient(135deg, #9f4742 0%, #ad514a 30%, #bd6056 64%, #c96d61 100%) !important;\n      box-shadow:\n        inset 0 1px 0 rgba(255,255,255,.10),\n        0 1px 4px rgba(112, 43, 39, .08) !important;'''

if old not in text:
    raise SystemExit('diagonal cutoff gradient anchor not found')

text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
