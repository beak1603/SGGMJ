from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
old="      $('#totalCount').textContent = state.comments.length.toLocaleString();\n"
new="      $('#totalCount').textContent = (state.top10 ? Math.min(100, state.comments.length) : state.comments.length).toLocaleString();\n"
if old not in text:
    raise SystemExit('totalCount anchor not found')
text=text.replace(old,new,1)
p.write_text(text,encoding='utf-8')
