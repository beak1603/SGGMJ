from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = '8/25(금) 20시'
new = '8/25(화) 20시'
if old not in s:
    raise SystemExit('schedule text not found')
s = s.replace(old, new)
p.write_text(s, encoding='utf-8')
