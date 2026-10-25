from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8');s=s.replace("lure:{name:","mgTank:{name:'机枪战车',short:'机枪车',desc:'前排锁敌射击并抗伤害',radius:40,color:'#c8c18c',pattern:[6,3,0,4,8]},\ngrenadeTank:{name:'榴弹战车',short:'榴弹车',desc:'前排范围轰炸并抗伤害',radius:55,color:'#d8ac79',pattern:[8,5,2,4,6]},\nlure:{name:")
s=s.replace("'mech','rate']","'mgTank','grenadeTank','mech','rate']")
s=s.replace('max:type===\'barricade\'?280:0,detonated:false','max:type===\'barricade\'?280:0,detonated:false')
s=s.replace("this.emit('deploy',{item:type,x,y});return true;", "const e=this.effects[this.effects.length-1];if(type==='mgTank'||type==='grenadeTank'){e.x=this.x;e.y=562;e.hp=e.max=type==='mgTank'?520:620;e.ammo=type==='mgTank'?90:18;e.duration=9999;e.tick=.5;}this.emit('deploy',{item:type,x,y});return true;")
s=s.replace("this.effects.push({id:++this.id,type,x,y,angle", "if((type==='mgTank'||type==='grenadeTank')&&this.effects.some(e=>e.type===type&&e.hp>0))return false;this.effects.push({id:++this.id,type,x,y,angle")
# Above must validate active BEFORE consume.
s=s.replace("const type=this.inventory[slot].type;this.inventory[slot]=null;if((type", "const type=this.inventory[slot].type;if((type")
s=s.replace("e.type===type&&e.hp>0))return false;this.effects.push", "e.type===type&&e.hp>0))return false;this.inventory[slot]=null;this.effects.push")
s=s.replace("casualty(count,o){if(this.attackGrace", "casualty(count,o){if(this.attackGrace")
s=s.replace("const n=Math.min(this.army,count);this.army-=n;", "const vehicle=this.effects.find(e=>(e.type==='mgTank'||e.type==='grenadeTank')&&e.hp>0&&Math.abs(e.x-this.x)<68);if(vehicle){vehicle.hp=Math.max(0,vehicle.hp-count*95);this.attackGrace=.65;o.cd=1.4;this.emit('vehicleHit',{x:vehicle.x,y:vehicle.y,destroyed:vehicle.hp===0});return;}const n=Math.min(this.army,count);this.army-=n;")
s=s.replace("if(!wall)return false;", "if(!wall){const tank=this.effects.find(e=>(e.type==='mgTank'||e.type==='grenadeTank')&&e.hp>0&&Math.abs(o.x-e.x)<55+o.r&&o.y>e.y-45);if(!tank)return false;o.y=tank.y-45;o.windup=0;tank.hp=Math.max(0,tank.hp-dt*(o.type==='giant'?75:18));return true;}")
s=s.replace("for(const e of this.effects){e.age+=dt;", """for(const e of this.effects){e.age+=dt;
 if(e.type==='mgTank'||e.type==='grenadeTank'){e.x+=(this.x-e.x)*Math.min(1,dt*9);e.y=562;e.tick-=dt;if(e.hp>0&&e.ammo>0&&e.tick<=0){const target=this.entities.filter(o=>!o.dead&&TYPES[o.type]&&o.y<540).sort((a,b)=>Math.hypot(a.x-e.x,a.y-e.y)-Math.hypot(b.x-e.x,b.y-e.y))[0];if(target){e.targetX=target.x;e.targetY=target.y;e.ammo--;e.tick=e.type==='mgTank'?.12:.8;e.firing=.08;if(e.type==='mgTank')this.hurt(target,15,'vehicle');else this.area(target.x,target.y,58,92,'grenade');}}e.firing=Math.max(0,(e.firing||0)-dt);}
""")
s=s.replace("(e.type!=='barricade'||e.hp>0)","(!['barricade','mgTank','grenadeTank'].includes(e.type)||e.hp>0)")
s=s.replace("age:e.age,hp:e.hp}","age:e.age,hp:e.hp,ammo:e.ammo,max:e.max}")
p.write_text(s,encoding='utf-8')
