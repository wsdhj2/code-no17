from pathlib import Path
import json,zipfile
p=Path('package.json');d=json.loads(p.read_text(encoding='utf-8'));d['version']='0.16.0';d['description']='余烬防线：指挥部剧情序章、交互教程、十章撤离与无线电支援';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');p.write_text('''# v0.16 指挥部通讯与序章

新增序章「断线重连」。首次进入且没有战役通关记录的玩家会从未知求救信号开始；已有进度的玩家可在首页点「序章」重玩。序章独立于26个正式关卡，不覆盖星级、人员接续存档或解锁进度。

## 剧情演出
- 人类指挥部两位固定角色：联络员林澈、指挥官陈砚。
- 新立绘、角色名牌、通讯频道、杂音波形、逐字字幕；点击可立即显示整句，再点击继续。
- 「跳过全部剧情」跳过当前与之后的对话，保留教程实操；「跳过序章」直接进入战役准备。
- 十章首次进入有指挥部对话，安全区终点有收尾剧情；都受统一剧情跳过选项控制。
- 剧情以文字演出为主，并非全篇配音。

## 实操教程
向右移动 → 自动射击救人 → 向联络员绘制空袭指令 → 选择落点并等待抵达 → 获得轨道授权 → 绘制激光指令处理重装目标 → 第一章整备。绘制阶段不减速，选择投放位置时才减速。

## 无线电语音
使用本机 Windows SAPI（Microsoft Zira / David / Huihui）合成短句，再做通讯带宽、饱和与开闭噪声处理；不是原作游戏音频或真人录音。处理后的WAV随游戏离线提供，不依赖网络语音接口。支持空袭、轨道打击、补给、战车、护盾、电磁、链路建立、重型敌情与目标完成。通知队列最多等待3条，同类短时间去重，字幕位于队伍上方；暂停菜单可独立调整「无线电语音」音量。

语句：Air strike incoming. / Orbital strike incoming. / Supply inbound. / Armored support inbound. / Shield deployment confirmed. / EMP strike confirmed. / Command link established. / Heavy hostile approaching. / Objective complete. Proceed to extraction.

## 新素材与验证
新指挥部立绘通过内置 image_gen 生成，文件 assets/hq-portraits-v16.png；提示词见 ART-NOTES-v16.md。源图未使用Python编辑。

69项规则测试；浏览器实际完成全部序章操作（含真实手势与落点）、三种尺寸的立绘/跳过/持久化、十条语音解码和空袭/轨道/补给队列；旧存档迁移、26关推进、持续激光和离线运行回归通过。

'''+s,encoding='utf-8')
Path('ART-NOTES-v16.md').write_text('''# Headquarters portraits

Method: built-in image_gen. Saved game asset: assets/hq-portraits-v16.png. The original generated PNG is retained in Codex generated_images; selected output copied into the workspace. CSS displays each half without modifying source pixels. Earlier three-character portrait concept was discarded after the user clarified the two human HQ roles.

Final prompt:
Use case: stylized-concept. Asset type: original visual-novel dialogue character portrait atlas for a polished dark pixel-art tactical survival game. ONE landscape 1536x1024 transparent PNG, exactly TWO equal vertical panels. Each panel contains a single human HEADQUARTERS officer, waist-up, head fully visible, shoulders and uniform fully within own half, 40px clear gutter between panels. LEFT: Chinese female communications liaison, adult around 27, short dark bob, soft but focused expression, over-ear communications headset with boom microphone, slate-blue uniform with subtle cyan stitching and utility vest, one hand on headset, cyan monitor rim lighting. RIGHT: Chinese male commanding officer around 48, graying temples, short neat hair, dark navy high-collared command coat with understated original insignia and shoulder epaulettes, calm decisive expression, arms loosely crossed, one gloved hand holding a thin tablet, restrained amber rim lighting. Both clearly HUMAN headquarters staff, no helmets or robot parts, no weapons, no sexualization. Detailed illustrated pixel art with mature visual-novel character acting, original designs suitable for ruined-city zombie/robot campaign, rich fabric and face shading, coherent limited desaturated palette, crisp readable silhouette. Frontal three-quarter waist-up composition suitable for Galgame/strategy mobile comms windows. True alpha background, no room or scenery, no text, labels, borders or logos. Do not copy existing franchise characters.
''',encoding='utf-8')
p=Path('assets/audio/AUDIO-CREDITS.md');s=p.read_text(encoding='utf-8')+'\nv0.16 radio notifications: local Windows SAPI synthesized speech using Microsoft Zira/David/Huihui, processed for radio bandwidth. Original written notification text; no sampled Helldivers or Arknights voice lines. radio-static is original noise synthesis. Voice-source scripts are authoring tools, not required by the offline game.\n';p.write_text(s,encoding='utf-8')
r=Path.cwd();names=['index.html','engine.js','story.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','story-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json','ART-NOTES-v15.md','ART-NOTES-v16.md']
out=r.parent/'余烬防线-v0.16-指挥部序章.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(r/n,'ember-vault/'+n)
 for p in (r/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(r).as_posix())
print('v0.16 packaged',round(out.stat().st_size/1024/1024,1),'MB')
