from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

needle = '''    const NORMALIZED_FEATURED_BROADCASTERS = [...FEATURED_BROADCASTERS]
      .map(normalizeBroadcasterName)
      .filter(Boolean);

    function isFeaturedBroadcasterName(nickname) {
      const target = normalizeBroadcasterName(nickname);
      if (!target) return false;
'''
replacement = '''    const NORMALIZED_FEATURED_BROADCASTERS = [...FEATURED_BROADCASTERS]
      .map(normalizeBroadcasterName)
      .filter(Boolean);
    const EXCLUDED_FEATURED_BROADCASTERS = new Set([
      normalizeBroadcasterName('춘빵이'),
      normalizeBroadcasterName('김먕이'),
      normalizeBroadcasterName('세이지')
    ]);

    function isFeaturedBroadcasterName(nickname) {
      const target = normalizeBroadcasterName(nickname);
      if (!target || EXCLUDED_FEATURED_BROADCASTERS.has(target)) return false;
'''

if needle not in s:
    raise SystemExit('featured matching insertion point not found')
s = s.replace(needle, replacement, 1)

p.write_text(s, encoding='utf-8')
