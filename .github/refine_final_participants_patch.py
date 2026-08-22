from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

replacements = {
    'rgba(255, 250, 226, .98)': 'rgba(255, 253, 246, .92)',
    'rgba(255, 239, 177, .96)': 'rgba(252, 246, 226, .88)',
    'rgba(255, 214, 102, .84)': 'rgba(247, 235, 200, .82)',
    'rgba(255, 236, 168, .95)': 'rgba(252, 246, 226, .88)',
    'rgba(255, 249, 222, .98)': 'rgba(255, 253, 246, .92)',
    'inset 4px 0 0 rgba(190, 132, 16, .52)': 'inset 3px 0 0 rgba(184, 145, 55, .34)',
    '0 4px 14px rgba(181, 132, 26, .10)': '0 2px 8px rgba(145, 111, 38, .045)',
    'rgba(255, 247, 211, 1)': 'rgba(255, 252, 241, .96)',
    'rgba(255, 232, 154, .99)': 'rgba(250, 242, 217, .92)',
    'rgba(255, 203, 73, .90)': 'rgba(244, 228, 187, .86)',
    'rgba(255, 229, 143, .98)': 'rgba(250, 242, 217, .92)',
    'rgba(255, 246, 207, 1)': 'rgba(255, 252, 241, .96)',
    '#6e4a00': '#5f5234',
    '#775000': '#6a5932',
    'rgba(205, 158, 46, .56)': 'rgba(193, 162, 91, .32)',
    '#d98518': '#bd8b35',
    'inset 3px 0 0 rgba(190,132,16,.48)': 'inset 2px 0 0 rgba(184,145,55,.30)',
    '0 2px 8px rgba(181,132,26,.08)': '0 1px 5px rgba(145,111,38,.04)'
}
for old, new in replacements.items():
    if old in s:
        s = s.replace(old, new, 1)

old_js = '''    function applyFeaturedBroadcasterHighlights() {
      document.querySelectorAll('.rank-row, .unknown-row').forEach((row) => {
        const nickname = row.querySelector('.name-link')?.textContent?.trim() || '';
        row.classList.toggle('featured-broadcaster', FEATURED_BROADCASTERS.has(nickname));
      });
    }
'''

new_js = r'''    function normalizeBroadcasterName(value) {
      return String(value || '')
        .normalize('NFKC')
        .toLocaleLowerCase('ko')
        .replace(/[^0-9a-zA-Z가-힣]/g, '');
    }

    function broadcasterEditDistance(a, b) {
      if (a === b) return 0;
      if (!a.length) return b.length;
      if (!b.length) return a.length;
      const prev = Array.from({ length: b.length + 1 }, (_, i) => i);
      const curr = new Array(b.length + 1);
      for (let i = 1; i <= a.length; i++) {
        curr[0] = i;
        for (let j = 1; j <= b.length; j++) {
          const cost = a[i - 1] === b[j - 1] ? 0 : 1;
          curr[j] = Math.min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost);
        }
        for (let j = 0; j <= b.length; j++) prev[j] = curr[j];
      }
      return prev[b.length];
    }

    const NORMALIZED_FEATURED_BROADCASTERS = [...FEATURED_BROADCASTERS]
      .map(normalizeBroadcasterName)
      .filter(Boolean);

    function isFeaturedBroadcasterName(nickname) {
      const target = normalizeBroadcasterName(nickname);
      if (!target) return false;

      return NORMALIZED_FEATURED_BROADCASTERS.some((candidate) => {
        if (target === candidate) return true;

        const shorter = target.length <= candidate.length ? target : candidate;
        const longer = target.length > candidate.length ? target : candidate;
        const lengthGap = longer.length - shorter.length;

        if (
          shorter.length >= 3 &&
          longer.includes(shorter) &&
          lengthGap <= Math.max(3, Math.floor(longer.length * 0.35))
        ) return true;

        if (shorter.length < 3) return false;
        const maxDistance = longer.length >= 7 ? 2 : 1;
        return broadcasterEditDistance(target, candidate) <= maxDistance;
      });
    }

    function applyFeaturedBroadcasterHighlights() {
      document.querySelectorAll('.rank-row, .unknown-row').forEach((row) => {
        const nickname = row.querySelector('.name-link')?.textContent?.trim() || '';
        row.classList.toggle('featured-broadcaster', isFeaturedBroadcasterName(nickname));
      });
    }
'''

if old_js in s:
    s = s.replace(old_js, new_js, 1)
elif 'function isFeaturedBroadcasterName(nickname)' not in s:
    raise SystemExit('featured broadcaster matching block not found')

p.write_text(s, encoding='utf-8')
