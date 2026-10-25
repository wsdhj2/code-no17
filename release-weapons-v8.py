from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace("function icon(type,x,y,scale=1){ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);if(type==='bomb')", """function icon(type,x,y,scale=1){ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);
if(['strafe','emp','laser','orbitalBomb','energyShield','mgTank','grenadeTank'].includes(type)){
 const color=F.ITEMS[type].color;
 if(type==='strafe'){for(let i=-1;i<=1;i++)poly([[-17+i*10,13],[-13+i*10,16],[9+i*10,-14],[5+i*10,-17]],color);}
 if(type==='emp')poly([[4,-21],[-14,3],[-2,3],[-4,22],[16,-7],[3,-7]],color);
 if(type==='laser'){rect(-4,-23,8,30,color);circle(0,13,13,color,false);poly([[-18,23],[0,9],[18,23]],color);}
 if(type==='orbitalBomb'){circle(0,0,18,color,false);circle(0,0,9,color,false);rect(-24,-1,48,2,color);rect(-1,-24,2,48,color);}
 if(type==='energyShield'){ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(0,-23);ctx.lineTo(20,-15);ctx.lineTo(16,10);ctx.lineTo(0,25);ctx.lineTo(-16,10);ctx.lineTo(-20,-15);ctx.closePath();ctx.stroke();poly([[3,-14],[-7,2],[1,2],[-2,14],[10,-4],[2,-4]],color);}
 if(type==='mgTank'||type==='grenadeTank'){rect(-20,-11,8,34,'#606d4d');rect(12,-11,8,34,'#606d4d');rect(-12,-14,24,35,color);rect(-7,-9,14,15,'#586748');rect(type==='mgTank'?-2:-5,-28,type==='mgTank'?4:10,23,color);}
 ctx.restore();return;
}if(type==='bomb')""")
p.write_text(s,encoding='utf-8')
p=Path('index.html');s=p.read_text(encoding='utf-8').replace('余烬防线：拖动控制队伍，拖拽右侧道具投放','余烬防线：左右拖动控制队伍，在支援终端绘制指令后投放');p.write_text(s,encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8-sig');history=s[s.index('## v0.4 声画更新'):]
intro='''# 余烬防线 v0.8 — 像素末日小队射击

双击“启动游戏.cmd”，或打开 http://localhost:4186 。也可直接打开 index.html 离线游玩，无需联网账号或安装游戏依赖。

## 操作与进度

出发前选择小队武器和最多两种重型支援。左右拖动队伍（电脑 A/D），队伍自动射击。点击右侧支援终端，直接照上方提示绘制手势来识别支援。终端为透明界面，绘制期间保持正常时间；只有识别成功、选择释放位置或扫射方向时才降为四分之一速度。松手投放，拖回支援入口或按 Esc 取消，不消耗道具。P 暂停，切到后台自动暂停。

五关：封锁公路、废弃医院、化工厂、货运港、撤离基地。每关行进65秒后进入独立Boss战；通关解锁下一关，也同步解锁武器。关卡解锁与选装偏好保存在本地。失败可重试当前关。继续下一关时保留队伍与攻击/攻速成长，并重新确认本关选装和补给。

## 武器

默认手枪，初始可选择手枪或冲锋枪。所有武器对全队生效。

| 武器 | 解锁 | 基础效果 |
|---|---|---|
| 手枪 | 初始 | 16伤害，1.4发/秒，直射，命中即消失 |
| 冲锋枪 | 初始 | 4伤害，7发/秒，直射，高频压制 |
| 大口径步枪 | 解锁第2关 | 44伤害，0.72发/秒，穿透3个目标，后续目标伤害逐次降至80% |
| 霰弹枪 | 解锁第3关 | 每发7颗弹丸，基础每颗7伤害，1.05发/秒；近距离×1.7，远距离衰减，最大射程360 |
| 激光炮 | 解锁第4关 | 全队光束汇聚后向前发射，每人基础20伤害/秒；人数和攻速升级增加束宽，攻击升级增加伤害 |

射速强化对枪械增加发射频率；激光炮保持固定伤害采样频率，将攻速强化转为光束增粗及额外伤害。只有大口径步枪的实体子弹可以穿透；霰弹弹丸各自命中一个目标。激光束可伤害束内的多个目标。武器有不同弹迹、聚能效果与音效。

## 两类支援

这里每关算一次出发：重型支援出发前最多选两种，每种本关只能使用一次，使用后不能通过掉落或Boss补给恢复。进入下一关时可以重新选装。允许少带或不带。

- 重型：轨道激光、轨道重轰炸、能量护盾、机枪战车、榴弹战车。重轰炸范围180、伤害5200；能量护盾1600耐久/18秒；轨道激光持续10秒、自动锁敌；机枪战车180发/1100耐久；榴弹战车28发/1400耐久。战车空弹后仍然抗伤，直到被摧毁。
- 局内：高爆轰炸、航空扫射、电磁压制、空投路障、声波诱饵。每关开局自带高爆轰炸1次，打破关内装备护盾获得额外支援。同类数量可累计，无库存上限；每次有效投放扣1，捡到后可以马上搓指令使用。Boss补给只空投局内支援目标，不恢复重型次数。

选择落点后，圆形轰炸延迟落下；扫射以首次触点为中心，拖动调整长条方向。路障固定落点，阻挡接近的丧尸；诱饵吸引普通感染者；电磁减速并打断攻击。支援不会伤害己方士兵；轰炸/激光等支援不破坏装备护盾。

## 队伍与敌人

初始8人，满编36人。左路装备和被困士兵固定在路面上，与路面同步经过；右路尸群主动逼近。清除围困丧尸后，约1.25秒归队才增加兵力。友军无误伤，没有医疗和复活。

吐酸者是远程精英，不是Boss。酸液落地前有预警，踩入持续酸池会间隔减员。精英名称不显示在战场；首页图鉴可点击模型查看名称、行为设定及应对方式。五个Boss各有立绘、攻击预警和半血阶段。

## 资源与验证

当前为可离线运行的网页游戏。原创像素场景、角色、首领、战车及本地声音的来源与字体许可见 assets/CREDITS.md。

- `node --test tests/frontline.test.cjs`：41项引擎测试。
- `node qa-armory-v8.cjs`：选装限制、解锁、库存、透明终端、精英图鉴、合束激光及手机/桌面布局。
- `node qa-support.cjs`：用测试库存验证全部10种指令的识别、错误重试、取消、消耗和释放；测试库存不代表正式游戏可携带全部重型支援。
- `node qa-campaign.cjs`：五关出场、阶段、过关及最终结算。
- `node qa-offline.cjs`：离线启动。
- `node simulate-campaign.cjs`：固定种子策略仿真。v0.8使用解锁武器及有限重型支援约351秒完成五关，仿真会即时发出支援指令，不代表玩家胜率或真机操作验证。

浏览器测试使用本机现有Edge与Playwright。运行游戏本身不需要这些测试依赖。未接入微信小游戏运行环境。

## 历史更新

'''
p.write_text(intro+history,encoding='utf-8')
