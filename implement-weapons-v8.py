from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8')
s=s.replace("laser:{name:'轨道激光'", "orbitalBomb:{name:'轨道重轰炸',short:'重轰炸',desc:'大范围高伤害轨道打击',radius:180,color:'#e7ba71',pattern:[2,1,0,3,6,7,8]},\nenergyShield:{name:'能量护盾',short:'护盾',desc:'跟随队伍吸收伤害18秒',radius:85,color:'#8dd7e6',pattern:[0,1,2,5,8,7,6,3]},\nlaser:{name:'轨道激光'")
pos=s.index('const LEVELS=')
s=s[:pos]+'''const FIELD_ITEMS=['bomb','strafe','emp','barricade','lure'];
const HEAVY_ITEMS=['laser','orbitalBomb','energyShield','mgTank','grenadeTank'];
for(const [id,item] of Object.entries(ITEMS))item.category=HEAVY_ITEMS.includes(id)?'heavy':'field';
const WEAPONS={
pistol:{name:'手枪',unlock:0,damage:16,rate:1.4,speed:650,range:620,color:'#f4d59a',desc:'低射速 · 中等单发伤害'},
smg:{name:'冲锋枪',unlock:0,damage:4,rate:7,speed:740,range:570,color:'#f1bc6e',desc:'高射速 · 低单发伤害'},
rifle:{name:'大口径步枪',unlock:1,damage:44,rate:.72,speed:900,range:650,pierce:3,color:'#b4e4e7',desc:'低射速 · 高伤害 · 穿透3个目标'},
shotgun:{name:'霰弹枪',unlock:2,damage:7,rate:1.05,speed:650,range:270,pellets:7,color:'#f4a96f',desc:'扇形弹幕 · 近距离高爆发'},
laserCannon:{name:'激光炮',unlock:3,damage:20,rate:10,range:570,color:'#a5e5ec',desc:'全队聚能 · 攻速升级增加束宽与伤害'}};
function normalizeLoadout(input){return [...new Set(Array.isArray(input)?input:['laser','mgTank'])].filter(id=>HEAVY_ITEMS.includes(id)).slice(0,2);}
''' +s[pos:]
s=s.replace("this.state='playing';this.time=0", "this.unlockedLevel=Math.max(this.level,clamp(Number(options.unlocked)||0,0,4));this.weapon='pistol';this.setWeapon(options.weapon||'pistol');this.loadout=normalizeLoadout(options.loadout);this.state='playing';this.time=0")
s=s.replace("this.inventory=Object.keys(ITEMS).map(type=>({type,count:1}))", "this.inventory=[{type:'bomb',count:1},...this.loadout.map(type=>({type,count:1}))];this.heavySpent=[]")
s=s.replace("rewards=['power','strafe','rate','laser','emp','barricade','lure','bomb','mgTank','grenadeTank','mech','rate']", "rewards=['power','strafe','rate','emp','barricade','lure','bomb','power','rate','bomb']")
a=s.index(' giveItem(type)');b=s.index('\n resolveItem',a)
s=s[:a]+''' setWeapon(id){const weapon=WEAPONS[id];if(!weapon||weapon.unlock>this.unlockedLevel)return false;this.weapon=id;this.shotClock=0;return true;}
 weaponStats(){const w=WEAPONS[this.weapon],power=this.damage/5,speed=this.rate/2.15;return{...w,id:this.weapon,damage:w.damage*power,rate:w.rate*speed,rateScale:speed,power};}
 giveItem(type){if(!ITEMS[type]||ITEMS[type].category==='heavy')return false;const same=this.inventory.find(s=>s&&s.type===type);if(same)same.count++;else{const empty=this.inventory.indexOf(null);if(empty>=0)this.inventory[empty]={type,count:1};else this.inventory.push({type,count:1});}this.emit('loot',{reward:type});return true;}
''' +s[b:]
s=s.replace("!this.inventory[slot]||x<35", "!this.inventory[slot]||this.inventory[slot].count<1||x<35")
s=s.replace("this.inventory[slot]=null;this.effects.push", "if(ITEMS[type].category==='heavy'){if(this.heavySpent.includes(type))return false;this.heavySpent.push(type);}if(--this.inventory[slot].count===0)this.inventory[slot]=null;this.effects.push")
s=s.replace("({bomb:1.9,strafe:2.8,laser:6.8,emp:5,barricade:10.6,lure:6.5})", "({bomb:1.9,orbitalBomb:2.8,energyShield:18,strafe:2.8,laser:10,emp:5,barricade:10.6,lure:6.5})")
s=s.replace("?520:620", "?1100:1400").replace("?90:18", "?180:28")
s=s.replace("this.emit('deploy',{item:type,x,y});return true;", "if(type==='energyShield'){e.x=this.x;e.y=624;e.hp=e.max=1600;}this.emit('deploy',{item:type,x,y});return true;")
s=s.replace("const vehicle=this.effects.find", "const shield=this.effects.find(e=>e.type==='energyShield'&&e.hp>0);if(shield){shield.hp=Math.max(0,shield.hp-count*100);this.attackGrace=.65;o.cd=1.4;this.emit('shieldAbsorb',{x:this.x,y:620});return;}const vehicle=this.effects.find")
a=s.index(' shoot(){');b=s.index('\n block(o,dt)',a)
s=s[:a]+''' shoot(){
  const w=this.weaponStats();
  if(this.weapon==='laserCannon'){
   const width=5+Math.sqrt(this.army)*1.5*w.rateScale,damage=this.army*w.damage*.1*(1+.4*(w.rateScale-1));
   let beam=this.effects.find(e=>e.type==='squadBeam');if(!beam){beam={id:++this.id,type:'squadBeam',age:0};this.effects.push(beam);}Object.assign(beam,{x:this.x,y:573,width,duration:beam.age+.16});
   for(const o of [...this.entities])if(!o.dead&&o.y>100&&o.y<573&&Math.abs(o.x-this.x)<width/2+o.r)this.hurt(o,damage,'bullet');
  }else for(const soldier of this.formation()){
   const count=w.pellets||1;for(let i=0;i<count;i++){const angle=count>1?(i-(count-1)/2)*.055:0;this.bullets.push({id:++this.id,weapon:this.weapon,x:soldier.x+3,y:soldier.y-17,vx:Math.sin(angle)*w.speed,vy:-Math.cos(angle)*w.speed,damage:w.damage*(soldier.special?1.6:1)*(this.mech>0?1.7:1),age:0,special:false,range:w.range,travel:0,pierce:w.pierce||1,hitIds:[],color:w.color});}
  }
  if(this.mech>0)for(let i=-1;i<=1;i++)this.bullets.push({id:++this.id,x:this.x+i*18,y:584,vx:0,vy:-500,damage:22,age:0,special:false,range:600,travel:0,pierce:1,hitIds:[]});
  this.emit('shot',{weapon:this.weapon});
 }
''' +s[b:]
a=s.index(' nextLevel(){');b=s.index('\n win()',a)
s=s[:a]+''' nextLevel(options={}){if(this.state!=='cleared')return false;this.level++;this.unlockedLevel=Math.max(this.level,this.unlockedLevel);this.loadout=normalizeLoadout(options.loadout??this.loadout);this.heavySpent=[];this.inventory=[{type:'bomb',count:1},...this.loadout.map(type=>({type,count:1}))];this.setWeapon(options.weapon||this.weapon);this.time=0;this.wave=0;this.nextWave=3.5;this.bossSpawned=false;this.bossKilled=false;this.entities=[];this.effects=[];this.bullets=[];this.joins=[];this.attackGrace=1;this.state='playing';this.army=Math.min(MAX_SQUAD,Math.max(this.army,8)+4);this.peak=Math.max(this.peak,this.army);this.spawnRescue(0,233,4,130);this.spawnHorde(1,145,5,1);return true;}
''' +s[b:]
s=s.replace("for(const type of ['bomb','strafe','laser','emp'])this.giveItem(type);", "this.spawnShield(0,160,this.wave%2?'bomb':'strafe',220+this.level*40);")
s=s.replace("if(e.type==='mgTank'||e.type==='grenadeTank'){const escorts", "if(e.type==='energyShield'){e.x=this.x;e.y=624;}\n if(e.type==='orbitalBomb'&&e.age>=1.5&&!e.detonated){e.detonated=true;this.area(e.x,e.y,ITEMS.orbitalBomb.radius,5200,'orbitalBomb');}\n if(e.type==='squadBeam'){e.x=this.x;}\n if(e.type==='mgTank'||e.type==='grenadeTank'){const escorts")
s=s.replace("this.hurt(target,15,'vehicle')", "this.hurt(target,36,'vehicle')").replace("this.area(target.x,target.y,58,92,'grenade')", "this.area(target.x,target.y,75,230,'grenade')")
s=s.replace("target.type==='giant'?42:75", "target.type==='giant'?125:210")
s=s.replace("['barricade','mgTank','grenadeTank'].includes", "['barricade','mgTank','grenadeTank','energyShield'].includes")
s=s.replace("this.shotClock=1/(this.rate*(this.mech>0?1.3:1))", "this.shotClock=1/((this.weapon==='laserCannon'?10:this.weaponStats().rate)*(this.mech>0?1.3:1))")
a=s.index(' // Sweep each bullet');b=s.index('\n this.bullets=this.bullets.filter',a)
s=s[:a]+''' // Sweep and order all contacts. Only the large-caliber rifle can penetrate.
 for(const b of this.bullets){
  if(this.state!=='playing')break;
  const oldX=b.x,oldY=b.y; b.age+=dt;b.x+=b.vx*dt;b.y+=b.vy*dt;
  const dx=b.x-oldX,dy=b.y-oldY,length2=dx*dx+dy*dy,segment=Math.sqrt(length2),remaining=(b.range||650)-(b.travel||0);let rangeT=segment>0?Math.min(1,remaining/segment):1;
  const contacts=[];b.hitIds=b.hitIds||[];
  for(const o of this.entities){
   if(o.dead||o.y<112||b.hitIds.includes(o.id))continue;
   const ox=oldX-o.x,oy=oldY-o.y,radius=o.r+3,c=ox*ox+oy*oy-radius*radius;
   let contact=0;
   if(c>0){if(length2===0)continue;const dot=ox*dx+oy*dy,discriminant=dot*dot-length2*c;if(discriminant<0)continue;contact=(-dot-Math.sqrt(discriminant))/length2;if(contact<0||contact>rangeT)continue;}
   contacts.push({o,t:contact});
  }
  contacts.sort((a,b)=>a.t-b.t);
  for(const {o,t} of contacts){if(o.dead)continue;const hitX=oldX+dx*t,hitY=oldY+dy*t,travel=(b.travel||0)+segment*t,falloff=b.weapon==='shotgun'?(travel<120?1.7:travel<190?.75:.25):1;
   this.emit('bulletHit',{x:hitX,y:hitY});this.hurt(o,b.damage*falloff);b.hitIds.push(o.id);b.pierce=(b.pierce||1)-1;
   if(b.pierce<=0){b.x=hitX;b.y=hitY;b.dead=true;break;}b.damage*=.8;
  }
  b.travel=(b.travel||0)+segment;if(b.travel>=(b.range||650))b.dead=true;
 }
''' +s[b:]
s=s.replace("army:this.army,x:this.x", "army:this.army,weapon:this.weapon,weaponStats:this.weaponStats(),loadout:[...this.loadout],heavySpent:[...this.heavySpent],unlockedLevel:this.unlockedLevel,x:this.x",1)
s=s.replace("Run,LANES,ITEMS,TYPES,LEVELS,END", "Run,LANES,ITEMS,FIELD_ITEMS,HEAVY_ITEMS,WEAPONS,normalizeLoadout,TYPES,LEVELS,END")
p.write_text(s,encoding='utf-8')
