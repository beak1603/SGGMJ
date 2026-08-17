from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
old = "0f65f55c87c47704194741c1dd4aa83401188ffea90cd881e0733059481dcdba"
new = "72a19e5761d3dbe392b2105d4a461de051cdf59e89c6d9321e277c7a641dfffd"
if old not in text:
    raise SystemExit('old admin hash not found')
text = text.replace(old, new)
p.write_text(text, encoding='utf-8')
