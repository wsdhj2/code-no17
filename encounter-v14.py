from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace('duration:boss?16:part===0?40:44','duration:boss?45:part===0?75:90')
s=s.replace('this.nextWave+=2.8','this.nextWave+=this.wave%5===0?6:2.8')
s=s.replace("if(!this.bossSpawned&&this.mission().boss&&this.time>=this.mission().duration)", "if(!this.bossWarned&&this.mission().boss&&this.time>=this.mission().duration-2.4){this.bossWarned=true;this.emit('bossWarning',{name:LEVELS[this.level].boss});}\n if(!this.bossSpawned&&this.mission().boss&&this.time>=this.mission().duration)")
s=s.replace('this.bossSpawned=false;', 'this.bossWarned=false;this.bossSpawned=false;')
s=s.replace("e.triggered=true;this.bile=8;this.emit('bileHit',{duration:8});", "e.triggered=true;const fresh=this.bile<=0;this.bile=8;if(fresh){const lane=this.x<216?0:1;this.spawnHorde(lane,180,6,Math.max(1,Math.floor(this.level/2)));this.spawnHorde(1-lane,20,6,Math.max(1,Math.floor(this.level/2)));}this.emit('bileHit',{duration:8,horde:fresh});")
s=s.replace("e.audioTick=(e.audioTick||0)-dt;if(e.audioTick<=0){e.audioTick=.65;this.emit('supportPulse',{item:e.type});}", "")
s=s.replace('else{e.beamX=null;e.beamY=null;}', 'else{e.beamX=e.beamX??e.x;e.beamY=e.beamY??e.y;}')
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8');a=s.index('function showBossIntro(){');z=s.index('function starDisplay',a)
s=s[:a]+'''function showBossWarning(){document.querySelector('#bossIntro')?.remove();const el=document.createElement('aside');el.id='bossIntro';el.className='boss-warning';el.setAttribute('role','status');el.innerHTML=`<span class="warning-symbol">△</span><b>WARNING</b><i></i><span>重型感染体接近</span>`;$('#frame').append(el);mixer.play('boss-warning',.45);setTimeout(()=>{if(el.isConnected)el.remove();},2400);}
function showBossIntro(){document.querySelector('#bossIntro')?.remove();const el=document.createElement('aside');el.id='bossIntro';el.className='boss-arrival';el.innerHTML=`<small>首领出现</small><b>${F.LEVELS[run.level].boss}</b>`;$('#frame').append(el);setTimeout(()=>el.remove(),1800);}
'''+s[z:]
s=s.replace("if(e.type==='boss'){", "if(e.type==='bossWarning')showBossWarning();if(e.type==='boss'){")
s=s.replace("toast('沾染胆汁 · 尸潮 ×2',2)", "toast(e.horde?'胆汁引发尸潮 · 敌群来袭':'沾染胆汁 · 尸潮 ×2',2)")
s=s.replace("function effect(e){if(e.arrival", "function supportAircraft(e){if(!['bomb','strafe'].includes(e.type))return;const age=e.age-(e.arrival||0),angle=e.type==='strafe'?e.angle:-Math.PI/2,travel=(age-(e.type==='strafe'?.8:0))*850,x=e.x+Math.cos(angle)*travel,y=e.y+Math.sin(angle)*travel;if(x<-50||x>482||y<100||y>800)return;const q=project(x,y);ctx.save();ctx.translate(q.x,q.y);ctx.rotate(angle+Math.PI/2);icon('bomb',0,0,1.5);ctx.restore();}\nfunction effect(e){supportAircraft(e);if(e.arrival")
s=s.replace("const planeY=(e.age-(e.arrival||0))*850;if(planeY>-100&&planeY<900)icon('bomb',p.x+50,planeY,1.5);", "")
s=s.replace("else circle(p.x,p.y,35,'#e6cf86',false);return;}", "return;}") if False else s
# Snapshot shows an active ray even in the first untargeted frame.
s=s.replace("if(e.type==='laser'){if(e.beamX!=null){const target=project(e.beamX,e.beamY)", "if(e.type==='laser'){if(e.age>=(e.arrival||0)){const target=project(e.beamX??e.x,e.beamY??e.y)")
s=s.replace("&&e.age<e.duration&&e.beamX!=null", "&&e.age<e.duration")
p.write_text(s,encoding='utf-8')
p=Path('tests/frontline.test.cjs');s=p.read_text(encoding='utf-8').replace('r.time=15.99','r.time=r.mission().duration-.01')
# Bile now spawns its promised immediate horde; isolate the multiplier test from that horde.
s=s.replace("r.bilePool(r.x,624,60,0);advance(r,.02);r.entities=[];", "r.bilePool(r.x,624,60,0);advance(r,.02);r.entities=[];")
s+='''\ntest('orbital laser stays on its last position when empty and acquires new enemies',()=>{const r=empty();r.inventory=[{type:'laser',count:1}];r.deploy(0,216,300);advance(r,3.1);const e=r.effects.find(e=>e.type==='laser');assert.equal(e.beamX,216);assert.equal(e.beamY,300);const z=r.unit('armored',240,320,{hp:10000,max:10000,speed:0});advance(r,.1);assert.equal(e.beamX,240);z.dead=true;advance(r,.1);assert.equal(e.beamX,240);assert.equal(e.beamY,320);});
test('bile contact immediately summons a horde once and repeat pools only refresh the debuff',()=>{const r=empty();r.bilePool(r.x,624,60,0);advance(r,.02);assert.equal(r.entities.length,24);r.bilePool(r.x,624,60,0);advance(r,.02);assert.equal(r.entities.length,24);});
test('longer missions warn before bosses without clearing existing infected',()=>{assert.ok(F.STAGES.filter(m=>!m.boss).every(m=>m.duration>=75));const r=empty();r.stageId=1;r.time=r.mission().duration-2.41;advance(r,.03);assert.ok(r.drain().some(e=>e.type==='bossWarning'));assert.equal(r.bossSpawned,false);});
''';p.write_text(s,encoding='utf-8')
