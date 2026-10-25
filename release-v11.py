from pathlib import Path
import json,zipfile
p=Path('package.json');d=json.loads(p.read_text(encoding='utf-8'));d['version']='0.11.0';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');s='''# v0.11 更新

- 尸群、资源、被困士兵随机左右换边；同一侧资源最多连续三波。同波资源与主尸群分处两侧。
- 战备为两个空的「＋」槽位，点开选择；支持更换、卸下，不能重复携带。同章接续时沿用战备。
- 战车右侧显示竖向弹药条、剩余数量和低弹药颜色，空弹后仍可抗伤害。
- 采用 The Free Firearm Sound Library 的 CC0 枪械录音，四种实弹武器有交替样本；空袭与轨道打击区分接近、充能、命中，另有持续激光、喷酸、战车射击与空弹反馈。枪械页可试听。
- 音效来源与修改说明见 assets/audio/AUDIO-CREDITS.md，游戏行动指南也有鸣谢。Jet Engine Takeoff by dklon 使用 CC BY 3.0；其余引入素材为 CC0。不是所有声音都声称为真实录音，能量/科幻效果仍使用设计素材。
- 三星评级按每关存活率：90%以上三星、70%以上两星、其余通关一星；失败无星。每关单独计算，保存历史最高星级。
- 激光后于尸体和角色绘制，避免遮挡。
- 常规尸潮2.8秒一波，Boss增援4.5秒一波，Boss生命提升15%。

验证：53项规则测试；三种屏幕的战备选择、移除与重复限制；10种手势；13关进度与章节继承；16个声音文件解码与事件触发；三星存档和激光绘制顺序；离线运行。脚本压力测试不能代表玩家真实胜率。

'''+s;p.write_text(s,encoding='utf-8')
root=Path.cwd();out=root.parent/'余烬防线-v0.11-完整游戏.zip'
files=['index.html','engine.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json']
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for name in files:z.write(root/name,'ember-vault/'+name)
 for p in (root/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(root).as_posix())
print('v0.11 packaged',round(out.stat().st_size/1024/1024,1),'MB')
