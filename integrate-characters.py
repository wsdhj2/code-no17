from pathlib import Path

p=Path('index.html');s=p.read_text(encoding='utf-8-sig')
s=s.replace('<script src="audio.js">','<script src="assets/characters-v5-manifest.js"></script><script src="characters.js"></script><script src="audio.js">')
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8-sig')
s=s.replace('let run=null,screen=', 'let corpses=[];let run=null,screen=')
s=s.replace('function soldier(', 'function legacySoldier(',1).replace('function zombie(', 'function legacyZombie(',1)
pos=s.index('function legacySoldier(')
s=s[:pos]+'''function soldier(x,y,scale=1,special=false,trapped=false,index=0){
 const time=run?.time||visualTime,shot=run&&run.state==='playing'&&!trapped&&run.shotClock>Math.max(0,1/(run.rate*(run.mech>0?1.3:1))-.1);
 const moving=trapped?false:(!run||Math.abs(run.x-run.targetX)>2||run.joins.length>0),frame=shot?2:moving?(Math.floor(time*8+index*.7)%2):0;
 EmberCharacters.shadow(ctx,x,y,10*scale,3.5*scale,.58);
 if(!EmberCharacters.draw(ctx,'soldier',x,y,scale,frame))legacySoldier(x,y,scale,special,trapped,index);
 if(trapped){label('!',x,y-42*scale,'#e3c78b',Math.max(8,Math.round(10*scale)));}
}
function zombie(x,y,type='walker',scale=1,age=0,hit=false,attacking=false){
 const frame=attacking?2:Math.floor(age*(type==='runner'?9:5))%2;
 EmberCharacters.shadow(ctx,x,y,(type==='giant'?24:type==='bloater'?17:12)*scale,4*scale,.64);
 if(!EmberCharacters.draw(ctx,type,x,y,scale,frame,hit))legacyZombie(x,y,type,scale,age,hit);
}
function addCorpse(type,x,y,scale=1){corpses.push({type,x,y,scale,age:0,life:type==='giant'?4.5:2.6});if(corpses.length>35)corpses.shift();}
function drawCorpses(){for(const c of corpses){const p=project(c.x,c.y),alpha=Math.min(1,(c.life-c.age)/.8)*.8;EmberCharacters.draw(ctx,c.type,p.x,p.y,c.scale,3,false,Math.max(0,alpha));}}
''' +s[pos:]
s=s.replace('particles=[];floaters=[];ripples=[];shake=0;', 'particles=[];floaters=[];ripples=[];corpses=[];shake=0;')
s=s.replace("if(e.type==='guardFall'){", "if(e.type==='guardFall'){for(let i=0;i<e.count;i++){const angle=((e.remaining||0)+i)/6*Math.PI*2-Math.PI/2;addCorpse('walker',e.x+Math.cos(angle)*30,e.y+Math.sin(angle)*25,.85);}")
s=s.replace("if(e.type==='kill'){", "if(e.type==='kill'){addCorpse(e.kind,e.x,e.y,e.kind==='giant'?2:1.12);")
s=s.replace("if(e.type==='casualty'){", "if(e.type==='casualty'){for(let i=0;i<e.count;i++)addCorpse('soldier',e.x+(i-(e.count-1)/2)*17,e.y+5,1.06);")
s=s.replace("zombie(p.x,p.y,'giant',2.0,o.age,o.hit>0);", "zombie(p.x,p.y,'giant',2.0,o.age,o.hit>0,o.windup>.15);")
s=s.replace('1.02+o.y/2500,o.age,o.hit>0);', '1.02+o.y/2500,o.age,o.hit>0,o.windup>.15);')
s=s.replace('for(const e of run.effects)effect(e);', 'for(const e of run.effects)effect(e);drawCorpses();')
s=s.replace('events();hud();for(const p of particles)', 'events();hud();for(const c of corpses)c.age+=dt;corpses=corpses.filter(c=>c.age<c.life);for(const p of particles)')
s=s.replace("window.emberAudioSnapshot=()=>mixer.snapshot();", "window.emberCharacterSnapshot=()=>({...EmberCharacters.snapshot(),corpses:corpses.length});window.emberAudioSnapshot=()=>mixer.snapshot();")
old='<button class="secondary" id="help" style="margin-top:10px">行动手册</button>'
new='<div class="menu-actions"><button class="secondary" id="help">行动手册</button><button class="secondary" id="models">角色图鉴</button></div>'
s=s.replace(old,new)
s=s.replace("$('#start').onclick=start;$('#help').onclick=help;", "$('#start').onclick=start;$('#help').onclick=help;$('#models').onclick=gallery;const startButton=$('#start');if(!EmberCharacters.snapshot().loaded){startButton.disabled=true;startButton.textContent='正在加载角色…';EmberCharacters.ready.then(ok=>{startButton.disabled=false;startButton.textContent=ok?'集结出发 →':'角色加载失败，点击刷新';if(!ok)startButton.onclick=()=>location.reload();});}")
pos=s.index('function help()')
s=s[:pos]+'''function gallery(){overlayState='gallery';$('#overlay').innerHTML='<div class="kicker">CHARACTER FIELD GUIDE / 05</div><h2 style="font-size:32px;margin:12px 0 0">行动档案</h2><p class="description" style="margin:7px 0">六种原创角色 · 实际战场使用的精灵</p><canvas id="characterGallery" width="374" height="375"></canvas><button id="back" class="primary" style="margin-top:16px">返回集结点</button>';$('#back').onclick=menu;drawGallery();}
function drawGallery(){const target=$('#characterGallery');if(!target)return;const g=target.getContext('2d');g.clearRect(0,0,374,375);g.imageSmoothingEnabled=false;
 const kinds=['soldier','walker','runner','armored','bloater','giant'],names=['游骑步枪兵','破衣行尸','低伏疾奔者','防化感染者','膨胀脓肿者','灾厄巨躯'],notes=['背包 / 护甲 / 步枪','破衣 / 消瘦 / 扑咬','蓝色兜帽 / 快速接近','黄色防化服 / 护甲','膨胀腹部 / 连锁爆炸','巨拳 / 疤痕 / 重击'];
 for(let i=0;i<6;i++){const x=i%2*187,y=Math.floor(i/2)*125;g.fillStyle='#10222bdc';g.fillRect(x+3,y+3,181,119);g.strokeStyle='#a0ad9044';g.strokeRect(x+3.5,y+3.5,180,118);EmberCharacters.shadow(g,x+94,y+83,25,6,.6);EmberCharacters.draw(g,kinds[i],x+94,y+83,i===5?1.3:1.55,Math.floor(visualTime*3)%2);g.textAlign='center';g.font='bold 12px Microsoft YaHei';g.fillStyle='#e1ccb0';g.fillText(names[i],x+94,y+101);g.font='9px Microsoft YaHei';g.fillStyle='#92a59c';g.fillText(notes[i],x+94,y+115);}
}
''' +s[pos:]
s=s.replace('}render();requestAnimationFrame(frame);', "}render();if(overlayState==='gallery')drawGallery();requestAnimationFrame(frame);")
p.write_text(s,encoding='utf-8')
p=Path('engine.js');s=p.read_text(encoding='utf-8-sig').replace("this.emit('guardFall',{x:o.x,y:o.y,count:fallen})", "this.emit('guardFall',{x:o.x,y:o.y,count:fallen,remaining})")
s=s.replace('cols=Math.min(5,this.army)', 'cols=Math.min(6,Math.ceil(Math.sqrt(this.army*1.3)))').replace(')*18,y:610',')*20,y:610')
p.write_text(s,encoding='utf-8')
