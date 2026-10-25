from pathlib import Path

p=Path('index.html');s=p.read_text(encoding='utf-8-sig');a=s.index('<div id="hud" hidden>');b=s.index('<section id="overlay"',a)
s=s[:a]+'''<div id="hud" hidden>
<header class="battle-top">
 <div class="squad-readout" aria-label="剩余士兵"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="6" r="3"/><path d="M6 20v-6a6 6 0 0 1 12 0v6h-4v-6h-4v6z"/></svg><b id="army">8</b></div>
 <div class="journey"><span id="chapter">封锁公路</span><div class="route"><i id="progress"></i></div></div>
 <div class="tools"><button id="sound" title="声音" aria-label="切换声音"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/><path class="sound-wave" d="M17 8q5 4 0 8" fill="none" stroke="currentColor" stroke-width="1.8"/></svg></button><button id="pause" aria-label="暂停"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3v14H7zM14 5h3v14h-3z"/></svg></button></div>
</header>
<div id="tactics" aria-label="战术道具栏"></div>
<div id="slowBanner" hidden>松手投放 <small>拖回取消</small></div>
</div>''' +s[b:]
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8-sig');a=s.index('function hud(){');b=s.index("const sig=JSON.stringify(run.inventory);",a)
s=s[:a]+'''function hud(){if(!run)return;$('#army').textContent=String(run.army);$('.squad-readout').setAttribute('aria-label',`剩余${run.army}名士兵`);const chapter=run.time<43?0:run.time<88?1:2;$('#chapter').textContent=run.bossSpawned?'撤离点':['封锁公路','感染街区','撤离通道'][chapter];$('#progress').style.width=Math.min(100,run.time/F.END*100)+'%';
''' +s[b:]
s=s.replace('<span class="count">×${s.count}</span>', '<span class="count">${s.count}</span>')
s=s.replace('`<button class="tactic empty" disabled aria-label="空战术槽位">${svg(\'empty\')}<b>待收集</b></button>`', "'<span class=\"tactic-empty\" aria-hidden=\"true\"></span>'")
# Preserve the SVG and only change its muted state, rather than replacing it with a music-note glyph.
s=s.replace("$('#sound').textContent=soundOn?'♪':'×';", "$('#sound').classList.toggle('muted',!soundOn);")
s=s.replace("top=ctx.createLinearGradient(0,0,0,160)", "top=ctx.createLinearGradient(0,0,0,104)")
s=s.replace("top.addColorStop(0,'#102b32fa');top.addColorStop(.65,'#102b32e8');top.addColorStop(1,'#102b3200');", "top.addColorStop(0,'#061017a6');top.addColorStop(.4,'#06101744');top.addColorStop(1,'#06101700');")
s=s.replace('ctx.fillRect(0,0,W,160);','ctx.fillRect(0,0,W,104);')
a=s.index('const bottom=ctx.createLinearGradient(');b=s.index('\nif(flash>0)',a);s=s[:a]+s[b:]
# Keep raster characters at their authored proportions on tall phone displays.
s=s.replace('window.emberCharacterSnapshot=', '''function fitViewport(){const box=canvas.getBoundingClientRect();canvas.spriteYRatio=(box.width/W)/(box.height/H);}window.addEventListener('resize',fitViewport);fitViewport();
window.emberCharacterSnapshot=''')
p.write_text(s,encoding='utf-8')
p=Path('characters.js');s=p.read_text(encoding='utf-8');s=s.replace("const dx=Math.round(x+(f.x-f.center)*factor),dy=Math.round(y+(f.y-char.base)*factor),dw=Math.max(1,Math.round(f.w*factor)),dh=Math.max(1,Math.round(f.h*factor));", "const sy=ctx.canvas.spriteYRatio||1;const dx=Math.round(x+(f.x-f.center)*factor),dy=Math.round(y+(f.y-char.base)*factor*sy),dw=Math.max(1,Math.round(f.w*factor)),dh=Math.max(1,Math.round(f.h*factor*sy));")
p.write_text(s,encoding='utf-8')
