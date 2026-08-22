from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = '''    .organizer-card {
      width: 100%;
      min-height: 78px;
      margin: 0 0 14px;
      padding: 12px 16px;
      display: grid;
      grid-template-columns: 50px minmax(0, 1fr) auto;
      align-items: center;
      gap: 13px;
      border: 1px solid rgba(185, 213, 230, .92);
      border-radius: 18px;
      background: linear-gradient(105deg, rgba(255,255,255,.96) 0%, rgba(247,252,255,.96) 58%, rgba(240,249,255,.94) 100%);
      box-shadow: 0 9px 26px rgba(44, 101, 134, .07);
      color: #243e51;
      text-decoration: none;
      transition: transform .16s ease, border-color .2s ease, box-shadow .2s ease;
    }
    .organizer-card:hover {
      transform: translateY(-1px);
      border-color: #aed4e8;
      box-shadow: 0 12px 30px rgba(44, 101, 134, .10);
    }'''

new = '''    .organizer-card {
      width: 100%;
      min-height: 78px;
      margin: 0 0 14px;
      padding: 12px 16px;
      display: grid;
      grid-template-columns: 50px minmax(0, 1fr) auto;
      align-items: center;
      gap: 13px;
      border: 1px solid rgba(137, 201, 236, .72);
      border-radius: 18px;
      background: linear-gradient(105deg, rgba(234,248,255,.98) 0%, rgba(209,239,255,.94) 52%, rgba(181,226,250,.90) 100%);
      box-shadow: 0 9px 26px rgba(44, 132, 181, .09);
      color: #243e51;
      text-decoration: none;
      transition: transform .16s ease, border-color .2s ease, box-shadow .2s ease;
    }
    .organizer-card:hover {
      transform: translateY(-1px);
      border-color: #78bee4;
      background: linear-gradient(105deg, rgba(226,245,255,.99) 0%, rgba(197,234,255,.96) 52%, rgba(164,218,248,.93) 100%);
      box-shadow: 0 12px 30px rgba(44, 132, 181, .13);
    }'''

if old not in s:
    raise SystemExit('organizer card style block not found')

s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
