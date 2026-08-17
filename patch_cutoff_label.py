from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

old = """      const rows = rankedVisible.length ? rankedVisible.map(({ item, rank }, index) => rowHtml(item, rank, draggable, scope, index === lastCutoffIndex)).join('') : `<div class=\"empty\">${esc(emptyMessage)}</div>`;"""
new = """      const rows = rankedVisible.length ? rankedVisible.map(({ item, rank }, index) => {
        const row = rowHtml(item, rank, draggable, scope, index === lastCutoffIndex);
        const cutoffLabel = index === lastCutoffIndex
          ? `<div class=\"top100-cutoff-label\" aria-label=\"100명 기준 컷트라인\"><span>100명 기준 컷트라인</span></div>`
          : '';
        return row + cutoffLabel;
      }).join('') : `<div class=\"empty\">${esc(emptyMessage)}</div>`;"""

if old not in text:
    raise SystemExit('cutoff rows target not found')
text = text.replace(old, new, 1)

css = r'''

    /* TOP 100 cutoff explanation row */
    .top100-cutoff-label {
      height: 34px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 12px;
      border-bottom: 1px solid rgba(221, 231, 237, .9);
      background: #fffaf1;
      color: #9b6b23;
      font-size: 11px;
      font-weight: 900;
      letter-spacing: -.01em;
      text-align: center;
      user-select: none;
      pointer-events: none;
    }
    .female-board .top100-cutoff-label {
      background: #fff9f2;
      border-top: 1px solid rgba(232, 161, 58, .28);
    }
    .male-board .top100-cutoff-label {
      background: #fff9f2;
      border-top: 1px solid rgba(232, 161, 58, .28);
    }
    @media (max-width: 640px) {
      .top100-cutoff-label {
        height: 28px;
        padding: 0 4px;
        font-size: 8px;
        white-space: nowrap;
      }
    }
'''

marker = '    /* ===== Dark-mode forced-vignette prevention ===== */'
if '/* TOP 100 cutoff explanation row */' not in text:
    if marker not in text:
        raise SystemExit('CSS insert marker not found')
    text = text.replace(marker, css + '\n' + marker, 1)

p.write_text(text, encoding='utf-8')
