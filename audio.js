/* Layered licensed field recordings and designed effects; see AUDIO-CREDITS.md. HTMLAudio also works when index.html opens offline. */
(() => {
'use strict';
const root='assets/audio/';
const VOICE_LINES={airstrike:'Air strike incoming.',orbital:'Orbital strike incoming.',supply:'Supply inbound.',reinforcements:'Reinforcements have arrived.',armor:'Armored support inbound.',shield:'Shield deployment confirmed.',emp:'EMP strike confirmed.',linked:'Command link established.',warning:'Heavy hostile approaching.',objective:'Objective complete. Proceed to extraction.',unknown:'还有活人吗？收到请回答。'};
class Soundscape {
 constructor(){
  this.enabled=true;this.unlocked=false;this.mode='menu';this.lastVolley=-10;this.lastCreature=-10;this.clock=0;this.pool=new Map();this.cooldowns={};this.duckUntil=0;this.variant=0;this.counts={};this.laserBed=this.element('laser-sustain-v15.wav',true);this.previewUntil=0;
  this.levels={sfx:.65,music:.38,ambience:.3,voice:.85};this.voiceQueue=[];this.voiceHistory={};this.voiceCue=null;this.dialogue=false;this.speech=new Audio();this.speech.preload='auto';this.speech.onended=()=>{this.voiceCue=null;this.nextVoice();};this.speech.onerror=()=>{this.voiceCue=null;this.nextVoice();};
  try{const saved=JSON.parse(localStorage.getItem('ember-audio'));for(const key of Object.keys(this.levels))if(typeof saved?.[key]==='number')this.levels[key]=Math.max(0,Math.min(1,saved[key]));}catch{}
  this.scoreFiles={menu:'score-menu-v43',patrol:'score-battle-v43',boss:'score-boss-v43',victory:'score-victory-v43',defeat:'score-defeat-v43'};this.musicMode=null;this.scorePreview=null;this.oneShotStarted={};this.tracks={...Object.fromEntries(Object.entries(this.scoreFiles).map(([key,file])=>[key,this.element(file+'.ogg',!['victory','defeat'].includes(key))])),ambience:this.element('ambience.ogg',true)};
  const firstTouch=()=>{if(!this.enabled)return;this.unlocked=true;if(this.mode==='menu')this.tracks.menu.play().catch(()=>{});};document.addEventListener('pointerdown',firstTouch,{once:true});document.addEventListener('keydown',firstTouch,{once:true});
  for(const [key,element] of Object.entries(this.tracks)){element.addEventListener('error',()=>{if(element.src.endsWith('.ogg'))element.src=root+(this.scoreFiles[key]||'ambience')+'.wav';},{once:true});}
  for(const name of ['gun-pistol','gun-pistol-alt','gun-smg','gun-smg-alt','gun-rifle','gun-rifle-alt','gun-shotgun','gun-shotgun-alt','airstrike-flyby','airstrike-impact','orbital-cannon-impact','orbital-charge','orbital-beam-loop','orbital-designate-v44','orbital-incoming-v44','orbital-impact-v44'])this.pool.set(name,[this.element(name+'.wav')]);
 }
 element(file,loop=false){const a=new Audio(root+file);a.preload='auto';a.loop=loop;a.volume=0;return a;}
 chatter(speaker='liaison'){if(this.clock-(this.lastChatter??-9)<.075)return;this.lastChatter=this.clock;this.play('radio-text-'+(['liaison','commander','unknown'].includes(speaker)?speaker:'commander'),this.levels.voice*.19,.94+(this.variant++%5)*.035);}
 speak(cue){if(!VOICE_LINES[cue]||cue==='unknown'||!this.enabled||!this.unlocked||this.dialogue)return;if(this.clock-(this.voiceHistory[cue]??-99)<3||this.voiceQueue.includes(cue)||this.voiceCue===cue)return;this.voiceHistory[cue]=this.clock;if(this.voiceQueue.length>=3)this.voiceQueue.shift();this.voiceQueue.push(cue);if(!this.voiceCue)this.nextVoice();}
 nextVoice(){if(!this.enabled){this.stopSpeech();return;}const cue=this.voiceQueue.shift();let el=document.querySelector('#radioNotice');if(!cue){if(el)el.hidden=true;return;}this.voiceCue=cue;this.speech.src=root+'voice-'+cue+'.wav';this.speech.playbackRate=1.18;this.speech.preservesPitch=true;this.speech.volume=this.levels.voice;this.speech.play().catch(()=>{this.voiceCue=null;this.nextVoice();});this.counts['voice-'+cue]=(this.counts['voice-'+cue]||0)+1;if(!el){el=document.createElement('aside');el.id='radioNotice';el.innerHTML='<small>COMMAND / RADIO</small><b></b>';document.querySelector('#frame')?.append(el);}el.querySelector('b').textContent=VOICE_LINES[cue];el.hidden=this.dialogue||!!document.querySelector('#tutorialGoal');}
 stopSpeech(){this.voiceQueue=[];this.voiceCue=null;this.speech.pause();try{this.speech.currentTime=0;}catch{}const el=document.querySelector('#radioNotice');if(el)el.hidden=true;}
 stopLaser(){this.laserBed.pause();this.laserBed.volume=0;this.previewUntil=0;}
 beginRun(){this.stopSpeech();this.voiceHistory={};this.stopLaser();for(const a of Object.values(this.tracks)){a.pause();a.currentTime=0;}this.bossAnnounced=false;this.mode='menu';this.lastCreature=-10;}
 unlock(){this.unlocked=true;this.play('call-confirm',.25);}
 save(){try{localStorage.setItem('ember-audio',JSON.stringify(this.levels));}catch{}}
 play(name,volume=1,pitch=null){
  if(!this.enabled||!this.unlocked)return;
  const gap=({'gun-smg':.075,'blast-grenade':.18,'shield-hit':.2,'gun-laser':.16,'impact':.1,'boss-impact':.2,'air-strafe-cannon':.1,'enemy-rifle':.14,'ui-input':.045,'tank-machinegun':.1,'spitter-cast':.5,'empty-magazine':.3,'orbital-beam-loop':.6})[name]||0;if(gap&&this.clock-(this.cooldowns[name]??-10)<gap)return;this.cooldowns[name]=this.clock;let list=this.pool.get(name);if(!list){list=[this.element(name+'.wav')];this.pool.set(name,list);}
  let a=list.find(e=>e.paused||e.ended);
  if(!a&&list.length<4){a=this.element(name+'.wav');list.push(a);}if(!a)return;
  a.currentTime=0;a.volume=Math.min(1,volume*this.levels.sfx);a.playbackRate=pitch??(name.startsWith('rifle')?.96+Math.random()*.08:1);
  a.play().catch(()=>{});this.counts[name]=(this.counts[name]||0)+1;
 }
 volley(army=8,mech=false){if(this.clock-this.lastVolley<.11)return;this.lastVolley=this.clock;const n=1+Math.floor(Math.random()*3);this.play(mech?'heavy':'rifle-'+n,.65);if(army>12)this.play('rifle-'+(n%3+1),.25);}
 weaponVolley(type,army=8){if(type==='laserCannon'){if(!['patrol','boss'].includes(this.mode))this.previewUntil=this.clock+.9;return;}const gap=type==='smg'?.07:type==='laserCannon'?.18:.1;if(this.clock-this.lastVolley<gap)return;this.lastVolley=this.clock;const sample=({assault:['gun-rifle',.4,1],pistol:['gun-pistol',.44,1],smg:['gun-smg',.28,1],rifle:['gun-rifle',.6,1],shotgun:['gun-shotgun',.55,1],laserCannon:['gun-laser',.22,1]})[type]||['gun-pistol',.4,1];const clip=type!=='laserCannon'&&this.variant++%2?sample[0]+'-alt':sample[0];this.play(clip,sample[1],.98+Math.random()*.04);if(army>16&&type!=='laserCannon')this.play(clip,sample[1]*.18,1.04);}
 effectSound(source){if(['bomb','orbitalBomb','boss'].includes(source))this.duckUntil=this.clock+(source==='orbitalBomb'?3.4:1.1);const sample=({sapper:['blast-grenade',.6],strafe:['air-strafe-cannon',.4],orbitalBarrage:['blast-grenade',.55],grenade:['blast-grenade',.4],orbitalBomb:['orbital-impact-v44',1],bomb:['airstrike-impact',.7],boss:['boss-impact',.55],enemy:['body-burst',.4],chain:['body-burst',.3],rocket:['blast-grenade',.5]})[source]||['blast-grenade',.3];this.play(...sample);}
 approach(type){const name=({bomb:'airstrike-flyby',strafe:'airstrike-flyby',orbitalBarrage:'orbital-incoming-v44',orbitalBomb:'orbital-incoming-v44',laser:'orbital-charge',mgTank:'airstrike-flyby',grenadeTank:'airstrike-flyby'})[type];if(name)this.play(name,type==='laser'?.16:type==='orbitalBomb'?.85:.45);}
 arrival(type){const sample=({strafe:'airstrike-flyby',energyShield:'emp-pulse',emp:'emp-pulse',barricade:'drop-land',mgTank:'drop-land',grenadeTank:'drop-land',lure:'lure-pulse'})[type];if(sample)this.play(sample,.4);}
 ui(action,step=0){this.unlocked=true;this.play('ui-'+action,action==='input'?.2:.32,action==='input'?1+(step%3)*.035:1);}
 creature(type){if(this.mechanical&&type==='giant'){if(this.clock-this.lastCreature>5){this.lastCreature=this.clock;this.play('mech-servo',.45);}return;}if(['robot','gunner','rocketeer','shieldbot','drone'].includes(type))return;if(type==='spitter')type='bloater';if(this.clock-this.lastCreature<(type==='giant'?5:4.5))return;this.lastCreature=this.clock;this.play('infected-'+type,type==='giant'?.82:.38);}
 toggle(){this.enabled=!this.enabled;if(!this.enabled){this.stopSpeech();this.stopLaser();for(const a of Object.values(this.tracks))a.pause();for(const list of this.pool.values())for(const a of list)a.pause();}return this.enabled;}
 setMode(mode){
  if(mode===this.mode)return;
  this.stopScorePreview();this.mode=mode;
  if(['paused','menu','ended','victory','defeat'].includes(mode))this.stopLaser();
  if(mode==='paused'){if(!this.dialogue)this.stopSpeech();for(const a of Object.values(this.tracks))a.pause();for(const list of this.pool.values())for(const a of list)a.pause();}
  if(mode==='boss'&&!this.bossAnnounced){this.bossAnnounced=true;this.tracks.boss.currentTime=0;this.lastCreature=-10;this.creature('giant');}
  if(mode==='ended')for(const a of Object.values(this.tracks))a.pause();
 }
 update(dt,mode,beams={}){
  this.clock+=dt;this.setMode(mode);if(this.noticeUntil&&this.clock>this.noticeUntil){const n=document.querySelector('#radioNotice');if(n)n.hidden=true;this.noticeUntil=0;}if(this.voiceCue&&!this.speech.paused){this.speech.volume=this.levels.voice;this.duckUntil=this.clock+.1;}const caption=document.querySelector('#radioNotice');if(caption&&this.dialogue)caption.hidden=true;const active=this.enabled&&this.unlocked&&(['patrol','boss'].includes(mode)&&(beams.orbital||beams.squad)||this.previewUntil>this.clock);const target=active?this.levels.sfx*Math.min(.28,(beams.orbital?.2:0)+(beams.squad?.13:0)+(this.previewUntil>this.clock?.15:0)):0;const bed=this.laserBed;bed.volume+=(target-bed.volume)*Math.min(1,dt*(active?9:15));if(target>0&&bed.paused){bed.playbackRate=1;bed.play().catch(()=>{});this.counts['laser-sustain-start']=(this.counts['laser-sustain-start']||0)+1;}if(!active&&bed.volume<.002){bed.pause();bed.volume=0;}
  if(this.scorePreview&&this.clock>=this.scorePreview.until)this.stopScorePreview();
  const musicMode=this.scorePreview?.mode||mode;
  if(!this.enabled||!this.unlocked)return;
  if(this.musicMode!==musicMode){this.musicMode=musicMode;if(['victory','defeat'].includes(musicMode)){this.oneShotStarted[musicMode]=false;this.tracks[musicMode].currentTime=0;}}
  for(const [name,a] of Object.entries(this.tracks)){
   const desired=name==='ambience'?(!this.scorePreview&&['patrol','boss'].includes(mode)?this.levels.ambience*.4:0):name===musicMode?this.levels.music*((this.dialogue||this.clock<this.duckUntil)?.22:musicMode==='menu'?.85:['victory','defeat'].includes(musicMode)?1:.8):0;
   a.volume+=(desired-a.volume)*Math.min(1,dt*3);
   const oneShot=['victory','defeat'].includes(name);
   if(desired>0&&a.paused&&!(oneShot&&this.oneShotStarted[name])){if(oneShot)this.oneShotStarted[name]=true;a.play().catch(()=>{if(oneShot)this.oneShotStarted[name]=false;});}
   if(desired===0&&a.volume<.003)a.pause();
  }
 }
 previewScore(mode){if(!this.scoreFiles[mode])return;this.enabled=true;this.unlocked=true;if(this.scorePreview?.mode===mode){this.stopScorePreview();return;}this.scorePreview={mode,until:this.clock+15};this.musicMode=null;this.tracks[mode].currentTime=0;this.syncScorePreview();}
 stopScorePreview(){this.scorePreview=null;this.syncScorePreview();}
 syncScorePreview(){document.querySelectorAll('[data-score]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.score===this.scorePreview?.mode)));}

 controls(){return`<div class="audio-panel"><span>声音</span>${[['sfx','枪声与效果'],['music','背景音乐'],['ambience','环境氛围'],['voice','无线电语音']].map(([id,name])=>`<label>${name}<input type="range" min="0" max="1" step="0.05" data-mix="${id}" value="${this.levels[id]}" aria-label="${name}音量"></label>`).join('')}<div class="music-audition"><span>\u914d\u4e50\u8bd5\u542c</span><div>${[['menu','\u4e3b\u9875'],['patrol','\u6218\u6597'],['boss','Boss'],['victory','\u80dc\u5229'],['defeat','\u6218\u8d25']].map(([id,name])=>`<button data-score="${id}" aria-pressed="false">${name}</button>`).join('')}</div></div></div>`;}
 bind(){document.querySelectorAll('[data-score]').forEach(el=>el.onclick=()=>this.previewScore(el.dataset.score));this.syncScorePreview();document.querySelectorAll('[data-mix]').forEach(e=>e.addEventListener('input',()=>{this.levels[e.dataset.mix]=Number(e.value);this.save();}));}
 snapshot(){return{mode:this.mode,musicMode:this.musicMode,preview:this.scorePreview?.mode||null,enabled:this.enabled,levels:{...this.levels},counts:{...this.counts},voice:{cue:this.voiceCue,queue:[...this.voiceQueue],paused:this.speech.paused,error:this.speech.error?.code??null},laser:{paused:this.laserBed.paused,time:this.laserBed.currentTime,volume:this.laserBed.volume,loop:this.laserBed.loop,error:this.laserBed.error?.code??null},tracks:Object.fromEntries(Object.entries(this.tracks).map(([k,v])=>[k,{src:v.currentSrc||v.src,loop:v.loop,paused:v.paused,time:v.currentTime,volume:v.volume,error:v.error?.code??null}]))};}
}
window.EmberSound=new Soundscape();
})();
