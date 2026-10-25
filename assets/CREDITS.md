# 余烬防线 v0.5 视觉与声音来源

## 城市材质

`city-road-v4.png`：使用内置 image_gen 工具为本项目生成的原创像素风末日城市公路。提示词和用途见 `art-prompt.txt`。运行时在离屏画布上采样为216×324像素后放大绘制，保持像素质感；原图保留。

## 角色精灵 v0.5

`characters-v5.png`：内置 image_gen 工具为本项目生成的原创透明角色图集。包含游骑步枪兵、破衣行尸、低伏疾奔者、防化感染者、膨胀脓肿者、灾厄巨躯，各有左右迈步、攻击、倒地四种姿态，共24个。提示词见 `characters-v5-prompt.txt`。

`characters-v5-manifest.js/json` 只记录透明边界裁切与统一脚底锚点，不改写原图像素。`characters.js` 按动作帧绘制，在运行时应用受击闪白和亮度调整；未使用任何现有游戏角色资产。完整原图保留。

## 字体

`fonts/EmberDisplay.woff2`：ZCOOL QingKe HuangYou（站酷庆科黄油体），Google Fonts 官方按本项目标题用字提供的子集，SIL Open Font License 1.1。许可全文见 `fonts/OFL.txt`。

官方来源：https://github.com/google/fonts/tree/main/ofl/zcoolqingkehuangyou

## 音效与配乐

`audio/` 中音效与配乐由本项目 `build-audio.py` 原创合成，无第三方录音、演员台词或现有游戏音轨。包括三种步枪声、重火力、肉体/护甲/护盾撞击、爆炸、五种感染者非语言叫声、受伤与无线电提示、胜负提示、城市风声、巡逻配乐和Boss配乐。

枪声为瞬态噪声、低频枪体、机械尾音与短街道回声的分层合成；感染者声音为谐波、气流噪声和动态包络合成。不是实录枪械或真人配音。音乐为原创D小调循环，巡逻88BPM，Boss116BPM。

## 类型参考

参考《求生之路》通过外形、动作和声音区分感染者的设计方向。游戏内行尸、疾奔者、防化感染者、脓肿者、灾厄巨躯均为本项目原创绘制；未使用Valve的角色模型、贴图、声音、音乐、标志或原名角色资产。

官方介绍：https://www.l4d.com/game.html

### 标题字体更新

`fonts/EmberSerif-Bold.ttf`、`fonts/EmberSerif-Black.ttf`：Noto Serif SC（思源宋体同源字体），Google Fonts 官方按界面标题及按钮用字提供的700/900字重子集。SIL Open Font License 1.1，全文见 `fonts/Serif-OFL.txt`。仅用于标题及菜单，战斗小字保持系统黑体。历史黄油体已停用。
来源：https://github.com/google/fonts/tree/main/ofl/notoserifsc

## v0.7 战役资产

以下均由内置 imagegen 为本项目生成的原创像素资产，不使用商业游戏角色、标志、模型或地图：

- `campaign-roads-v7.png`：五个并列地图面板。运行时分别采样为216×720后绘制，无覆盖或改写源文件。
- `campaign-bosses-v7b.png`：最终五首领图集，立绘、待机、攻击、狂暴姿态。医院首领经生成工具定向修改为缝合者，不再是吐酸角色。
- `escorts-v7.png`：吐酸精英与两种护卫战车，含攻击及空弹姿态。
- `campaign-bosses-v7.png`、`boss-iron-v7.png`：早期设计留档，未作为最终战役图集使用。

`campaign-manifest.js/json` 保存运行时裁切边界，`inspect-campaign.py` 复现元数据。部分大立绘跨越图集行界，展示时改用同角色完整待机图，避免裁断；源图保留。最终生成提示见 `campaign-art-prompts.txt`。


## v0.9 原生作战地图与界面

`operation-map-v9.svg` 为代码绘制的原创城市平面图，`operation-map-v9.js` 封装相同SVG的data URI供离线与现有本地服务器一致显示，不改变原有像素战场资产。`operation-ui.css` 实现连接式节点、蓝灰高对比任务区、左侧可用支援与右上透明手势输入。

界面布局研究参考《明日方舟》官方产品及公开作战终端截图，采用信息层级与连接节点的设计方向，没有使用其图片、角色、图标、字体文件或标志。
参考：https://www.arknights.global/ ，https://arknights.wiki.gg/wiki/Terminal
## Vehicle artwork, v74

New transparent raster sprites generated for this project using the imagegen skill: dropship-v74.png, sapper-v74.png, supply-truck-v74.png. The dropship silhouette references the heavy industrial troop-carrier design shown on the official Helldivers 2 page: https://www.playstation.com/en-us/games/helldivers-2/ . No source game image, mesh or texture is included. Dynamic engine light, tread movement, landing, crash and unloading effects are drawn by the local runtime.
## Vehicle orientation correction, v75

Redrawn from the v74 designs: supply-truck-v75.png and sapper-v75.png align to the vertical road axis with a centered elevated camera; dropship-v75.png aligns horizontally to its flight direction. Generated transparent artwork using imagegen. Old v74 artwork is retained as a source reference but is no longer selected by the runtime.
