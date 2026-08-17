from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''    function badgeHtml(item) {
      const key = itemKey(item);
      const dragged = state.newDraggedApplicants.has(key) ? `<span class="new-badge">NEW!</span>` : '';
      const fresh = state.newApplicants.has(key) ? `<span class="fresh-badge">신규</span>` : '';
      return dragged + fresh;
    }
'''
new = '''    function badgeHtml(item) {
      const key = itemKey(item);
      const sharedNew = manualGenderKeys(item).some(k => state.sharedNewApplicants.has(k));
      const dragged = (state.newDraggedApplicants.has(key) || sharedNew) ? `<span class="new-badge">NEW!</span>` : '';
      const fresh = state.newApplicants.has(key) ? `<span class="fresh-badge">신규</span>` : '';
      return dragged + fresh;
    }
'''

if old not in text:
    raise SystemExit('badgeHtml target not found')

text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
