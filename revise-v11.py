from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8')
s=s.replace("loadout:cp?F.normalizeLoadout(cp.loadout):F.normalizeLoadout(record.loadout)","loadout:cp?F.normalizeLoadout(cp.loadout):[]")
a=s.index('<div class="heavy-options">${F.HEAVY_ITEMS.map');z=s.index('<div class="field-starter">',a)
s=s[:a]+'''<div class="loadout-slots">${[0,1].map(slot=>{const id=b.slots?.[slot]??b.loadout[slot];return `<button class="loadout-slot ${id?'filled':''}" data-slot="${slot}" ${b.checkpoint?'disabled':''}><small>0${slot+1}</small>${id?`${supportIcon(id)}<b>${F.ITEMS[id].name}</b><span>${F.ITEMS[id].arrival}s 抵达 · 1次</span>`:'<i>＋</i><b>选择战备</b>'}</button>`;}).join('')}</div>'''+s[z:]
a=s.index("document.querySelectorAll('[data-heavy]').forEach");z=s.index("$('#deployStart').onclick",a)
s=s[:a]+"document.querySelectorAll('[data-slot]').forEach(el=>el.onclick=()=>chooseLoadout(Number(el.dataset.slot)));"+s[z:]
pos=s.index('function launch(')
s=s[:pos]+'''function chooseLoadout(slot){const b=briefing;if(!b||b.checkpoint)return;if(!b.slots)b.slots=[b.loadout[0]||null,b.loadout[1]||null];$('#loadoutPicker')?.remove();const sheet=document.createElement('section');sheet.id='loadoutPicker';sheet.innerHTML=`<div class="loadout-sheet"><header><div><small>战备槽 0${slot+1}</small><h3>选择支援</h3></div><button id="pickerClose" aria-label="关闭战备选择">×</button></header><div class="loadout-choices">${F.HEAVY_ITEMS.map(id=>{const elsewhere=b.slots[1-slot]===id;return `<button data-pick="${id}" ${elsewhere?'disabled':''} class="${b.slots[slot]===id?'chosen':''}">${supportIcon(id)}<span><b>${F.ITEMS[id].name}</b><small>${({laser:'锁定追踪 · 持续10秒',orbitalBomb:'广域打击 · 5200伤害',energyShield:'吸收1600伤害 · 持续18秒',mgTank:'180发弹药 · 1100装甲',grenadeTank:'28发榴弹 · 1400装甲'})[id]}</small></span><i>${elsewhere?'已携带':F.ITEMS[id].arrival+'s'}</i></button>`;}).join('')}</div><button id="clearSlot">卸下战备</button></div>`;$('#frame').append(sheet);const close=()=>sheet.remove();$('#pickerClose').onclick=close;sheet.onclick=e=>{if(e.target===sheet)close();};sheet.querySelectorAll('[data-pick]').forEach(el=>el.onclick=()=>{b.slots[slot]=el.dataset.pick;b.loadout=b.slots.filter(Boolean);close();drawBriefing();});$('#clearSlot').onclick=()=>{b.slots[slot]=null;b.loadout=b.slots.filter(Boolean);close();drawBriefing();};}
'''+s[pos:]
# null slots must stay null, avoid fallback duplicates
s=s.replace("b.slots?.[slot]??b.loadout[slot]", "b.slots?b.slots[slot]:b.loadout[slot]")
s=s.replace("label(e.ammo>0?`${e.ammo} 发`:'弹药耗尽 · 护卫',p.x,p.y+23,e.ammo>0?'#d7d8ad':'#a8b09b',9);", "const ammoMax=e.type==='mgTank'?180:28,ammoRatio=e.ammo/ammoMax;rect(p.x+36,p.y-49,7,49,'#07151ce8');rect(p.x+38,p.y-47+45*(1-ammoRatio),3,45*ammoRatio,ammoRatio>.2?'#f0d08a':'#e58d6b');for(let i=1;i<5;i++)rect(p.x+37,p.y-47+i*9,5,1,'#162834');label(e.ammo>0?String(e.ammo):'空',p.x+40,p.y+13,e.ammo>0?'#e5d5aa':'#df987a',8);")
s=s.replace("if(e.type==='arrival')mixer.arrival(e.item);", "if(e.type==='arrival')mixer.arrival(e.item);if(e.type==='supportApproach')mixer.approach(e.item);if(e.type==='supportPulse')mixer.play('orbital-beam-loop',.26);")
p.write_text(s,encoding='utf-8')
p=Path('engine.js');s=p.read_text(encoding='utf-8')
s=s.replace("e.age+=dt;if(e.arrival&&e.age<e.arrival)continue;", "e.age+=dt;if(e.arrival&&!e.approaching&&e.age>=e.arrival-.75){e.approaching=true;this.emit('supportApproach',{item:e.type});}if(e.arrival&&e.age<e.arrival)continue;")
s=s.replace("if(e.type==='laser'&&activeAge>=0){", "if(e.type==='laser'&&activeAge>=0){e.audioTick=(e.audioTick||0)-dt;if(e.audioTick<=0){e.audioTick=.65;this.emit('supportPulse',{item:e.type});}")
s=s.replace("this.nextWave+=3.2", "this.nextWave+=2.8").replace("8+this.level*2,2+Math.floor(this.level/2)", "11+this.level*2,2+Math.floor(this.level/2)").replace("this.nextWave=this.time+5.5", "this.nextWave=this.time+4.5")
s=s.replace("hp:map.hp,max:map.hp", "hp:map.hp*1.15,max:map.hp*1.15")
s=s.replace("const motion=dt*(o.slow>0?.22:1)", "const motion=dt*(o.slow>0?.22:1)*(1+this.level*.04+(this.bossSpawned?.08:0))")
p.write_text(s,encoding='utf-8')
