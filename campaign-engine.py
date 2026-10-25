from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8-sig');s=s.replace('END=132','END=65')
pos=s.index('const TYPES=')
s=s[:pos]+'''const LEVELS=[
{name:'封锁公路',boss:'铁棺·围城者',kind:'smash',color:'#b6a06a',hp:4200},
{name:'废弃医院',boss:'疫母·白衣',kind:'acid',color:'#91b69c',hp:4800},
{name:'化工厂',boss:'熔炉·重锤',kind:'charge',color:'#d89461',hp:5600},
{name:'货运港',boss:'沉锚·甲壳',kind:'artillery',color:'#81abb8',hp:6200},
{name:'撤离基地',boss:'黑冠·指挥官',kind:'final',color:'#ce9a79',hp:7200}];
''' +s[pos:]
s=s.replace("giant:{hp:6400", "spitter:{hp:76,speed:25,score:32,r:17},giant:{hp:6400")
s=s.replace("this.state='playing';this.time=0", "this.level=clamp(options.level||0,0,4);this.state='playing';this.time=0")
s=s.replace("if(stage>0&&i===count-1&&this.wave%3===0)type='bloater';", "if(stage>0&&i===count-1&&this.wave%3===0)type='bloater';if(i===1&&(this.wave%2===1||this.level>0))type='spitter';")
s=s.replace("stage=Math.min(3,Math.floor(w/5))", "stage=Math.min(3,Math.floor(w/5)+Math.floor(this.level/2))")
s=s.replace("if(o.type==='giant'){this.bossKilled=true;this.win();}", "if(o.type==='giant'){this.bossKilled=true;if(this.level===4)this.win();else{this.state='cleared';this.emit('levelClear',{level:this.level});}}")
s=s.replace("o.hp-=damage;o.hit=.09;", "if(o.type==='giant'&&o.recover>0)damage*=1.45;o.hp-=damage;o.hit=.09;")
a=s.index(" if(!this.bossSpawned&&this.time>=END)");b=s.index('\n for(const e of this.effects)',a)
s=s[:a]+''' if(!this.bossSpawned&&this.time>=END){this.bossSpawned=true;const map=LEVELS[this.level];this.entities=this.entities.filter(o=>o.type==='rescue'||o.type==='shield');this.unit('giant',216,270,{hp:map.hp,max:map.hp,attackTimer:3,phase:1,recover:0,pattern:0});this.nextWave=this.time+12;this.bossSupply=this.time+18;this.emit('boss',{name:map.boss});}
 if(this.bossSpawned&&!this.bossKilled&&this.time>=this.nextWave){this.wave++;this.spawnHorde(1,100,3,1);this.nextWave=this.time+14;}
 if(this.bossSpawned&&!this.bossKilled&&this.time>=this.bossSupply){for(const type of ['bomb','strafe','laser','emp'])this.giveItem(type);this.bossSupply=this.time+22;this.emit('resupply');}
''' +s[b:]
s=s.replace("for(const e of this.effects){e.age+=dt;", """for(const e of this.effects){e.age+=dt;
 if(e.type==='acidPool'&&e.age>=e.delay){e.tick-=dt;if(e.tick<=0&&Math.hypot(this.x-e.x,624-e.y)<e.radius+20){e.tick=1.15;this.casualty(1,{y:600,cd:0});}}
 if(e.type==='bossStrike'&&e.age>=e.delay&&!e.detonated){e.detonated=true;this.emit('explosion',{x:e.x,y:e.y,radius:e.radius,source:'boss'});if(Math.abs(this.x-e.x)<e.radius+16)this.casualty(e.damage,{y:600,cd:0});}
""")
s=s.replace("const motion=dt*(o.slow>0?.22:1);", """if(o.type==='spitter'){if(o.y<330)o.y+=o.speed*dt;else{o.spit=(o.spit??1.2)-dt;if(o.spit<=0){o.spit=5;this.acid(this.x,623,56,1.3);this.emit('spit',{x:o.x,y:o.y});}}continue;}
 if(o.type==='giant'&&this.bossSpawned){this.bossStep(o,dt);continue;}
 const motion=dt*(o.slow>0?.22:1);""")
pos=s.index(' win(){')
s=s[:pos]+''' acid(x,y,radius=60,delay=1.3){this.effects.push({id:++this.id,type:'acidPool',x,y,radius,delay,age:0,duration:delay+5.5,tick:0});}
 strike(x,radius=65,delay=1.5,damage=2){this.effects.push({id:++this.id,type:'bossStrike',x,y:624,radius,delay,age:0,duration:delay+.55,damage,detonated:false});}
 bossStep(o,dt){o.recover=Math.max(0,(o.recover||0)-dt);o.phase=o.hp/o.max<.5?2:1;if(o.phase===2&&!o.enraged){o.enraged=true;this.emit('enrage');}o.x+=(clamp(this.x,110,322)-o.x)*dt*.22;o.y=270+Math.sin(o.age*.8)*10;o.attackTimer-=dt;if(o.attackTimer>0)return;const kind=LEVELS[this.level].kind,seq=o.pattern++;o.attackTimer=o.phase===2?3.8:5.1;o.recover=2.3;
 if(kind==='smash'){this.strike(this.x,72,o.phase===2?1.15:1.6,2);}
 if(kind==='acid'){this.acid(this.x,624,65,1.5);if(o.phase===2)this.acid(this.x<216?326:106,540,50,2);}
 if(kind==='charge'){this.strike(this.x,52,1.3,3);o.chargeX=this.x;o.chargeUntil=o.age+1.9;}
 if(kind==='artillery'){for(let i=0;i<3;i++)this.effects.push({id:++this.id,type:'bossStrike',x:72+i*144,y:624,radius:44,delay:1.2+i*.65,age:0,duration:3.2,damage:2,detonated:false});}
 if(kind==='final'){if(seq%3===0){this.acid(this.x<216?326:106,624,65,1.1);this.strike(this.x,58,1.8,3);}else if(seq%3===1){this.strike(106,66,1.3,2);this.strike(326,66,2.4,2);}else{this.spawnHorde(1,190,4,2);this.strike(this.x,60,1.7,2);}}
 this.emit('bossAttack',{kind});}
 nextLevel(){if(this.state!=='cleared')return false;this.level++;this.time=0;this.wave=0;this.nextWave=3.5;this.bossSpawned=false;this.bossKilled=false;this.entities=[];this.effects=[];this.bullets=[];this.joins=[];this.attackGrace=1;this.state='playing';this.army=Math.min(MAX_SQUAD,Math.max(this.army,8)+4);this.peak=Math.max(this.peak,this.army);for(const type of Object.keys(ITEMS))this.giveItem(type);this.spawnRescue(0,233,4,130);this.spawnHorde(1,145,5,1);return true;}
''' +s[pos:]
s=s.replace("return{state:this.state,seed", "return{state:this.state,level:this.level,map:LEVELS[this.level].name,seed")
s=s.replace("windup:o.windup}","windup:o.windup,phase:o.phase,recover:o.recover}")
s=s.replace('Run,LANES,ITEMS,TYPES,END','Run,LANES,ITEMS,TYPES,LEVELS,END')
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace('raw*((aim||command)?.25:1)','raw*(aim?.25:1)').replace('timeScale:(aim||command)?.25:1','timeScale:aim?.25:1');p.write_text(s,encoding='utf-8')
