from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

replacements = [
    ('''<button id="top10Toggle" class="view-btn" type="button" aria-pressed="false">TOP 100</button>''',
     '''<button id="top10Toggle" class="view-btn" type="button" aria-pressed="false">TOP 99</button>'''),
    ('''function takeTopRanks(items, limit = 100)''', '''function takeTopRanks(items, limit = 99)'''),
    ('''<= 100).sort(compareRankItems)''', '''<= 99).sort(compareRankItems)'''),
    ('''${state.top10 ? 'TOP 100 · ' : ''}좋아요순''', '''${state.top10 ? 'TOP 99 · ' : ''}좋아요순'''),
    ('''// TOP 100 selection guideline: aim for 50 men + 50 women.\n      // If there are fewer than 50 male applicants, the shortage is added to the female cutoff.\n      const maleTop100Cutoff = Math.min(50, fullMaleCount);\n      const femaleTop100Cutoff = Math.min(100, 100 - maleTop100Cutoff);\n      const showGenderCutoff = state.top10 && state.splitGender && !state.query.trim();''',
     '''// TOP 99 selection guideline: aim for up to 50 men, with the remaining slots assigned to women.\n      // If there are fewer than 50 male applicants, the shortage is added to the female cutoff.\n      const maleTop99Cutoff = Math.min(50, fullMaleCount);\n      const femaleTop99Cutoff = Math.min(99, 99 - maleTop99Cutoff);\n      const showGenderCutoff = state.top10 && state.splitGender && !state.query.trim();'''),
    ('''showGenderCutoff ? femaleTop100Cutoff : 0''', '''showGenderCutoff ? femaleTop99Cutoff : 0'''),
    ('''showGenderCutoff ? maleTop100Cutoff : 0''', '''showGenderCutoff ? maleTop99Cutoff : 0'''),
    ('''const overallCutoff = state.top10 && !state.query.trim() ? 100 : 0;''', '''const overallCutoff = state.top10 && !state.query.trim() ? 99 : 0;'''),
    ('''top10Toggle.textContent = state.top10 ? 'TOP 100 ON' : 'TOP 100';''', '''top10Toggle.textContent = state.top10 ? 'TOP 99 ON' : 'TOP 99';'''),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f'anchor not found: {old[:80]}')
    text = text.replace(old, new)

# Cosmetic comments only.
text = text.replace('TOP 100 keeps the normal page background.', 'TOP 99 keeps the normal page background.')
text = text.replace('Soft gradient pills behind 좋아요순 / TOP 100', 'Soft gradient pills behind 좋아요순 / TOP 99')
text = text.replace('TOP 100 gender quota cutoff', 'TOP 99 gender quota cutoff')
text = text.replace('TOP 100 cutoff explanation row', 'TOP 99 cutoff explanation row')
text = text.replace('TOP100 exact headcount + single red cutoff bar', 'TOP99 cutoff + single red cutoff bar')
text = text.replace('TOP100 full-list behavior + larger cutoff label', 'TOP99 full-list behavior + larger cutoff label')

p.write_text(text, encoding='utf-8')
