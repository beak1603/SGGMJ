from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) TOP 100 버튼 숨김 + 툴바 정렬 보정
css_marker = '/* ===== Hide TOP100 control + stronger organizer blue ===== */'
if css_marker not in s:
    css = r'''

    /* ===== Hide TOP100 control + stronger organizer blue ===== */
    #top10Toggle {
      display: none !important;
    }
    @media (min-width: 641px) {
      .toolbar {
        grid-template-columns: minmax(0, 1fr) auto !important;
      }
    }

    .organizer-card {
      border-color: rgba(76, 172, 224, .82) !important;
      background: linear-gradient(105deg,
        rgba(215,242,255,.99) 0%,
        rgba(177,225,252,.97) 52%,
        rgba(137,205,245,.95) 100%) !important;
      box-shadow: 0 10px 28px rgba(34, 128, 184, .13) !important;
    }
    .organizer-card:hover {
      border-color: #55aeda !important;
      background: linear-gradient(105deg,
        rgba(203,237,255,1) 0%,
        rgba(160,218,251,.99) 52%,
        rgba(116,195,241,.97) 100%) !important;
      box-shadow: 0 13px 32px rgba(34, 128, 184, .17) !important;
    }
    .organizer-name {
      color: #15547a !important;
    }
    .organizer-role {
      border-color: rgba(87, 166, 208, .42) !important;
      background: rgba(255,255,255,.72) !important;
      color: #285d7a !important;
    }
'''
    if '</style>' not in s:
        raise SystemExit('style closing tag not found')
    s = s.replace('</style>', css + '\n</style>', 1)

# 2) 고세구 카드를 split 여부와 무관하게 공통 생성
old = '''      if (state.splitGender) {
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
        contentEl.innerHTML = `${dragHint}${organizerCard}<div class="split">
          ${boardHtml('여자 신청자', female, state.query ? '검색 결과가 없습니다.' : '여자로 분류된 신청자가 없습니다.', 'female', 'female', showGenderCutoff ? femaleTop100Cutoff : 0)}
          ${boardHtml('남자 신청자', male, state.query ? '검색 결과가 없습니다.' : '남자로 분류된 신청자가 없습니다.', 'male', 'male', showGenderCutoff ? maleTop100Cutoff : 0)}
        </div>${unknownBoard}`;
      } else {
        const overallCutoff = state.top10 && !state.query.trim() ? 100 : 0;
        contentEl.innerHTML = `<div class="single">${boardHtml('전체 신청자', tagged.sort(compareRankItems), state.query ? '검색 결과가 없습니다.' : '신청 댓글이 없습니다.', '', 'overall', overallCutoff)}</div>${unknownBoard}`;
      }'''

new = '''      const organizerCard = `
        <a class="organizer-card" href="https://www.sooplive.com/station/gosegu2" target="_blank" rel="noopener noreferrer" aria-label="고세구 방송국 열기">
          <div class="organizer-avatar-wrap">
            <img class="organizer-avatar" src="https://stimg.sooplive.com/LOGO/go/gosegu2/gosegu2.jpg" data-fallback-src="https://stimg.sooplive.com/LOGO/go/gosegu2/gosegu2.webp" alt="" loading="lazy" referrerpolicy="no-referrer"
              onerror="if(this.dataset.fallbackSrc){const u=this.dataset.fallbackSrc;delete this.dataset.fallbackSrc;this.src=u}else{this.style.display='none';this.nextElementSibling.style.display='grid'}">
            <div class="organizer-avatar-fallback" style="display:none">고</div>
          </div>
          <div class="organizer-name">고세구</div>
          <div class="organizer-role">역대급배그컨텐츠기획자</div>
        </a>`;

      if (state.splitGender) {
        const dragHint = state.isAdmin ? `<p class="drag-hint">PC는 드래그 · 모바일은 신청자를 약 0.5초 꾹 누른 뒤 여자/남자 칸으로 옮겨 놓으면 저장됩니다.</p>` : '';
        contentEl.innerHTML = `${dragHint}${organizerCard}<div class="split">
          ${boardHtml('여자 신청자', female, state.query ? '검색 결과가 없습니다.' : '여자로 분류된 신청자가 없습니다.', 'female', 'female', showGenderCutoff ? femaleTop100Cutoff : 0)}
          ${boardHtml('남자 신청자', male, state.query ? '검색 결과가 없습니다.' : '남자로 분류된 신청자가 없습니다.', 'male', 'male', showGenderCutoff ? maleTop100Cutoff : 0)}
        </div>${unknownBoard}`;
      } else {
        const overallCutoff = state.top10 && !state.query.trim() ? 100 : 0;
        contentEl.innerHTML = `${organizerCard}<div class="single">${boardHtml('전체 신청자', tagged.sort(compareRankItems), state.query ? '검색 결과가 없습니다.' : '신청 댓글이 없습니다.', '', 'overall', overallCutoff)}</div>${unknownBoard}`;
      }'''

if old not in s:
    raise SystemExit('organizer render block not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
