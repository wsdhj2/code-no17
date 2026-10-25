from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8-sig')
s=s.replace("damage:16,rate:1.4", "damage:9,rate:1.4").replace("damage:4,rate:7", "damage:2.4,rate:6.5").replace("damage:44,rate:.72", "damage:28,rate:.65").replace("damage:7,rate:1.05", "damage:4.2,rate:.9").replace("damage:20,rate:10", "damage:10.5,rate:10")
pos=s.index('const TYPES=')
s=s[:pos]+'''const CHAPTER_MISSIONS=[
 ['封锁线','铁棺封锁'],
 ['急诊入口','住院楼','缝合室'],
 ['输送管廊','熔炉核心'],
 ['集装箱区','装卸通道','沉锚码头'],
 ['外围防线','最后通道','撤离行动']
];
const STAGES=[];
for(let chapter=0;chapter<5;chapter++)CHAPTER_MISSIONS[chapter].forEach((name,part)=>{const boss=part===CHAPTER_MISSIONS[chapter].length-1;STAGES.push({id:STAGES.length,chapter,part,name,code:`${chapter+1}-${part+1}`,boss,duration:boss?16:part===0?40:44});});
function stageFor(chapter,part=0){return STAGES.find(s=>s.chapter===chapter&&s.part===part)||STAGES[0];}
''' +s[pos:]
s=s.replace("this.level=clamp(options.level||0,0,4);this.unlockedLevel", "this.level=clamp(options.level||0,0,4);const selected=STAGES[options.stageId]||stageFor(this.level,options.part||0);this.stageId=selected.id;this.level=selected.chapter;this.part=selected.part;this.unlockedLevel")
s=s.replace("this.army=8;this.damage=5", "this.army=8;this.members=[];this.memberId=0;this.damage=5")
s=s.replace("this.spawnRescue(0,233,4,112);this.spawnHorde(1,145,5,0);", "this.syncMembers();this.restoreCheckpoint(options.checkpoint);this.spawnRescue(0,233,4,100);this.spawnHorde(1,145,8,0);")
s=s.replace("formation(){const out=[]", "formation(){this.syncMembers();const out=[]")
s=s.replace("special:i<this.specialists,index:i", "special:i<this.specialists,index:i,id:this.members[i].id,hp:this.members[i].hp")
s=s.replace("this.damage=Math.min(12,this.damage*1.22)","this.damage=Math.min(8.5,this.damage*1.15)").replace("this.rate=Math.min(4.3,this.rate*1.18)","this.rate=Math.min(3.44,this.rate*1.12)")
s=s.replace("hp:TYPES[type].hp*(1+stage*.32)*(1+.018*Math.max(0,this.wave-4)**2),max:TYPES[type].hp*(1+stage*.32)*(1+.018*Math.max(0,this.wave-4)**2)","hp:TYPES[type].hp*(1+stage*.14)*(1+.04*Math.max(0,this.wave-5)),max:TYPES[type].hp*(1+stage*.14)*(1+.04*Math.max(0,this.wave-5))")
s=s.replace("142+w*29+Math.max(0,w-4)**2*4", "110+w*14").replace("145+w*34+Math.max(0,w-4)**2*5", "105+w*15")
s=s.replace("this.spawnHorde(1-lane,100,5+stage*2,stage)","this.spawnHorde(1-lane,100,9+stage*3,stage)")
s=s.replace("this.nextWave+=5.5", "this.nextWave+=4.4")
s=s.replace("this.time<END-7", "this.time<this.mission().duration-7")
s=s.replace("if(!this.bossSpawned&&this.time>=END)", "if(!this.bossSpawned&&this.mission().boss&&this.time>=this.mission().duration)")
s=s.replace("if(o.type==='giant'){this.bossKilled=true;if(this.level===4)this.win();else{this.state='cleared';this.emit('levelClear',{level:this.level});}}", "if(o.type==='giant'){this.bossKilled=true;this.completeStage();}")
s=s.replace("if(o.type==='bloater')this.area(o.x,o.y,85,125,'chain');", "if(o.type==='bloater'){this.area(o.x,o.y,85,125,'chain');this.damageSquadArea(o.x,o.y,75,2,'burst');}")
a=s.index(' casualty(count,o)');b=s.index('\n shoot(){',a)
s=s[:a]+''' syncMembers(){if(!this.members)this.members=[];while(this.members.length<this.army)this.members.push({id:++this.memberId,hp:2});if(this.members.length>this.army)this.members.length=this.army;}
 mission(){return STAGES[this.stageId];}
 completeStage(){if(this.state!=='playing')return;if(this.stageId===STAGES.length-1)this.win();else{this.state='cleared';this.emit('levelClear',{level:this.level,stageId:this.stageId});}}
 checkpoint(){const next=STAGES[this.stageId+1];if(this.state!=='cleared'||!next||next.chapter!==this.level)return null;this.syncMembers();return{chapter:this.level,stageId:next.id,army:this.army,members:this.members.map(m=>({...m})),damage:this.damage,rate:this.rate,weapon:this.weapon,inventory:this.inventory.map(s=>s?{...s}:null),loadout:[...this.loadout],heavySpent:[...this.heavySpent],score:this.score,kills:this.kills,rescued:this.rescued,casualties:this.casualties,peak:this.peak};}
 restoreCheckpoint(cp){if(!cp||cp.chapter!==this.level||cp.stageId!==this.stageId||this.part===0)return false;this.army=clamp(Number(cp.army)||8,1,MAX_SQUAD);this.members=(cp.members||[]).slice(0,this.army).map(m=>({id:++this.memberId,hp:clamp(Number(m.hp)||2,1,2)}));this.syncMembers();this.damage=clamp(Number(cp.damage)||5,5,8.5);this.rate=clamp(Number(cp.rate)||2.15,2.15,3.44);this.loadout=normalizeLoadout(cp.loadout);this.heavySpent=(cp.heavySpent||[]).filter(id=>this.loadout.includes(id));this.inventory=(cp.inventory||[]).map(s=>s&&ITEMS[s.type]&&(ITEMS[s.type].category==='field'||this.loadout.includes(s.type)&&!this.heavySpent.includes(s.type))?{type:s.type,count:ITEMS[s.type].category==='heavy'?1:Math.max(1,Math.floor(Number(s.count)||1))}:null);this.setWeapon(cp.weapon||this.weapon);for(const key of ['score','kills','rescued','casualties','peak'])this[key]=Math.max(0,Number(cp[key])||0);return true;}
 casualty(count,o,options={}){if((this.attackGrace>0&&!options.area)||this.state!=='playing')return;this.syncMembers();if(!options.ignoreProtection){const shield=this.effects.find(e=>e.type==='energyShield'&&e.hp>0);if(shield){shield.hp=Math.max(0,shield.hp-count*100);this.attackGrace=.65;o.cd=1.4;this.emit('shieldAbsorb',{x:this.x,y:620});return;}const vehicle=this.effects.find(e=>(e.type==='mgTank'||e.type==='grenadeTank')&&e.hp>0&&Math.abs(e.x-this.x)<68);if(vehicle){vehicle.hp=Math.max(0,vehicle.hp-count*95);this.attackGrace=.65;o.cd=1.4;this.emit('vehicleHit',{x:vehicle.x,y:vehicle.y,destroyed:vehicle.hp===0});return;}}
 const n=Math.min(this.army,count),indices=options.indices||Array.from({length:n},(_,i)=>i),formation=this.formation(),positions=indices.slice(0,n).map(i=>formation[i]).filter(Boolean);this.members=this.members.filter((_,i)=>!indices.includes(i));this.army-=n;this.casualties+=n;this.specialists=Math.min(this.specialists,this.army);this.attackGrace=.65;this.emit('casualty',{count:n,x:this.x,y:620,positions});o.y=Math.max(520,o.y-28);o.cd=1.8;if(this.army===0){this.state='lost';this.emit('end',{win:false});}}
 damageSquadArea(x,y,radius,damage=1,kind='acid',rect=false){if(this.state!=='playing')return 0;const hit=this.formation().filter(s=>rect?Math.abs(s.x-x)<=radius&&Math.abs(s.y-y)<=78:Math.hypot(s.x-x,s.y-y)<=radius);if(!hit.length)return 0;const shield=this.effects.find(e=>e.type==='energyShield'&&e.hp>0);if(shield){shield.hp=Math.max(0,shield.hp-hit.length*damage*50);this.emit('shieldAbsorb',{x:this.x,y:620});return 0;}for(const tank of this.effects.filter(e=>e.hp>0&&(e.type==='mgTank'||e.type==='grenadeTank')))if(Math.hypot(tank.x-x,tank.y-y)<radius+32)tank.hp=Math.max(0,tank.hp-damage*75);for(const unit of hit)this.members[unit.index].hp-=damage;const killed=hit.filter(s=>this.members[s.index].hp<=0).map(s=>s.index);this.emit('areaHit',{x,y,kind,affected:hit.length,killed:killed.length});if(killed.length)this.casualty(killed.length,{y,cd:0},{area:true,indices:killed,ignoreProtection:true});return killed.length;}
''' +s[b:]
s=s.replace("if(e.type==='acidPool'&&e.age>=e.delay){e.tick-=dt;if(e.tick<=0&&Math.hypot(this.x-e.x,624-e.y)<e.radius+20){e.tick=1.15;this.casualty(1,{y:600,cd:0});}}", "if(e.type==='acidPool'&&e.age>=e.delay){e.tick-=dt;if(e.tick<=0){e.tick=1.15;this.damageSquadArea(e.x,e.y,e.radius,1,'acid');}}")
s=s.replace("if(Math.abs(this.x-e.x)<e.radius+16)this.casualty(e.damage,{y:600,cd:0});", "this.damageSquadArea(e.x,e.y,e.radius,2,'blast',true);")
s=s.replace("this.casualty(o.type==='giant'?3:o.type==='bloater'?2:1,o);if(o.type==='bloater')o.dead=true;", "if(o.type==='bloater'){this.damageSquadArea(o.x,o.y+18,72,2,'burst');o.dead=true;this.emit('explosion',{x:o.x,y:o.y,radius:72,source:'enemy'});}else this.casualty(o.type==='giant'?3:1,o);")
a=s.index(' nextLevel(options=');b=s.index('\n win()',a)
s=s[:a]+''' nextLevel(options={}){if(this.state!=='cleared'||!STAGES[this.stageId+1])return false;const next=STAGES[this.stageId+1],crossChapter=next.chapter!==this.level;this.stageId=next.id;this.level=next.chapter;this.part=next.part;this.unlockedLevel=Math.max(this.level,this.unlockedLevel);if(crossChapter){this.army=8;this.members=[];this.damage=5;this.rate=2.15;this.specialists=0;this.loadout=normalizeLoadout(options.loadout??this.loadout);this.heavySpent=[];this.inventory=[{type:'bomb',count:1},...this.loadout.map(type=>({type,count:1}))];this.mech=0;this.lock=0;}this.setWeapon(options.weapon||this.weapon);this.syncMembers();this.time=0;this.wave=0;this.nextWave=3.5;this.bossSpawned=false;this.bossKilled=false;this.entities=[];this.effects=crossChapter?[]:this.effects.filter(e=>['energyShield','mgTank','grenadeTank'].includes(e.type)&&e.hp>0);this.bullets=[];this.joins=[];this.attackGrace=1;this.state='playing';this.peak=Math.max(this.peak,this.army);this.spawnRescue(0,233,4,100);this.spawnHorde(1,145,8,Math.min(2,Math.floor(this.level/2)));return true;}
''' +s[b:]
s=s.replace("this.entities=this.entities.filter(o=>!o.dead);", "this.entities=this.entities.filter(o=>!o.dead);if(!this.mission().boss&&this.time>=this.mission().duration&&!this.entities.some(o=>TYPES[o.type]))this.completeStage();")
s=s.replace("level:this.level,map:LEVELS[this.level].name", "level:this.level,stageId:this.stageId,part:this.part,mission:{...this.mission()},wounded:this.members.filter(m=>m.hp<2).length,map:LEVELS[this.level].name")
s=s.replace("WEAPONS,normalizeLoadout,TYPES,LEVELS,END", "WEAPONS,normalizeLoadout,TYPES,LEVELS,STAGES,stageFor,END")
p.write_text(s,encoding='utf-8')
