from pathlib import Path
import zipfile,json,wave
root=Path.cwd();out=root.parent/'余烬防线-v0.10-完整游戏.zip'
files=['index.html','engine.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json']
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for name in files:z.write(root/name,'ember-vault/'+name)
 for p in (root/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(root).as_posix())
print('Release:',out,'MB:',round(out.stat().st_size/1024/1024,1))
for p in (root/'assets/audio').glob('*.wav'):
 with wave.open(str(p)) as f:assert f.getnframes()>0
print('WAV assets valid')
