from pathlib import Path
import json,zipfile
p=Path('package.json');d=json.loads(p.read_text(encoding='utf-8'));d['version']='0.13.0';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');p.write_text('''# v0.13 更新

- 轨道激光持续显示和发声。没有目标时驻留投放点，击杀目标后停在最后照射点，搜索范围内出现新目标后继续追踪。
- Boss登场前2.4秒出现单行WARNING警告横幅与低频警报，登场后短暂显示首领名称。
- 修正轰炸飞机倒飞：机头与运动方向一致，从下往上掠过落点；扫射飞机沿玩家指定方向飞行。飞机在战场角色之上绘制。
- 普通小关75秒或90秒后进入肃清，Boss关推进45秒后出现首领；每五波之间留6秒调整时间。
- 胆汁首次接触立即召来24只感染者，从两侧错位逼近，同时保留8秒新增尸群翻倍；持续沾染只刷新时间，不连续重复召唤。

验证：59项引擎回归通过；浏览器检查Boss预警与登场、无目标激光显示/持续声、胆汁即时尸群，以及激光暂停恢复与淡出。

'''+s,encoding='utf-8')
r=Path.cwd();names=['index.html','engine.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json']
with zipfile.ZipFile(r.parent/'余烬防线-v0.13-完整游戏.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(r/n,'ember-vault/'+n)
 for p in (r/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(r).as_posix())
print('v0.13 packaged')
