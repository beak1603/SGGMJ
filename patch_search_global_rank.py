from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = '''    function rankedItems(items) {
      const sorted = [...items].sort(compareRankItems);
      let lastLikes = null;
      let lastRank = 0;
      return sorted.map((item, index) => {
        const rank = index === 0 || item.likes !== lastLikes ? index + 1 : lastRank;
        lastLikes = item.likes;
        lastRank = rank;
        return { item, rank };
      });
    }

    function takeTopRanks(items, limit = 100) {'''
new = '''    function rankedItems(items) {
      const sorted = [...items].sort(compareRankItems);
      let lastLikes = null;
      let lastRank = 0;
      return sorted.map((item, index) => {
        const rank = index === 0 || item.likes !== lastLikes ? index + 1 : lastRank;
        lastLikes = item.likes;
        lastRank = rank;
        return { item, rank };
      });
    }

    function fullRankMap(scope = 'overall') {
      const tagged = state.comments.map(x => ({ ...x, gender: classifyGender(x) }));
      let source = tagged;
      if (scope === 'female') source = tagged.filter(x => x.gender === 'female');
      else if (scope === 'male') source = tagged.filter(x => x.gender === 'male');
      else if (scope === 'unknown') source = tagged.filter(x => x.gender === 'unknown');

      const map = new Map();
      for (const { item, rank } of rankedItems(source)) map.set(itemKey(item), rank);
      return map;
    }

    function takeTopRanks(items, limit = 100) {'''
if old not in text:
    raise SystemExit('rankedItems anchor not found')
text = text.replace(old, new, 1)

old = '''    function unknownBoardHtml(items, emptyMessage) {
      const totalCount = items.length;
      const visible = takeTopRanks(items);
      const rows = visible.length ? rankedItems(visible).map(({ item, rank }) => unknownRowHtml(item, rank)).join('') : `<div class="empty">${esc(emptyMessage)}</div>`;
      const manualCount = state.comments.filter(isManualGender).length;'''
new = '''    function unknownBoardHtml(items, emptyMessage) {
      const totalCount = items.length;
      const isSearch = Boolean(state.query.trim());
      const rankMap = isSearch ? fullRankMap('unknown') : null;
      const visible = isSearch && state.top10
        ? [...items].filter(item => (rankMap.get(itemKey(item)) || Infinity) <= 100).sort(compareRankItems)
        : takeTopRanks(items);
      const rankedVisible = isSearch
        ? [...visible].sort(compareRankItems).map(item => ({ item, rank: rankMap.get(itemKey(item)) || 0 }))
        : rankedItems(visible);
      const rows = rankedVisible.length ? rankedVisible.map(({ item, rank }) => unknownRowHtml(item, rank)).join('') : `<div class="empty">${esc(emptyMessage)}</div>`;
      const manualCount = state.comments.filter(isManualGender).length;'''
if old not in text:
    raise SystemExit('unknownBoardHtml anchor not found')
text = text.replace(old, new, 1)

old = '''    function boardHtml(title, items, emptyMessage, genderDrop = '', scope = 'overall', cutoffRank = 0) {
      const totalCount = items.length;
      const visible = takeTopRanks(items);
      const displayCount = state.top10 ? Math.min(totalCount, 100) : totalCount;
      const genderClass = genderDrop === 'female' ? ' female-board' : genderDrop === 'male' ? ' male-board' : '';
      const dropAttrs = genderDrop ? ` data-gender-drop="${genderDrop}" class="board drop-zone${genderClass}"` : ' class="board"';
      const draggable = Boolean(genderDrop) && state.isAdmin;
      const rankedVisible = rankedItems(visible);'''
new = '''    function boardHtml(title, items, emptyMessage, genderDrop = '', scope = 'overall', cutoffRank = 0) {
      const totalCount = items.length;
      const isSearch = Boolean(state.query.trim());
      const rankMap = isSearch ? fullRankMap(scope) : null;
      const visible = isSearch && state.top10
        ? [...items].filter(item => (rankMap.get(itemKey(item)) || Infinity) <= 100).sort(compareRankItems)
        : takeTopRanks(items);
      const displayCount = state.top10 ? visible.length : totalCount;
      const genderClass = genderDrop === 'female' ? ' female-board' : genderDrop === 'male' ? ' male-board' : '';
      const dropAttrs = genderDrop ? ` data-gender-drop="${genderDrop}" class="board drop-zone${genderClass}"` : ' class="board"';
      const draggable = Boolean(genderDrop) && state.isAdmin;
      const rankedVisible = isSearch
        ? [...visible].sort(compareRankItems).map(item => ({ item, rank: rankMap.get(itemKey(item)) || 0 }))
        : rankedItems(visible);'''
if old not in text:
    raise SystemExit('boardHtml anchor not found')
text = text.replace(old, new, 1)

p.write_text(text, encoding='utf-8')
