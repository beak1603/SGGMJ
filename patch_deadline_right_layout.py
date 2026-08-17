from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
marker = '\n</style>'
css = r'''

    /* ===== Deadline countdown: right aligned, borderless, two lines ===== */
    @media (min-width: 641px) {
      .site-title {
        padding-right: 360px !important;
      }
    }
    .deadline-countdown,
    .deadline-countdown.is-warning,
    .deadline-countdown.is-urgent,
    .deadline-countdown.is-closed {
      position: absolute !important;
      top: 8px !important;
      right: 0 !important;
      width: fit-content !important;
      max-width: min(360px, 46%) !important;
      margin: 0 !important;
      padding: 0 !important;
      display: grid !important;
      grid-template-columns: auto auto !important;
      grid-template-areas:
        "label time"
        "date date" !important;
      align-items: baseline !important;
      justify-content: end !important;
      column-gap: 10px !important;
      row-gap: 3px !important;
      border: 0 !important;
      border-radius: 0 !important;
      background: transparent !important;
      background-image: none !important;
      box-shadow: none !important;
    }
    .deadline-countdown .deadline-label {
      grid-area: label !important;
      align-self: baseline !important;
      white-space: nowrap !important;
    }
    .deadline-countdown strong {
      grid-area: time !important;
      justify-self: end !important;
      white-space: nowrap !important;
    }
    .deadline-countdown .deadline-date {
      grid-area: date !important;
      justify-self: end !important;
      white-space: nowrap !important;
      text-align: right !important;
    }

    @media (max-width: 640px) {
      .deadline-countdown,
      .deadline-countdown.is-warning,
      .deadline-countdown.is-urgent,
      .deadline-countdown.is-closed {
        position: static !important;
        max-width: 100% !important;
        margin: -4px 0 14px auto !important;
        padding: 0 !important;
        column-gap: 7px !important;
        row-gap: 2px !important;
      }
    }
'''
if '/* ===== Deadline countdown: right aligned, borderless, two lines ===== */' not in text:
    text = text.replace(marker, css + marker, 1)
p.write_text(text, encoding='utf-8')
