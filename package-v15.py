from pathlib import Path
import zipfile
r=Path.cwd();names=['index.html','engine.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json','ART-NOTES-v15.md']
out=r.parent/'余烬防线-v0.15-十章机械战役.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(r/n,'ember-vault/'+n)
 for p in (r/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(r).as_posix())
print('Packaged',round(out.stat().st_size/1024/1024,1),'MB')
