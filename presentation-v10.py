from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8')
a=s.index(" $('#overlay').innerHTML=`<h2 class=\"home-title\"")
z=s.index(";\n $('#start').onclick",a)
s=s[:a]+''' $('#overlay').innerHTML=`<div class="home-design"><div class="home-brand"><span class="brand-mark">╱╱</span><span>余烬行动局<small>EVACUATION DIVISION</small></span><b>01 / 05</b></div><div class="home-hero"><span class="home-kicker">THE LAST ROAD HOME</span><h1>余烬<span>防线</span></h1><div class="hero-coordinate">31° 14′ N<br>121° 28′ E</div><div class="hero-line"></div><span class="home-edition">战术生存 · 像素行动</span></div><div class="home-bottom"><div class="home-status"><i></i><span>撤离路线已建立</span><b>${(record.clearedStages||[]).length} / 13</b></div><button class="primary" id="start">进入作战<span>↗</span></button><div class="menu-actions"><button class="secondary" id="models">作战图鉴 <span>＋</span></button><button class="secondary" id="help">行动指南 <span>＋</span></button></div><div class="home-footer">EMBER FRONT<span>终点 / 安全区</span></div></div></div>`'''+s[z:]
s=s.replace("startButton.textContent=ok?'作战终端':'加载失败，重试'", "startButton.innerHTML=ok?'进入作战<span>↗</span>':'加载失败，重试'")
# replace old detailed stats area with art and bar display
start=s.index('<div class="weapon-detail"><span>${w.desc}')
end=s.index('<div class="equipment-label"><span>重型支援',start)
s=s[:start]+'${weaponPresentation(b.weapon,w)}'+s[end:]
pos=s.index('function start(level=')
fn='''function weaponPresentation(id,w){
const shapes={
pistol:'<path d="M83 65H229L244 74V97H174L161 145H118L126 97H83Z"/><path class="gun-dark" d="M125 102H163L151 137H120Z"/><path d="M173 98H198V119H168V113H190V104H172Z"/><path class="gun-steel" d="M92 68H227V78H92Z"/><path class="gun-dark" d="M224 78H245V91H224Z"/>',
smg:'<path d="M45 75H258V98H175L167 117H126L108 101H45Z"/><path d="M45 80H16V113H43Z"/><path class="gun-dark" d="M139 100H164L157 150H134Z M93 100H117L108 136H88Z"/><path class="gun-steel" d="M183 79H250V91H183Z M255 81H298V91H255Z"/><path d="M218 62H241V75H218Z"/>',
rifle:'<path d="M19 89L66 77H186L206 85H297V94H203L184 103H106L89 125H66L72 101H19Z"/><path class="gun-dark" d="M122 102H151L142 138H116Z"/><path d="M119 67H185V77H119Z M134 61H177V67H134Z"/><path class="gun-steel" d="M193 80H258V89H193Z M272 83H308V98H272Z"/><path class="gun-dark" d="M22 92H62V100H22Z"/>',
shotgun:'<path d="M18 94L71 82H134L149 91H292V98H139L116 107H87L66 126H45L52 102H18Z"/><path class="gun-steel" d="M123 74H303V83H123Z M161 89H292V95H161Z"/><path class="gun-wood" d="M166 83H222V102H166Z M22 94H72L65 114H48L52 101H22Z"/><path class="gun-dark" d="M95 105H117L105 137H87Z"/>',
laserCannon:'<path d="M24 70H215L240 82H296V109H239L216 123H24Z"/><path class="gun-dark" d="M39 78H91V114H39Z M114 78H178V114H114Z M147 123H184V146H147Z"/><path class="gun-glow" d="M94 72H104V122H94Z M183 72H193V122H183Z M243 87H292V103H243Z"/><path class="gun-steel" d="M29 64H210V70H29Z M28 123H211V129H28Z"/>'};
const stats=[['单发威力',id==='laserCannon'?55:Math.min(100,w.damage/28*100)],['射击频率',Math.min(100,w.rate/10*100)],['覆盖范围',w.pellets?95:w.pierce?65:id==='laserCannon'?45:15]];
return `<div class="weapon-showcase"><span class="armory-serial">${({pistol:'P-09 / SERVICE',smg:'SM-24 / RAPID',rifle:'AR-76 / PIERCING',shotgun:'SG-12 / SCATTER',laserCannon:'LC-01 / CONVERGENCE'})[id]}</span><svg class="weapon-portrait" viewBox="0 0 330 175" role="img" aria-label="${w.name}侧视立绘"><defs><linearGradient id="gunMetal" x2="0" y2="1"><stop stop-color="#9faeb5"/><stop offset=".4" stop-color="#687b88"/><stop offset="1" stop-color="#344650"/></linearGradient></defs><path class="weapon-guide" d="M8 150H320M8 33V155M320 33V155M40 46H288"/><g class="gun-body">${shapes[id]}</g><path class="weapon-guide" d="M276 138H309M292 122V154"/></svg><div class="weapon-summary"><b>${w.name}</b><span>${w.desc}</span></div><div class="weapon-bars">${stats.map(([name,value])=>`<div><span>${name}</span><i><em style="width:${Math.max(8,value)}%"></em></i></div>`).join('')}</div></div>`;
}
'''
s=s[:pos]+fn+s[pos:]
s=s.replace("[[192,414],[240,414],[216,456]]", "[[282,458]]").replace("x,y,1.8,0", "x,y,3.8,0")
p.write_text(s,encoding='utf-8')
