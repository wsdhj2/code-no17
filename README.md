# 代号 No.17

竖屏小队生存射击游戏，当前版本 **0.78.0**。使用原生 JavaScript、Canvas 和本地音频，可在浏览器运行，也提供 Android 离线封装工程。

v0.78 增加航空扫射的双列曳光弹、连续落弹闪光、地面碎屑、扬尘和随地图后移的弹痕；保持伤害、范围和方向不变。

v0.77 优化轨道火力网的标定、炮弹尾焰、分层火球、冲击波、随路面后移的烟尘及轻微震屏，伤害、范围与炮击次数保持 v0.76 参数。

## 运行

安装 Node.js 20 或更新版本，在项目目录执行：

```sh
npm start
```

浏览器打开 `http://localhost:4186/`。不需要安装运行依赖。首次播放声音需要点击页面。进度保存在浏览器本地存储中。

## 内容

- 十章主线，每章两节；序章教程与工程师营救、信号塔防守支线。
- 小队自动射击、左右移动、救援人员及伤害和攻速成长。
- 感染者与机械敌人采用不同机制，包含运输机、自爆小车、精英及 Boss。
- 手势指令支援、重型战备、支线解锁的固定增援栏。
- 简单、普通、弈崎三档难度；简单和普通在指令输入时减速。
- 本地配乐、音效、合成无线电语音及对话选项。

## v0.76 调整

- 普通道具投放机会减少约 15%，轰炸与扫射采用相同掉落权重。
- 刷怪数量按攻速加成的 80% 增长，另保留人员成长系数。
- 感染者关不投放 EMP；机械关不投放诱饵，并限制其实际作用对象。
- 累计胆汁接触一秒后触发七秒尸潮。
- 新重型战备“轨道火力网”：三秒抵达，持续十秒，每秒一次随机小轰炸，单发 600 伤害、半径 95。

## 项目结构

| 路径 | 内容 |
| --- | --- |
| `index.html`、`frontline.js`、CSS | 界面、输入和战场绘制 |
| `engine.js` | 战斗、成长、刷怪与伤害规则 |
| `story-events.js`、`story.js` | 主线对话与剧情演出 |
| `signal-branch.js` | 信号塔支线及增援 |
| `assets/` | 图片、字体和可离线播放的音频 |
| `audio-sources/`、`voice-sources/` | 音频制作源文件与来源资料 |
| `android/` | Android 原生 WebView 容器 |
| `tools/build-android.py` | Android 离线安装包构建脚本 |
| `tests/`、`qa-*.cjs` | 规则测试和浏览器检查脚本 |
| `剧情台本-v72.md` | 剧情台本导出快照 |

保留了历次制作脚本和设计记录；历史文档描述的是当时版本，当前行为以运行源码为准。早期 README 已保存为 `HISTORY-early-versions.md`。

## 测试

v0.76 的当前规则回归：

```sh
node --test tests/support-v76.test.cjs tests/frontline.test.cjs tests/progression-v61.test.cjs tests/director-v62.test.cjs tests/vehicles-v74.test.cjs tests/balance-v72.test.cjs tests/laser-close-v72.test.cjs tests/story-v71.test.cjs tests/signal-branch-v66.test.cjs tests/robot-wave-v65.test.cjs tests/transport-v63.test.cjs tests/resource-dps-v57.test.cjs tests/robot-matchups.test.cjs
```

该组合共 124 项测试。`npm test` 包含历次版本的测试，其中部分针对旧参数；浏览器 QA 脚本中也保留了开发机器的路径，需要在其他机器上调整 Playwright 引用。手机尺寸浏览器检查不等同于安卓真机验证。

## Android 构建

需要 Python 3、JDK 21、Android SDK Build Tools 36 和 API 36 的 `android.jar`：

```sh
python tools/build-android.py --build-tools /path/to/build-tools/36.0.0 --platform-jar /path/to/platforms/android-36/android.jar --java-home /path/to/jdk --work ../work/android-build --output ../outputs/code17-0.76.0.apk
```

包名为 `com.emberfront.game`，最低 Android API 26。脚本把网页与资源封装进 APK，并签名、检查对齐。首次运行会在工作目录的同级 `ember-android-signing` 中生成签名材料。升级已有安装必须使用原签名，签名密钥和密码不进入 Git 仓库。APK 单独交付，不直接纳入源码提交。

## 资源说明

资源来源与制作记录见 `assets/audio/AUDIO-CREDITS.md`、`ART-NOTES-*.md` 及相关源文件目录。包含合成立绘与合成语音；项目没有额外声明开源许可，仓库上传不代表授予全部素材的再分发许可。下载素材压缩档、临时截图、构建缓存和日志不进入版本管理，已解压的制作源文件保留。
