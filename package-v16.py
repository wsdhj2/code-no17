from pathlib import Path
import zipfile
r=Path.cwd();out=r.parent/'余烬防线-v0.16-指挥部序章.zip'
with zipfile.ZipFile(out,'a',zipfile.ZIP_DEFLATED) as z:
 pass
# Rebuild the runtime package so each file has exactly one entry.
names=['index.html','engine.js','story.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','story-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json','ART-NOTES-v15.md','ART-NOTES-v16.md']
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(r/n,'ember-vault/'+n)
 for p in (r/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(r).as_posix())
print('Final package updated')
