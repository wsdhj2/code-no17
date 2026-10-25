/* Optional fifth-chapter signal restoration. Main route IDs stay stable. */
(function(root,factory){if(typeof module==='object')module.exports=factory(require('./engine'));else root.EmberSignal=factory(root.Frontline);})(globalThis,function(F){
'use strict';
const MISSIONS={engineers:{id:'signal-1',chapter:4,part:0,name:'失联的工程组',code:'支-1',boss:false,duration:100},tower:{id:'signal-2',chapter:4,part:1,name:'重启广播',code:'支-2',boss:true,duration:155,bossAt:99999}};
const REPAIR_PATTERN=[0,1,4,7,8],REPAIR_SECONDS=85,APPROACH_SECONDS=42;
F.ITEMS.reinforcements={name:'车队增援',short:'增援',desc:'卡车送来20名幸存者，每小节一次',category:'fixed',arrival:3,radius:0,color:'#cbb37a',pattern:[2,5,8,7,6,3,4]};
const Base=F.Run;
class SignalRun extends Base{
 constructor(options={}){super(options);this.reinforcementUnlocked=options.reinforcementUnlocked===true;this.reinforcementUsed=false;this.ensureReinforcement();if(MISSIONS[options.branch]){this.branch=options.branch;this.level=4;this.stageId=9;this.part=MISSIONS[this.branch].part;this.time=0;this.nextWave=7;this.entities=[];this.effects=[];this.events=[];this.joins=[];this.bossSpawned=false;this.bossKilled=false;this.bossWarned=false;this.extractionAt=null;this.engineerRescued=false;this.engineerSpawnAt=25;this.repairStartedAt=null;this.openingWave();}}
 mission(){if(!this.branch)return super.mission();const m=MISSIONS[this.branch];if(this.branch==='tower')return {...m,duration:this.repairStartedAt==null?99999:this.repairStartedAt+REPAIR_SECONDS,bossAt:this.repairStartedAt==null?99999:this.repairStartedAt+30};return {...m};}
 bossMap(){return this.branch==='tower'?{name:'旧城信号站',boss:'聚群者 · 回声',kind:'smash',color:'#c6ab72',hp:12000}:super.bossMap();}
 difficultyProfile(){const profile=super.difficultyProfile();return this.branch?{...profile,pace:profile.pace*.8}:profile;}
 roadSpeed(){return this.branch==='tower'&&this.time>=APPROACH_SECONDS?0:F.ROAD_SPEED;}
 sceneryTime(){return this.branch==='tower'?Math.min(this.time,APPROACH_SECONDS):this.time;}
 openingWave(){if(!this.branch)return super.openingWave();this.spawnRescue(2,245,4);this.spawnFlanks(8,0,135);}
 spawnWave(){if(!this.branch)return super.spawnWave();const w=this.wave++,defending=this.branch==='tower'&&this.repairStartedAt!=null,stage=defending?1:this.time<25?0:this.time<65?1:2;if(w%4===0)this.spawnRescue(2,105,4);else{const rewards=['bomb','rate','strafe','power','bomb','emp'];const reward=rewards[(w-1)%rewards.length];if(F.ITEMS[reward]){if(this.random()<.85)this.spawnShield(2,105,this.fieldReward());}else this.spawnShield(2,105,reward);}const count=defending?18+Math.min(8,Math.floor((this.time-this.repairStartedAt)/18)*2):12+Math.min(6,Math.floor(this.time/28)*2);this.spawnFlanks(count,stage,110);}
 ensureReinforcement(){if(!this.reinforcementUnlocked)return;const fixed=this.inventory.find(s=>s?.type==='reinforcements');if(!fixed)this.inventory.push({type:'reinforcements',count:this.reinforcementUsed?0:1});}
 refreshHeavySupport(){super.refreshHeavySupport();this.ensureReinforcement();}
 nextLevel(options={}){this.reinforcementUsed=false;const ok=super.nextLevel(options);if(ok)this.ensureReinforcement();return ok;}
 giveItem(type){if(type==='reinforcements')return false;return super.giveItem(type);}
 deploy(slot,x,y,angle){if(this.inventory[slot]?.type!=='reinforcements')return super.deploy(slot,x,y,angle);if(this.state!=='playing'||!this.reinforcementUnlocked||this.reinforcementUsed||this.inventory[slot].count<1)return false;this.reinforcementUsed=true;this.inventory[slot].count=0;this.effects.push({id:++this.id,type:'reinforcementTruck',age:0,duration:7,x:350,y:660,arrival:0,delivered:false});this.emit('deploy',{item:'reinforcements',x:350,y:660,arrival:3});return true;}
 hurt(o,...args){const wasAlive=!o.dead;super.hurt(o,...args);if(wasAlive&&o.dead&&o.type==='giant'&&this.branch==='tower')this.extractionAt=this.mission().duration;if(wasAlive&&o.dead&&o.engineer){this.engineerRescued=true;this.emit('engineerRescued');}}
 beginRepair(path){if(this.branch!=='tower'||!this.consoleReady||this.repairStartedAt!=null||this.state!=='playing'||path.join(',')!==REPAIR_PATTERN.join(','))return false;this.repairStartedAt=this.time;this.nextWave=Math.min(this.nextWave,this.time+1);this.emit('repairStarted');return true;}
 completeStage(){if(this.branch==='engineers'&&!this.engineerRescued)return;if(this.branch==='tower'&&(this.repairStartedAt==null||this.time<this.repairStartedAt+REPAIR_SECONDS||!this.bossKilled))return;super.completeStage();}
 sideCheckpoint(){this.syncMembers();return{chapter:4,stageId:9,army:this.army,members:this.members.map(m=>({...m})),damage:this.damage,rate:this.rate,weapon:this.weapon,inventory:this.inventory.filter(s=>s&&F.ITEMS[s.type]?.category==='field').map(s=>({...s})),loadout:[...this.loadout],heavySpent:[],score:this.score,kills:this.kills,rescued:this.rescued,casualties:this.casualties,peak:this.peak,effects:[]};}
 step(dt){if(this.state!=='playing')return;const stationary=this.roadSpeed()===0,step=Math.max(0,Math.min(.025,dt));super.step(dt);if(stationary)for(const o of this.entities)if(o.type==='rescue'||o.type==='shield')o.y-=F.ROAD_SPEED*step;if(stationary)for(const e of this.effects)if(['bilePool','acidPool'].includes(e.type)&&e.age>=e.delay)e.y-=F.ROAD_SPEED*step;
  for(const e of this.effects)if(e.type==='reinforcementTruck'&&e.age>=3&&!e.delivered){e.delivered=true;this.joins.push({x:350,y:660,age:0,count:20,duration:1.4});this.emit('reinforcementArrived',{count:20});}
  if(this.branch==='engineers'&&!this.engineerRescued&&this.time>=this.engineerSpawnAt&&!this.entities.some(o=>o.engineer&&!o.dead)){this.spawnRescue(2,135,4,this.resourceHp(2));this.entities.at(-1).engineer=true;this.engineerSpawnAt=this.time+12;this.emit('engineerLocated');}
  if(this.branch==='tower'&&!this.consoleReady&&this.time>=APPROACH_SECONDS){this.consoleReady=true;this.emit('towerConsole');}
  if(this.branch==='tower'&&this.repairStartedAt!=null&&!this.repairComplete&&this.time>=this.repairStartedAt+REPAIR_SECONDS){this.repairComplete=true;this.emit('broadcastRestored');}
  if(this.state==='playing'&&!this.joins.length&&(this.branch==='engineers'&&this.engineerRescued&&this.time>=MISSIONS.engineers.duration||this.branch==='tower'&&this.repairComplete&&this.bossKilled))this.completeStage();
 }
 snapshot(){return {...super.snapshot(),branch:this.branch||null,reinforcementUnlocked:this.reinforcementUnlocked,reinforcementUsed:this.reinforcementUsed,engineerRescued:this.engineerRescued||false,consoleReady:!!this.consoleReady,repairProgress:this.repairStartedAt==null?0:Math.min(1,(this.time-this.repairStartedAt)/REPAIR_SECONDS),stationary:this.roadSpeed()===0};}
}
F.Run=SignalRun;
const towerImage=typeof Image==='undefined'?null:new Image();
if(towerImage)towerImage.src='assets/signal-station-v71.png';
function drawTower(g,run){
 if(run.branch!=='tower')return;
 const t=run.sceneryTime(),y=718-Math.max(0,APPROACH_SECONDS-t)*30;
 if(y<-80||!towerImage?.complete||!towerImage.naturalWidth)return;
 const x=292,w=240,h=360,sy=g.canvas.spriteYRatio||1;
 g.save();g.imageSmoothingEnabled=true;g.imageSmoothingQuality='high';
 g.fillStyle='#02080c48';g.beginPath();g.ellipse(x-8,y-9,69,17,0,0,Math.PI*2);g.fill();
 g.drawImage(towerImage,x-w/2,y-h*sy,w,h*sy);
 // Only the lamps animate. Architecture and its contact shadow remain grounded.
 const tipY=y-h*sy+9*sy,pulse=.25+.35*(.5+.5*Math.sin(run.time*3));
 g.globalAlpha=pulse;g.fillStyle=run.repairComplete?'#8bd1ac':'#ff8964';
 g.beginPath();g.ellipse(x+3,tipY,2.6,2.6*sy,0,0,Math.PI*2);g.fill();
 g.globalAlpha=1;
 if(run.repairStartedAt!=null){const q=run.repairComplete?1:Math.min(1,(run.time-run.repairStartedAt)/REPAIR_SECONDS);g.fillStyle='#101b20';g.fillRect(x-9,y-65*sy,20,3*sy);g.fillStyle=run.repairComplete?'#a3cdb2':'#d3ae70';g.fillRect(x-9,y-65*sy,20*q,3*sy);}
 g.restore();
}
function drawTruck(g,e){
 const arrival=Math.min(1,e.age/3),departure=Math.max(0,e.age-5),xx=e.x+departure*100,yy=860-(860-e.y)*(1-(1-arrival)**2);
 if(typeof window!=='undefined'&&window.EmberVehicles?.draw(g,'truck',xx,yy,110,e.age,{moving:e.age<3||departure>0,unloading:e.age>=3&&e.age<5,angle:Math.min(1,departure/.5)*Math.PI/2}))return;
 const q=Math.min(1,e.age/3),exit=Math.max(0,e.age-5),x=e.x+exit*100,y=860-(860-e.y)*(1-(1-q)**2);g.save();g.translate(x,y);const box=(x,y,w,h,c)=>{g.fillStyle=c;g.fillRect(x,y,w,h);};box(-22,-60,44,101,'#101a21');box(-26,-44,8,20,'#0b141a');box(18,-44,8,20,'#0b141a');box(-26,15,8,19,'#0b141a');box(18,15,8,19,'#0b141a');box(-20,-56,40,32,'#9c9471');box(-16,-52,32,13,'#223a43');box(-13,-50,26,3,'#8ca9a9');box(-19,-23,38,61,'#4b615a');box(-16,-20,32,55,'#677265');for(let i=0;i<5;i++)box(-16,-15+i*10,32,2,'#384a47');box(-17,-58,9,3,'#ffe3a1');box(8,-58,9,3,'#ffe3a1');box(-17,35,8,3,'#cf654b');box(9,35,8,3,'#cf654b');if(e.age>3&&e.age<5){box(-17,39,34,6,'#8b957c');g.fillStyle='#c5b273';g.font='10px Microsoft YaHei';g.textAlign='center';g.fillText('+20',0,-72);}g.restore();}
return {MISSIONS,REPAIR_PATTERN,REPAIR_SECONDS,APPROACH_SECONDS,drawTower,drawTruck};
});
