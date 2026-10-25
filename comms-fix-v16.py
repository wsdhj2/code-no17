from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace("function setCommsLine(){if(!prologue)return;", "function setCommsLine(){if(!prologue)return;mixer.stopSpeech();");p.write_text(s,encoding='utf-8')
