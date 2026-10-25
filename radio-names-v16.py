from pathlib import Path
p=Path('audio.js');s=p.read_text(encoding='utf-8').replace("el.querySelector('b').textContent=VOICE_LINES[cue];", "el.querySelector('small').textContent=cue==='warning'?'陈砚 / 指挥频道':'林澈 / 指挥部频道';el.querySelector('b').textContent=VOICE_LINES[cue];");p.write_text(s,encoding='utf-8')
