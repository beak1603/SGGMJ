from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) 합격자 명단 버튼으로 변경
old_source = '<a class="source-link" href="https://www.sooplive.com/station/gosegu2/post/204391425" target="_blank" rel="noopener noreferrer">원본 게시글 ↗</a>'
new_source = '<a class="source-link" href="https://www.sooplive.com/station/gosegu2/post/205049071" target="_blank" rel="noopener noreferrer">참가합격자 명단 ↗</a>'
if old_source not in s:
    raise SystemExit('source link not found')
s = s.replace(old_source, new_source, 1)

# 2) 최종 참가자 발표 문구 아래 일정 추가
old_announcement = '''      <div id="deadlineCountdown" class="deadline-countdown final-announcement" role="status" aria-live="polite">
        <strong class="deadline-final-title">최종 참가자가 발표되었습니다!</strong>
      </div>'''
new_announcement = '''      <div id="deadlineCountdown" class="deadline-countdown final-announcement" role="status" aria-live="polite">
        <strong class="deadline-final-title">최종 참가자가 발표되었습니다!</strong>
        <span class="deadline-final-date">컨텐츠 일시 : 8/25(금) 20시</span>
      </div>'''
if old_announcement not in s:
    raise SystemExit('final announcement HTML not found')
s = s.replace(old_announcement, new_announcement, 1)

old_update = '''    function updateDeadlineCountdown() {
      const box = $('#deadlineCountdown');
      if (!box) return;
      box.className = 'deadline-countdown final-announcement';
      box.innerHTML = '<strong class="deadline-final-title">최종 참가자가 발표되었습니다!</strong>';
    }
'''
new_update = '''    function updateDeadlineCountdown() {
      const box = $('#deadlineCountdown');
      if (!box) return;
      box.className = 'deadline-countdown final-announcement';
      box.innerHTML = `
        <strong class="deadline-final-title">최종 참가자가 발표되었습니다!</strong>
        <span class="deadline-final-date">컨텐츠 일시 : 8/25(금) 20시</span>
      `;
    }
'''
if old_update not in s:
    raise SystemExit('updateDeadlineCountdown not found')
s = s.replace(old_update, new_update, 1)

# 3) 커트라인 관련 하단 안내 문구 제거
s = s.replace(
    '<p class="unofficial-notice">이 홈페이지는 공식 홈페이지가 아니며, 실제 컨텐츠 선정 인원은 커트라인과 상이할 수 있습니다</p>',
    '<p class="unofficial-notice">이 홈페이지는 공식 홈페이지가 아닙니다</p>',
    1
)

# 4) 커트라인 렌더링 제거
old_cutoff = '''      const lastCutoffIndex = cutoffRank > 0 && rankedVisible.length
        ? Math.min(cutoffRank, rankedVisible.length) - 1
        : -1;
      const rows = rankedVisible.length ? rankedVisible.map(({ item, rank }, index) => {
        const row = rowHtml(item, rank, draggable, scope, index === lastCutoffIndex);
        const cutoffLabel = index === lastCutoffIndex
          ? `<div class="top100-cutoff-label" aria-label="커트라인"><span>커트라인</span></div>`
          : '';
        return row + cutoffLabel;
      }).join('') : `<div class="empty">${esc(emptyMessage)}</div>`;'''
new_cutoff = '''      const rows = rankedVisible.length
        ? rankedVisible.map(({ item, rank }) => rowHtml(item, rank, draggable, scope, false)).join('')
        : `<div class="empty">${esc(emptyMessage)}</div>`;'''
if old_cutoff not in s:
    raise SystemExit('cutoff rendering block not found')
s = s.replace(old_cutoff, new_cutoff, 1)

# 5) 고세구 단일 카드: 남녀 랭킹 위에 삽입
needle_render = '''      if (state.splitGender) {
        const dragHint = state.isAdmin ? `<p class="drag-hint">PC는 드래그 · 모바일은 신청자를 약 0.5초 꾹 누른 뒤 여자/남자 칸으로 옮겨 놓으면 저장됩니다.</p>` : '';
        contentEl.innerHTML = `${dragHint}<div class="split">'''
replacement_render = '''      if (state.splitGender) {
        const dragHint = state.isAdmin ? `<p class="drag-hint">PC는 드래그 · 모바일은 신청자를 약 0.5초 꾹 누른 뒤 여자/남자 칸으로 옮겨 놓으면 저장됩니다.</p>` : '';
        const organizerCard = `
          <a class="organizer-card" href="https://www.sooplive.com/station/gosegu2" target="_blank" rel="noopener noreferrer" aria-label="고세구 방송국 열기">
            <div class="organizer-avatar-wrap">
              <img class="organizer-avatar" src="https://stimg.sooplive.com/LOGO/go/gosegu2/gosegu2.jpg" data-fallback-src="https://stimg.sooplive.com/LOGO/go/gosegu2/gosegu2.webp" alt="" loading="lazy" referrerpolicy="no-referrer"
                onerror="if(this.dataset.fallbackSrc){const u=this.dataset.fallbackSrc;delete this.dataset.fallbackSrc;this.src=u}else{this.style.display='none';this.nextElementSibling.style.display='grid'}">
              <div class="organizer-avatar-fallback" style="display:none">고</div>
            </div>
            <div class="organizer-name">고세구</div>
            <div class="organizer-role">역대급배그컨텐츠기획자</div>
          </a>`;
        contentEl.innerHTML = `${dragHint}${organizerCard}<div class="split">'''
if needle_render not in s:
    raise SystemExit('split render insertion point not found')
s = s.replace(needle_render, replacement_render, 1)

# 6) 최종 스타일 오버라이드 추가
css_marker = '/* ===== Final layout additions 2026-08-23 ===== */'
if css_marker not in s:
    css = r'''

    /* ===== Final layout additions 2026-08-23 ===== */
    /* 커트라인 관련 시각 요소는 완전히 숨깁니다. */
    .top100-cutoff-label,
    .rank-row.top100-cutoff-row,
    .female-board .rank-row.top100-cutoff-row,
    .male-board .rank-row.top100-cutoff-row {
      box-shadow: none !important;
    }
    .top100-cutoff-label { display: none !important; }

    /* 최종 발표 + 콘텐츠 일정 */
    .deadline-countdown.final-announcement,
    .deadline-countdown.is-warning.final-announcement,
    .deadline-countdown.is-urgent.final-announcement,
    .deadline-countdown.is-closed.final-announcement,
    .deadline-countdown.is-complete.final-announcement {
      display: flex !important;
      flex-direction: column !important;
      align-items: flex-end !important;
      justify-content: flex-start !important;
      gap: 6px !important;
    }
    .deadline-countdown.final-announcement .deadline-final-date {
      color: #4f6f5b !important;
      font-size: 14px !important;
      line-height: 1.2 !important;
      font-weight: 850 !important;
      letter-spacing: -.015em !important;
      white-space: nowrap !important;
    }

    /* 방송 진행자 고세구 전용 카드 */
    .organizer-card {
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
    }
    .organizer-avatar-wrap {
      width: 50px;
      height: 50px;
      overflow: hidden;
      display: grid;
      place-items: center;
      border: 2px solid #fff;
      border-radius: 50%;
      background: #edf5f9;
      box-shadow: 0 0 0 1px rgba(91,136,162,.20), 0 4px 11px rgba(52,100,128,.09);
    }
    .organizer-avatar {
      width: 100%;
      height: 100%;
      display: block;
      object-fit: cover;
    }
    .organizer-avatar-fallback {
      width: 100%;
      height: 100%;
      place-items: center;
      background: linear-gradient(145deg, #edf4f7, #f9fbfc);
      color: #5f7d90;
      font-size: 17px;
      font-weight: 950;
    }
    .organizer-name {
      min-width: 0;
      color: #1d4059;
      font-size: 18px;
      font-weight: 950;
      letter-spacing: -.025em;
    }
    .organizer-role {
      min-width: 190px;
      padding: 10px 14px;
      border: 1px solid #d9e8ef;
      border-radius: 12px;
      background: rgba(255,255,255,.78);
      color: #436577;
      font-size: 13px;
      font-weight: 900;
      letter-spacing: -.02em;
      text-align: center;
      white-space: nowrap;
    }

    @media (max-width: 640px) {
      .deadline-countdown.final-announcement .deadline-final-date {
        font-size: 11px !important;
      }
      .organizer-card {
        min-height: 62px;
        margin-bottom: 8px;
        padding: 8px 9px;
        grid-template-columns: 38px minmax(0, 1fr) auto;
        gap: 7px;
        border-radius: 14px;
      }
      .organizer-avatar-wrap {
        width: 38px;
        height: 38px;
        border-width: 1px;
      }
      .organizer-name { font-size: 13px; }
      .organizer-role {
        min-width: 0;
        padding: 7px 8px;
        border-radius: 9px;
        font-size: 9px;
      }
    }
'''
    if '</style>' not in s:
        raise SystemExit('style closing tag not found')
    s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
