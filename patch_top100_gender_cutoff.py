from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# Add a visual cutoff marker to the final selected row while keeping up to 100 visible per gender.
css = r'''

    /* ===== TOP 100 gender quota cutoff ===== */
    .rank-row.top100-cutoff-row {
      position: relative;
      box-shadow: inset 0 -3px 0 #e5a13a;
    }
    .female-board .rank-row.top100-cutoff-row {
      box-shadow: inset 0 -3px 0 #e8a13a;
    }
    .male-board .rank-row.top100-cutoff-row {
      box-shadow: inset 0 -3px 0 #e8a13a;
    }
    @media (max-width: 640px) {
      .rank-row.top100-cutoff-row,
      .female-board .rank-row.top100-cutoff-row,
      .male-board .rank-row.top100-cutoff-row {
        box-shadow: inset 0 -2px 0 #e5a13a;
      }
    }
'''
if '/* ===== TOP 100 gender quota cutoff ===== */' not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

old_sig = "    function rowHtml(item, rank, draggable = false, scope = 'overall') {"
new_sig = "    function rowHtml(item, rank, draggable = false, scope = 'overall', cutoffAfter = false) {"
if old_sig not in text:
    raise SystemExit('rowHtml signature not found')
text = text.replace(old_sig, new_sig, 1)

old_action = "      const actionClass = undo ? ' has-admin-action' : '';\n      return `<div class=\"rank-row${topClass}${actionClass}\"${dragAttrs} data-comment-url=\"${esc(commentUrl(item))}\" role=\"link\" tabindex=\"0\">"
new_action = "      const actionClass = undo ? ' has-admin-action' : '';\n      const cutoffClass = cutoffAfter ? ' top100-cutoff-row' : '';\n      return `<div class=\"rank-row${topClass}${actionClass}${cutoffClass}\"${dragAttrs} data-comment-url=\"${esc(commentUrl(item))}\" role=\"link\" tabindex=\"0\">"
if old_action not in text:
    raise SystemExit('rowHtml class target not found')
text = text.replace(old_action, new_action, 1)

old_board_sig = "    function boardHtml(title, items, emptyMessage, genderDrop = '', scope = 'overall') {"
new_board_sig = "    function boardHtml(title, items, emptyMessage, genderDrop = '', scope = 'overall', cutoffRank = 0) {"
if old_board_sig not in text:
    raise SystemExit('boardHtml signature not found')
text = text.replace(old_board_sig, new_board_sig, 1)

old_rows = "      const rows = visible.length ? rankedItems(visible).map(({ item, rank }) => rowHtml(item, rank, draggable, scope)).join('') : `<div class=\"empty\">${esc(emptyMessage)}</div>`;"
new_rows = "      const rankedVisible = rankedItems(visible);\n      const lastCutoffIndex = cutoffRank > 0 ? rankedVisible.reduce((last, entry, index) => entry.rank <= cutoffRank ? index : last, -1) : -1;\n      const rows = rankedVisible.length ? rankedVisible.map(({ item, rank }, index) => rowHtml(item, rank, draggable, scope, index === lastCutoffIndex)).join('') : `<div class=\"empty\">${esc(emptyMessage)}</div>`;"
if old_rows not in text:
    raise SystemExit('board rows target not found')
text = text.replace(old_rows, new_rows, 1)

old_full = "      const fullTagged = state.comments.map(x => ({...x, gender: classifyGender(x)}));\n      const fullUnknownCount = fullTagged.filter(x=>x.gender==='unknown').length;"
new_full = "      const fullTagged = state.comments.map(x => ({...x, gender: classifyGender(x)}));\n      const fullFemaleCount = fullTagged.filter(x=>x.gender==='female').length;\n      const fullMaleCount = fullTagged.filter(x=>x.gender==='male').length;\n      const fullUnknownCount = fullTagged.filter(x=>x.gender==='unknown').length;\n\n      // TOP 100 selection guideline: aim for 50 men + 50 women.\n      // If there are fewer than 50 male applicants, the shortage is added to the female cutoff.\n      const maleTop100Cutoff = Math.min(50, fullMaleCount);\n      const femaleTop100Cutoff = Math.min(100, 100 - maleTop100Cutoff);\n      const showGenderCutoff = state.top10 && state.splitGender && !state.query.trim();"
if old_full not in text:
    raise SystemExit('fullTagged target not found')
text = text.replace(old_full, new_full, 1)

text = text.replace("      $('#femaleCount').textContent = fullTagged.filter(x=>x.gender==='female').length.toLocaleString();", "      $('#femaleCount').textContent = fullFemaleCount.toLocaleString();", 1)
text = text.replace("      $('#maleCount').textContent = fullTagged.filter(x=>x.gender==='male').length.toLocaleString();", "      $('#maleCount').textContent = fullMaleCount.toLocaleString();", 1)

old_female_call = "          ${boardHtml('여자 신청자', female, state.query ? '검색 결과가 없습니다.' : '여자로 분류된 신청자가 없습니다.', 'female', 'female')}"
new_female_call = "          ${boardHtml('여자 신청자', female, state.query ? '검색 결과가 없습니다.' : '여자로 분류된 신청자가 없습니다.', 'female', 'female', showGenderCutoff ? femaleTop100Cutoff : 0)}"
if old_female_call not in text:
    raise SystemExit('female board call not found')
text = text.replace(old_female_call, new_female_call, 1)

old_male_call = "          ${boardHtml('남자 신청자', male, state.query ? '검색 결과가 없습니다.' : '남자로 분류된 신청자가 없습니다.', 'male', 'male')}"
new_male_call = "          ${boardHtml('남자 신청자', male, state.query ? '검색 결과가 없습니다.' : '남자로 분류된 신청자가 없습니다.', 'male', 'male', showGenderCutoff ? maleTop100Cutoff : 0)}"
if old_male_call not in text:
    raise SystemExit('male board call not found')
text = text.replace(old_male_call, new_male_call, 1)

p.write_text(text, encoding='utf-8')
