from pathlib import Path
p=Path('index.html')
text=p.read_text(encoding='utf-8')
text=text.replace('<span class="deadline-date">8월 21일 23:59 마감</span>','<span class="deadline-date">8/21 23:59 마감</span>')
text=text.replace("timeEl.textContent = `${days}일 ${String(hours).padStart(2, '0')}시간 ${String(minutes).padStart(2, '0')}분 ${String(seconds).padStart(2, '0')}초`;","timeEl.textContent = `${days}일 ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;")
p.write_text(text,encoding='utf-8')
