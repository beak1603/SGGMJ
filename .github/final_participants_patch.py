from pathlib import Path
import json

p = Path('index.html')
s = p.read_text(encoding='utf-8')

names = [
    '강드-','강주이','광수야.','길앞잡이광수','김메이','김뱅글:Þ','김부각º','깅도일','깡담비','깨박이깨박이',
    '꼬부기07.','꼼모리','꿈틀__','난워니-_-+','냐쵸♥','냥쏘','니즈__','델라리','도깨비루딘','도이지',
    '땡글땡글포포','뜨사.','라벤_','릉빵이','리르','리리하','마또','마이곰이','매그피이','묭씨',
    '박나닝','박사장','방랑검객강풍','방진구','버터우스3세','부바','블랙워크','비즈니스킴-','빈스','빡룡',
    '뽀린걸','샤르망','샤키_','솔롱고스','수셈이','숙봉이','시몽','시트리','신루_','아야네_세나',
    '야구자','양도끼','양지랖','어둠우주기사','연토리뿡치','연푸_','오구','오그림','오따식','오정제',
    '요한.3.','우앵두','윤견','이지상:)','이학일.','재수피기','제갈_통','제로!','제이404','주드',
    '쥐쥐.','쪼이.','차승원_','촌장_고봉','최또','최애리','춘봉_','치유+','치즈치즈♪','치카:3',
    '카노ミ☆','코렛트','코코미짱','코코양','클라비스','토끼예나','파니_','프트9','하루아_','하율옹',
    '한결___','항상#킴성태','헤다ㆍ','후룽카카','히루','힌콕','힙비','EscA_에스카','S.드라구노프'
]

css_marker = '/* ===== Final participant broadcaster highlight ===== */'
if css_marker not in s:
    css = r'''

    /* ===== Final participant broadcaster highlight ===== */
    .rank-row.featured-broadcaster,
    .unknown-row.featured-broadcaster {
      background:
        linear-gradient(90deg,
          rgba(255, 250, 226, .98) 0%,
          rgba(255, 239, 177, .96) 28%,
          rgba(255, 214, 102, .84) 52%,
          rgba(255, 236, 168, .95) 76%,
          rgba(255, 249, 222, .98) 100%) !important;
      box-shadow:
        inset 4px 0 0 rgba(190, 132, 16, .52),
        inset 0 1px 0 rgba(255,255,255,.58),
        0 4px 14px rgba(181, 132, 26, .10) !important;
    }
    .rank-row.featured-broadcaster:hover,
    .unknown-row.featured-broadcaster:hover {
      background:
        linear-gradient(90deg,
          rgba(255, 247, 211, 1) 0%,
          rgba(255, 232, 154, .99) 28%,
          rgba(255, 203, 73, .90) 52%,
          rgba(255, 229, 143, .98) 76%,
          rgba(255, 246, 207, 1) 100%) !important;
    }
    .rank-row.featured-broadcaster .name-link,
    .unknown-row.featured-broadcaster .name-link {
      color: #6e4a00 !important;
      font-weight: 950 !important;
    }
    .rank-row.featured-broadcaster .likes,
    .unknown-row.featured-broadcaster .likes {
      color: #775000 !important;
      border-color: rgba(205, 158, 46, .56) !important;
      background: rgba(255,255,255,.63) !important;
    }
    .rank-row.featured-broadcaster .heart,
    .unknown-row.featured-broadcaster .heart {
      color: #d98518 !important;
    }

    /* Final announcement replaces the expired deadline UI. */
    .deadline-countdown.final-announcement,
    .deadline-countdown.is-warning.final-announcement,
    .deadline-countdown.is-urgent.final-announcement,
    .deadline-countdown.is-closed.final-announcement,
    .deadline-countdown.is-complete.final-announcement {
      position: absolute !important;
      top: 8px !important;
      right: 0 !important;
      width: fit-content !important;
      max-width: min(470px, 56%) !important;
      margin: 0 !important;
      padding: 0 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: flex-end !important;
      border: 0 !important;
      border-radius: 0 !important;
      background: transparent !important;
      background-image: none !important;
      box-shadow: none !important;
      text-align: right !important;
    }
    .deadline-countdown.final-announcement .deadline-final-title {
      color: #1d9b4b !important;
      font-size: 31px !important;
      line-height: 1.12 !important;
      font-weight: 950 !important;
      letter-spacing: -.03em !important;
      white-space: nowrap !important;
      text-shadow: 0 2px 10px rgba(29,155,75,.11) !important;
    }
    @media (max-width: 640px) {
      .rank-row.featured-broadcaster,
      .unknown-row.featured-broadcaster {
        box-shadow:
          inset 3px 0 0 rgba(190,132,16,.48),
          0 2px 8px rgba(181,132,26,.08) !important;
      }
      .deadline-countdown.final-announcement,
      .deadline-countdown.is-warning.final-announcement,
      .deadline-countdown.is-urgent.final-announcement,
      .deadline-countdown.is-closed.final-announcement,
      .deadline-countdown.is-complete.final-announcement {
        position: static !important;
        max-width: 100% !important;
        margin: -4px 0 14px auto !important;
      }
      .deadline-countdown.final-announcement .deadline-final-title {
        font-size: 22px !important;
        white-space: normal !important;
      }
    }
'''
    if '</style>' not in s:
        raise SystemExit('style closing tag not found')
    s = s.replace('</style>', css + '\n</style>', 1)

html_start = s.find('      <div id="deadlineCountdown"')
if html_start < 0:
    raise SystemExit('deadlineCountdown HTML not found')
html_end = s.find('      </div>', html_start)
if html_end < 0:
    raise SystemExit('deadlineCountdown closing div not found')
html_end += len('      </div>')
final_html = '''      <div id="deadlineCountdown" class="deadline-countdown final-announcement" role="status" aria-live="polite">
        <strong class="deadline-final-title">최종 참가자가 발표되었습니다!</strong>
      </div>'''
s = s[:html_start] + final_html + s[html_end:]

fn_start = s.find('    function updateDeadlineCountdown() {')
fn_end = s.find('\n    function loadAdminSession()', fn_start)
if fn_start < 0 or fn_end < 0:
    raise SystemExit('deadline countdown function boundaries not found')
final_fn = '''    function updateDeadlineCountdown() {
      const box = $('#deadlineCountdown');
      if (!box) return;
      box.className = 'deadline-countdown final-announcement';
      box.innerHTML = '<strong class="deadline-final-title">최종 참가자가 발표되었습니다!</strong>';
    }
'''
s = s[:fn_start] + final_fn + s[fn_end:]

js_marker = 'const FEATURED_BROADCASTERS = new Set('
if js_marker not in s:
    needle = "    const contentEl = $('#content');\n"
    if needle not in s:
        raise SystemExit('contentEl declaration not found')
    names_json = json.dumps(names, ensure_ascii=False)
    js = f'''    const contentEl = $('#content');
    const FEATURED_BROADCASTERS = new Set({names_json});

    function applyFeaturedBroadcasterHighlights() {{
      document.querySelectorAll('.rank-row, .unknown-row').forEach((row) => {{
        const nickname = row.querySelector('.name-link')?.textContent?.trim() || '';
        row.classList.toggle('featured-broadcaster', FEATURED_BROADCASTERS.has(nickname));
      }});
    }}

    const featuredBroadcasterObserver = new MutationObserver(() => applyFeaturedBroadcasterHighlights());
    featuredBroadcasterObserver.observe(contentEl, {{ childList: true, subtree: true }});
'''
    s = s.replace(needle, js, 1)

s = s.replace('합격자 발표는 22일(오늘) 예정입니다', '')
s = s.replace('신청이 마감되었습니다!', '')

p.write_text(s, encoding='utf-8')
