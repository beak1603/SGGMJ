from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = "      $('#totalCount').textContent = (state.top10 ? Math.min(100, state.comments.length) : state.comments.length).toLocaleString();\n"
new = "      $('#totalCount').textContent = state.comments.length.toLocaleString();\n"
if old not in text:
    raise SystemExit('total count anchor not found')
text = text.replace(old, new, 1)

old = '''      const visible = isSearch && state.top10
        ? [...items].filter(item => (rankMap.get(itemKey(item)) || Infinity) <= 100).sort(compareRankItems)
        : (state.top10 && scope === 'overall' ? [...items].sort(compareRankItems) : takeTopRanks(items));
      const displayCount = state.top10
        ? (scope === 'overall' ? Math.min(100, totalCount) : Math.min(100, visible.length))
        : totalCount;
'''
new = '''      const visible = isSearch && state.top10
        ? [...items].filter(item => (rankMap.get(itemKey(item)) || Infinity) <= 100).sort(compareRankItems)
        : [...items].sort(compareRankItems);
      const displayCount = totalCount;
'''
if old not in text:
    raise SystemExit('board visibility anchor not found')
text = text.replace(old, new, 1)

# Make the solid red cutoff bar and its label easier to read on both desktop and mobile.
old = '''      height: 20px !important;
      min-height: 20px !important;'''
new = '''      height: 26px !important;
      min-height: 26px !important;'''
if old not in text:
    raise SystemExit('cutoff desktop height anchor not found')
text = text.replace(old, new, 1)

old = '''      font-size: 10px !important;
      font-weight: 900 !important;
      line-height: 1 !important;
      letter-spacing: .025em !important;'''
new = '''      font-size: 13px !important;
      font-weight: 950 !important;
      line-height: 1 !important;
      letter-spacing: .02em !important;'''
if old not in text:
    raise SystemExit('cutoff desktop font anchor not found')
text = text.replace(old, new, 1)

old = '''        height: 17px !important;
        min-height: 17px !important;
        font-size: 8px !important;'''
new = '''        height: 23px !important;
        min-height: 23px !important;
        font-size: 11px !important;'''
if old not in text:
    raise SystemExit('cutoff mobile anchor not found')
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
