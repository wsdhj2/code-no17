from pathlib import Path
import json
p=Path('qa-campaign.cjs');p.write_text("require('./qa-ten-chapters-v15.cjs');\n",encoding='utf-8')
p=Path('package.json');d=json.loads(p.read_text(encoding='utf-8'));d['version']='0.15.0';d['description']='余烬防线：十章撤离战役、感染者与机械军团、手势战备';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');p.write_text('''# v0.15 十章机械战役

当前版本：10章、26个关卡节点、10个独立Boss。前5章感染区，后5章机械战区。每章1或2个普通关与1个Boss关，同章保留人员、伤势、增益和支援消耗，跨章重置。第10章终点为安全区。

## 新机械敌人
- 第6章：巡逻射手、重装机枪精英。可见弹道，发射后可移动躲避。
- 第7章：导弹精英，圆形落点预警后范围伤害。
- 第8章：持盾精英，重甲和枪火配合。
- 第9章：横移无人机精英，空中火力骚扰。
- 第10章：混合军团与战争中枢机甲。

新增机械Boss：铁卫（扇面机枪/重击）、攻城者（连续迫击炮）、雷矛（锁定直线炮）、蜂巢（召唤机群/导弹）、裁决者（重弹、错位炮击、召唤交替）。普通机械敌人射击可以被战车与路障拦截，电磁支援可中断机械兵开火。酸液、胆汁与机器人弹道属于不同机制。

## 音效与UI
激光持续声改为无缝限频纹理，加入低频层，持续发射只启动一个循环，暂停/静音/结束时停止。手势输入、确认、取消、打开和失败分别使用独立短音效。机械战区使用机械反馈声。图鉴增加机械军团分类与Boss分页；十章路线保留历史星级，旧版五章通关存档接续第六章。

## 新素材
使用内置 image_gen 生成两张原始像素材质机甲/机械敌人图集，复制到 assets/mech-bosses-v15.png、assets/robot-enemies-v15.png，按裁切元数据在游戏中绘制；未使用Python编辑图像。完整生成提示词和素材路径见 ART-NOTES-v15.md。音效授权见 assets/audio/AUDIO-CREDITS.md。

## 验证
67项规则测试通过。浏览器验证26关推进至安全区、10个Boss节点、旧版通关迁移、5台机甲与机械图鉴、三种屏幕尺寸、10种手势及独立UI声音、持续激光与暂停恢复。移动端为浏览器尺寸验证，未宣称真实手机性能。

'''+s,encoding='utf-8')
Path('ART-NOTES-v15.md').write_text('''# Mechanical campaign art / v0.15

Method: built-in image_gen tool (not CLI). Original generated PNGs retained under Codex generated_images. Selected outputs copied into the game workspace. Source atlas pixels are preserved; runtime metadata selects sprite rectangles. These designs do not use copied franchise artwork or emblems.

Final files:
- assets/mech-bosses-v15.png
- assets/robot-enemies-v15.png
- assets/robot-manifest-v15.js (crop metadata)

## Boss atlas prompt
Use case: stylized-concept. Asset type: production sprite atlas for original mobile pixel-art military zombie/robot survival shooter. Create ONE transparent PNG atlas in a perfectly regular TWO COLUMN by FIVE ROW grid, 1024x1536 portrait. Ten separate sprites, every sprite fully inside its cell with at least 24px transparent gutter. Each row contains same giant mech boss twice: left idle, right weapon-firing pose. Camera fixed elevated top-down three-quarter view looking at front, all mechs facing DOWN toward viewer, full body visible, feet at bottom. Row 1 olive heavy biped with rotary machinegun arms and orange monoeye; row 2 slate blue tracked siege mech with twin mortars and reinforced plow; row 3 red-black spider quadruped with long rail cannon and cyan capacitors; row 4 pale industrial hexapod carrier with shield emitter and drone pods; row 5 enormous black and brass command biped with broad missile shoulders and red reactor core. Highly distinct silhouettes, chunky crisp pixel art, weathered steel plating, readable orange/cyan warning lamps, rich restrained material detail, strong contact shadows kept within sprite. Match dark urban survival pixel game art; not cartoon vector, no text, no cell borders, no floor, no background. Actual alpha transparency. All 10 cells consistent size and camera; no overlapping cells, no extra characters. Original designs, no copied franchise insignia.

## Robot atlas prompt
Use case: stylized-concept. Asset type: transparent enemy sprite atlas for a dark original military pixel-art mobile top-down shooter. ONE atlas 1024x1536 portrait with exactly TWO COLUMNS and FIVE ROWS, perfectly regular equal cells, 24 pixel transparent gutters. Every row same enemy in two poses, left idle aimed forward, right firing/attack. All seen elevated three-quarter top-down, facing DOWN toward bottom of screen, complete silhouettes, same lighting, no floor or environment. Row1 rifle robot infantry, thin olive steel skeletal legs, compact rifle and orange single eye; row2 bulky rotary gunner elite, broad armored blue-gray shoulders, ammunition belt, twin barrels; row3 missile-launcher robot elite with yellow shoulders and two tall rocket tubes; row4 heavy riot shield robot elite, large dark rectangular shield with narrow red slit and gun peeking around it; row5 hovering drone/sniper elite, four small rotor arms and central cyan long-barrel laser emitter, compact diamond silhouette. Crisp chunky detailed pixel art, restrained dark weathered metal, readable gun barrels and emissive red/orange/cyan accents, powerful distinct silhouettes, clear material light/shadow. Original designs suited to ruined city survival game. Alpha transparency required; no text, borders, labels, gridlines, background, extra sprites, cut-off parts, or overlap between cells.
''',encoding='utf-8')
p=Path('assets/audio/AUDIO-CREDITS.md');s=p.read_text(encoding='utf-8')+'\nv0.15: ui-input/ui-confirm/ui-cancel/ui-open/ui-error and laser-sustain-v15 are original designed short textures and a periodic continuous noise loop. enemy-rifle is derived from Free Firearm Sound Library B_16P; mech-servo derives from Residue ventilator. Licensed sources above remain applicable.\n';p.write_text(s,encoding='utf-8')
print('Documentation and asset provenance updated')
