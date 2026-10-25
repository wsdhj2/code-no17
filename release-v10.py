from pathlib import Path
import json,zipfile
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace("for(let i=0;i<count;i++)particles.push", "for(let i=0;i<count&&particles.length<700;i++)particles.push")
s=s.replace("if(e.type==='explosion'){particlesAt(e.x,e.y,'#f3c385',35);ripples.push({x:e.x,y:e.y,r:e.radius,age:0,color:'#efb971'});", "if(e.type==='explosion'){particlesAt(e.x,e.y,e.source==='strafe'?'#c9d7c4':'#f3c385',e.source==='strafe'?5:e.source==='grenade'?12:30);if(e.source!=='strafe')ripples.push({x:e.x,y:e.y,r:e.radius,age:0,color:'#efb971'});")
p.write_text(s,encoding='utf-8')
p=Path('package.json');data=json.loads(p.read_text(encoding='utf-8'));data['version']='0.10.0';data['description']='余烬防线：五章撤离战役、手势支援、武器选装与尸潮首领战';p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');s='''# v0.10 更新

- 静态首页，不滚动、不震屏；枪械使用独立侧视插画和性能条。
- 霰弹枪射程620，7发扇形散射；近距离优势来自弹丸命中重叠，没有强制距离减伤。
- 支援入口再次点击关闭。绘制阶段正常时间，完成指令选择落点时才减速。
- 呼叫到达：1秒（护盾、电磁、诱饵）；2秒（轰炸、扫射、路障）；3秒（轨道激光、重轰炸、两种战车）。到达前不生效，持续时间从到达后计算。
- 区分5种枪械、扫射、榴弹、轨道打击、护盾、电磁、落地和破坏音效，限制高频重复发声。
- 常规尸潮每3.2秒15只起，后续章节增加。Boss登场保留小怪并增援，战斗中每5.5秒8只起。
- Boss更频繁攻击、更大范围，按各自配置伤害作用于区域内每名士兵；预警仍保留躲避时间。
- 五章共13节点，同章保留人员、伤势、增益和已消耗支援，跨章重置。最终抵达安全区。

验证：52项引擎回归、10种手势、13关进度、3种屏幕尺寸、静态首页与开关交互。脚本策略压力测试用于发现问题，不代表真实玩家胜率。

'''+s;p.write_text(s,encoding='utf-8')
