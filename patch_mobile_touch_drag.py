from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

css = r'''

    /* Mobile long-press drag & drop */
    [data-drag-key] {
      -webkit-user-select: none;
      user-select: none;
    }
    @media (pointer: coarse) {
      [data-drag-key] {
        -webkit-touch-callout: none;
      }
    }
    .touch-drag-source {
      opacity: .42 !important;
    }
    .board.touch-drop-target {
      outline: 3px solid rgba(57, 175, 240, .58);
      outline-offset: -3px;
      box-shadow: 0 0 0 5px rgba(57, 175, 240, .11), 0 12px 30px rgba(45,120,160,.13) !important;
    }
    .female-board.touch-drop-target {
      outline-color: rgba(217, 104, 145, .58);
      box-shadow: 0 0 0 5px rgba(217, 104, 145, .10), 0 12px 30px rgba(167,77,108,.11) !important;
    }
    .touch-drag-ghost {
      position: fixed;
      z-index: 3000;
      left: 0;
      top: 0;
      max-width: 170px;
      padding: 8px 11px;
      border: 1px solid rgba(104,145,169,.25);
      border-radius: 11px;
      background: rgba(255,255,255,.96);
      box-shadow: 0 10px 30px rgba(29,73,99,.22);
      color: #243e51;
      font-size: 12px;
      font-weight: 900;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      pointer-events: none;
      transform: translate(-50%, -125%);
    }
    body.touch-dragging {
      overscroll-behavior: none;
    }
'''

if '/* Mobile long-press drag & drop */' not in text:
    text = text.replace('</style>', css + '\n</style>', 1)

old_hint = '''        const dragHint = state.isAdmin ? `<p class="drag-hint">신청자를 드래그해서 반대쪽 성별 칸에 놓으면 수동 분류로 저장됩니다.</p>` : '';'''
new_hint = '''        const dragHint = state.isAdmin ? `<p class="drag-hint">PC는 드래그 · 모바일은 신청자를 약 0.5초 꾹 누른 뒤 여자/남자 칸으로 옮겨 놓으면 저장됩니다.</p>` : '';'''
text = text.replace(old_hint, new_hint, 1)

js = r'''

    // 모바일 브라우저는 기본 HTML5 drag/drop 지원이 불안정하므로
    // 관리자 모드에서 길게 누른 뒤 손가락으로 옮기는 터치 드래그를 별도로 지원합니다.
    const touchDragState = {
      timer: null,
      active: false,
      key: '',
      startX: 0,
      startY: 0,
      x: 0,
      y: 0,
      sourceRow: null,
      targetZone: null,
      ghost: null
    };

    function clearTouchDragTimer() {
      if (touchDragState.timer) clearTimeout(touchDragState.timer);
      touchDragState.timer = null;
    }

    function clearTouchDropTarget() {
      if (touchDragState.targetZone) touchDragState.targetZone.classList.remove('touch-drop-target');
      touchDragState.targetZone = null;
    }

    function finishTouchDragVisuals() {
      clearTouchDragTimer();
      clearTouchDropTarget();
      touchDragState.sourceRow?.classList.remove('touch-drag-source');
      touchDragState.ghost?.remove();
      document.body.classList.remove('touch-dragging');
      touchDragState.active = false;
      touchDragState.key = '';
      touchDragState.sourceRow = null;
      touchDragState.ghost = null;
    }

    function positionTouchGhost(x, y) {
      if (!touchDragState.ghost) return;
      touchDragState.ghost.style.left = `${x}px`;
      touchDragState.ghost.style.top = `${y}px`;
    }

    function updateTouchDropTarget(x, y) {
      const el = document.elementFromPoint(x, y);
      const zone = el?.closest?.('[data-gender-drop]') || null;
      if (zone === touchDragState.targetZone) return zone;
      clearTouchDropTarget();
      if (zone) {
        zone.classList.add('touch-drop-target');
        touchDragState.targetZone = zone;
      }
      return zone;
    }

    function applyMobileGenderDrop(key, gender) {
      if (!state.isAdmin || !key || (gender !== 'female' && gender !== 'male')) return;
      const item = state.comments.find(x => itemKey(x) === key);
      const beforeGender = item ? classifyGender(item) : '';
      const actuallyMoved = Boolean(beforeGender && beforeGender !== gender);

      if (item) setManualGenderForItem(item, gender);
      else state.manualGenderOverrides[key] = gender;

      if (actuallyMoved) state.newDraggedApplicants.add(key);
      saveManualGenderOverrides();

      if (item) syncGenderForItem(item, gender, actuallyMoved);
      else syncGenderOperation({ operation: 'set', keys: [key], gender, nickname: '', markNew: actuallyMoved });
      render();
    }

    contentEl.addEventListener('touchstart', (e) => {
      if (!state.isAdmin || e.touches.length !== 1) return;
      if (e.target.closest('button')) return;
      const row = e.target.closest('[data-drag-key]');
      if (!row) return;

      const t = e.touches[0];
      finishTouchDragVisuals();
      touchDragState.key = row.dataset.dragKey || '';
      touchDragState.startX = touchDragState.x = t.clientX;
      touchDragState.startY = touchDragState.y = t.clientY;
      touchDragState.sourceRow = row;

      touchDragState.timer = setTimeout(() => {
        if (!touchDragState.key || !touchDragState.sourceRow) return;
        touchDragState.active = true;
        touchDragState.sourceRow.classList.add('touch-drag-source');
        document.body.classList.add('touch-dragging');

        const ghost = document.createElement('div');
        ghost.className = 'touch-drag-ghost';
        ghost.textContent = touchDragState.sourceRow.querySelector('.name-link')?.textContent?.trim() || '신청자 이동';
        document.body.appendChild(ghost);
        touchDragState.ghost = ghost;
        positionTouchGhost(touchDragState.x, touchDragState.y);
        updateTouchDropTarget(touchDragState.x, touchDragState.y);
        if (navigator.vibrate) navigator.vibrate(25);
      }, 480);
    }, { passive: true });

    contentEl.addEventListener('touchmove', (e) => {
      if (!touchDragState.key || e.touches.length !== 1) return;
      const t = e.touches[0];
      touchDragState.x = t.clientX;
      touchDragState.y = t.clientY;

      if (!touchDragState.active) {
        const dx = t.clientX - touchDragState.startX;
        const dy = t.clientY - touchDragState.startY;
        if (Math.hypot(dx, dy) > 10) finishTouchDragVisuals();
        return;
      }

      e.preventDefault();
      positionTouchGhost(t.clientX, t.clientY);
      updateTouchDropTarget(t.clientX, t.clientY);

      // 긴 목록에서도 손가락을 화면 위/아래 가장자리로 가져가면 천천히 스크롤합니다.
      if (t.clientY < 72) window.scrollBy(0, -18);
      else if (t.clientY > window.innerHeight - 72) window.scrollBy(0, 18);
    }, { passive: false });

    contentEl.addEventListener('touchend', (e) => {
      if (!touchDragState.key) return;
      clearTouchDragTimer();
      if (!touchDragState.active) {
        finishTouchDragVisuals();
        return;
      }

      e.preventDefault();
      const t = e.changedTouches?.[0];
      const zone = t ? updateTouchDropTarget(t.clientX, t.clientY) : touchDragState.targetZone;
      const key = touchDragState.key;
      const gender = zone?.dataset?.genderDrop || '';
      finishTouchDragVisuals();
      if (gender === 'female' || gender === 'male') applyMobileGenderDrop(key, gender);
    }, { passive: false });

    contentEl.addEventListener('touchcancel', () => finishTouchDragVisuals(), { passive: true });

    contentEl.addEventListener('contextmenu', (e) => {
      if (state.isAdmin && window.matchMedia?.('(pointer: coarse)')?.matches && e.target.closest('[data-drag-key]')) {
        e.preventDefault();
      }
    });
'''

marker = "    adminBtn.addEventListener('click', () => {"
if 'const touchDragState = {' not in text:
    if marker not in text:
        raise SystemExit('admin button marker not found')
    text = text.replace(marker, js + '\n\n' + marker, 1)

p.write_text(text, encoding='utf-8')
