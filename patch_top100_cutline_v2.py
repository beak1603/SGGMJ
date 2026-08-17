from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

# 1) TOP100 must be an exact headcount rather than tie-inclusive competition rank.
old = '''    function takeTopRanks(items, limit = 100) {
      if (!state.top10) return [...items].sort(compareRankItems);
      return rankedItems(items).filter(x => x.rank <= limit).map(x => x.item);
    }
'''
new = '''    function takeTopRanks(items, limit = 100) {
      const sorted = [...items].sort(compareRankItems);
      if (!state.top10) return sorted;
      return sorted.slice(0, limit);
    }
'''
if old not in text:
    raise SystemExit('takeTopRanks anchor not found')
text = text.replace(old, new, 1)

# 2) In overall TOP100 view, keep applicants below #100 visible and separate them with a cutoff bar.
old = '''      const visible = isSearch && state.top10
        ? [...items].filter(item => (rankMap.get(itemKey(item)) || Infinity) <= 100).sort(compareRankItems)
        : takeTopRanks(items);
      const displayCount = state.top10 ? visible.length : totalCount;
'''
new = '''      const visible = isSearch && state.top10
        ? [...items].filter(item => (rankMap.get(itemKey(item)) || Infinity) <= 100).sort(compareRankItems)
        : (state.top10 && scope === 'overall' ? [...items].sort(compareRankItems) : takeTopRanks(items));
      const displayCount = state.top10
        ? (scope === 'overall' ? Math.min(100, totalCount) : Math.min(100, visible.length))
        : totalCount;
'''
if old not in text:
    raise SystemExit('board visible/displayCount anchor not found')
text = text.replace(old, new, 1)

# 3) Cutoff position is based on exact selected headcount, not tie rank.
old = '''      const lastCutoffIndex = cutoffRank > 0 ? rankedVisible.reduce((last, entry, index) => entry.rank <= cutoffRank ? index : last, -1) : -1;
'''
new = '''      const lastCutoffIndex = cutoffRank > 0 && rankedVisible.length
        ? Math.min(cutoffRank, rankedVisible.length) - 1
        : -1;
'''
if old not in text:
    raise SystemExit('cutoff index anchor not found')
text = text.replace(old, new, 1)

# 4) Simplify cutoff label copy.
old = '''          ? `<div class=\"top100-cutoff-label\" aria-label=\"100명 기준 컷트라인\"><span>100명 기준 컷트라인</span></div>`
'''
new = '''          ? `<div class=\"top100-cutoff-label\" aria-label=\"커트라인\"><span>커트라인</span></div>`
'''
if old not in text:
    raise SystemExit('cutoff label anchor not found')
text = text.replace(old, new, 1)

# 5) Overall board also receives an exact 100-person cutoff when TOP100 is active.
old = '''        contentEl.innerHTML = `<div class=\"single\">${boardHtml('전체 신청자', tagged.sort(compareRankItems), state.query ? '검색 결과가 없습니다.' : '신청 댓글이 없습니다.', '', 'overall')}</div>${unknownBoard}`;
'''
new = '''        const overallCutoff = state.top10 && !state.query.trim() ? 100 : 0;
        contentEl.innerHTML = `<div class=\"single\">${boardHtml('전체 신청자', tagged.sort(compareRankItems), state.query ? '검색 결과가 없습니다.' : '신청 댓글이 없습니다.', '', 'overall', overallCutoff)}</div>${unknownBoard}`;
'''
if old not in text:
    raise SystemExit('overall board anchor not found')
text = text.replace(old, new, 1)

# 6) Override old orange/two-part cutoff styling with one solid red bar carrying white text.
marker = '\n</style>'
css = r'''

    /* ===== TOP100 exact headcount + single red cutoff bar ===== */
    .rank-row.top100-cutoff-row,
    .female-board .rank-row.top100-cutoff-row,
    .male-board .rank-row.top100-cutoff-row {
      box-shadow: none !important;
    }
    .top100-cutoff-label,
    .female-board .top100-cutoff-label,
    .male-board .top100-cutoff-label {
      width: 100% !important;
      height: 20px !important;
      min-height: 20px !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      border: 0 !important;
      border-radius: 0 !important;
      background: #e23b3b !important;
      background-image: none !important;
      box-shadow: none !important;
      color: #fff !important;
      font-size: 10px !important;
      font-weight: 900 !important;
      line-height: 1 !important;
      letter-spacing: .025em !important;
      text-align: center !important;
      user-select: none !important;
      pointer-events: none !important;
    }
    .top100-cutoff-label span {
      color: #fff !important;
      background: transparent !important;
      border: 0 !important;
      padding: 0 !important;
      line-height: 1 !important;
    }
    @media (max-width: 640px) {
      .top100-cutoff-label,
      .female-board .top100-cutoff-label,
      .male-board .top100-cutoff-label {
        height: 17px !important;
        min-height: 17px !important;
        font-size: 8px !important;
      }
    }
'''
if '/* ===== TOP100 exact headcount + single red cutoff bar ===== */' not in text:
    text = text.replace(marker, css + marker, 1)

p.write_text(text, encoding='utf-8')
