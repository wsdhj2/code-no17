from pathlib import Path
import json,zipfile
p=Path('qa-audio-v11.cjs');s=p.read_text(encoding='utf-8').replace("assert.ok(result.counts['orbital-beam-loop']>0)","assert.equal(result.counts['orbital-beam-loop']||0,0)");p.write_text(s,encoding='utf-8')
p=Path('package.json');d=json.loads(p.read_text(encoding='utf-8'));d['version']='0.12.1';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');p.write_text('''# v0.12.1 激光声音修复

轨道激光和队伍激光炮共用平稳、限频的连续滋声循环，移除0.65秒反复触发的切片与激光炮逐发音效；削减尖锐高频，限制叠加音量。光束结束时淡出，暂停、静音或返回菜单时停止。枪械页激光试听为0.9秒。

浏览器验证：持续发射超过一个循环只启动一次，旧切片不再触发；暂停/继续及结束淡出正常。

'''+s,encoding='utf-8')
r=Path.cwd();names=['index.html','engine.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json']
with zipfile.ZipFile(r.parent/'余烬防线-v0.12.1-完整游戏.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(r/n,'ember-vault/'+n)
 for p in (r/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(r).as_posix())
print('laser audio fix packaged')
