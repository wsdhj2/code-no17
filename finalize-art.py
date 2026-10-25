from pathlib import Path
import base64

p=Path('art-direction.css'); s=p.read_text(encoding='utf-8')
data=base64.b64encode(Path('assets/fonts/EmberDisplay.woff2').read_bytes()).decode()
s=s.replace("url('assets/fonts/EmberDisplay.woff2')", "url('data:font/woff2;base64,"+data+"')")
p.write_text(s,encoding='utf-8')
p=Path('engine.js'); s=p.read_text(encoding='utf-8-sig').replace("this.unit('giant',LANES[1],175", "this.unit('giant',LANES[1],235")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js'); s=p.read_text(encoding='utf-8-sig').replace("if(e.type==='boss'){mixer.setMode('boss');toast(","if(e.type==='boss'){mixer.setMode('boss');shake=6;flash=.13;toast(")
p.write_text(s,encoding='utf-8')
p=Path('package.json'); s=p.read_text(encoding='utf-8-sig').replace('0.3.1','0.4.0'); p.write_text(s,encoding='utf-8')
p=Path('README.md'); s=p.read_text(encoding='utf-8-sig').replace('v0.3.1','v0.4')
s=s.replace('Canvas程序绘制，Web Audio合成音效。','使用AI生成的原创城市材质与Canvas像素角色绘制；标题使用站酷庆科黄油体。23段原创本地音频包括分层枪声、重火力、命中、爆炸、感染者叫声、巡逻氛围与Boss配乐。暂停菜单可分别调节音效、音乐、环境音量。素材来源及许可见 assets/CREDITS.md。')
if '## v0.4 声画更新' not in s:
 s+='\n## v0.4 声画更新\n\n湿沥青、破损混凝土、锈蚀围栏、霓虹积水与废弃车辆的像素城市材质；嵌入式艺术标题字体支持离线显示。重绘行尸、低伏疾奔者、防化服感染者、脓肿者和灾厄巨躯。枪声采用瞬态、低频枪体、机械尾音和街道短回声分层；Boss战有116BPM原创配乐，普通路段有88BPM配乐与城市风声。所有声音是原创合成，不是实录枪械或真人配音。\n\n`audio.js` 管理采样音效、音乐过渡、暂停/静音和音量保存；`build-audio.py` 可重建音频；`art-direction.css` 包含本地嵌入的字体子集与艺术界面。`qa-art.cjs` 与 `qa-soundscape.cjs` 验证材质、字体、音频解码、Boss切歌、暂停续播与手机布局。\n'
p.write_text(s,encoding='utf-8')
