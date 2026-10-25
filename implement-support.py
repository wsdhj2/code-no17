from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8-sig')
a=s.index('const ITEMS=');b=s.index('\nconst TYPES',a)
s=s[:a]+'''const ITEMS={
bomb:{name:'高爆轰炸',short:'轰炸',desc:'圆形区域延迟轰炸',radius:106,color:'#e8c65e',pattern:[0,1,2,4,6,7,8]},
strafe:{name:'航空扫射',short:'扫射',desc:'拖出扫射方向',radius:32,color:'#e7b878',pattern:[6,3,0,1,2]},
laser:{name:'轨道激光',short:'激光',desc:'自动追踪搜索区内的敌人',radius:135,color:'#e6d894',pattern:[0,3,6,7,8,5,2]},
emp:{name:'电磁压制',short:'电磁',desc:'减速并打断区域内敌人',radius:120,color:'#8fcad5',pattern:[1,4,7]},
barricade:{name:'空投路障',short:'路障',desc:'阻挡丧尸10秒或被摧毁',radius:66,color:'#c7ba8e',pattern:[6,3,0,1,2,5,8]},
lure:{name:'声波诱饵',short:'诱饵',desc:'吸引普通丧尸6秒',radius:125,color:'#83d5da',pattern:[0,4,8]}};''' + s[b:]
s=s.replace("this.inventory=[{type:'bomb',count:1},null]","this.inventory=Object.keys(ITEMS).map(type=>({type,count:1}))")
s=s.replace("rewards=['power','barricade','rate','rate','lure','power','bomb','mech','power','rate']","rewards=['power','strafe','rate','laser','emp','barricade','lure','bomb','mech','rate']")
a=s.index(' giveItem(');b=s.index('\n reward(',a)
s=s[:a]+''' giveItem(type){if(!ITEMS[type])return;const same=this.inventory.find(s=>s&&s.type===type);if(same){this.emit('message',{text:'该支援已就绪'});return;}const empty=this.inventory.indexOf(null);if(empty>=0)this.inventory[empty]={type,count:1};else this.inventory.push({type,count:1});this.emit('loot',{reward:type});}
 resolveItem(){this.state='playing';this.pending=[];}
 deploy(slot,x,y,angle=-Math.PI/2){if(this.state!=='playing'||!this.inventory[slot]||x<35||x>397||y<115||y>570)return false;const type=this.inventory[slot].type;this.inventory[slot]=null;this.effects.push({id:++this.id,type,x,y,angle:Number.isFinite(angle)?angle:-Math.PI/2,age:0,tick:0,duration:({bomb:1.9,strafe:2.8,laser:6.8,emp:5,barricade:10.6,lure:6.5})[type],hp:type==='barricade'?280:0,max:type==='barricade'?280:0,detonated:false});this.emit('deploy',{item:type,x,y});return true;}
''' + s[b:]
a=s.index(' for(const e of this.effects){e.age+=dt;');b=s.index('\n this.effects=this.effects.filter',a)
s=s[:a]+''' for(const e of this.effects){e.age+=dt;
 if(e.type==='bomb'&&e.age>=.85&&!e.detonated){e.detonated=true;this.area(e.x,e.y,ITEMS.bomb.radius,440,'bomb');}
 if(e.type==='emp'&&e.age>.5)for(const o of this.entities)if(!o.dead&&o.type!=='shield'&&o.type!=='rescue'&&Math.hypot(o.x-e.x,o.y-e.y)<ITEMS.emp.radius){o.slow=.2;o.windup=0;}
 if(e.type==='strafe'&&e.age>=.7){const t=clamp((e.age-.7)/1.6,0,1);e.beamX=e.x+Math.cos(e.angle)*(t-.5)*260;e.beamY=e.y+Math.sin(e.angle)*(t-.5)*260;e.tick-=dt;if(e.tick<=0&&e.age<2.4){e.tick=.12;this.area(e.beamX,e.beamY,32,95,'strafe');}}
 if(e.type==='laser'&&e.age>=.8){let target=this.entities.find(o=>o.id===e.target&&!o.dead&&o.type!=='rescue'&&o.type!=='shield'&&Math.hypot(o.x-e.x,o.y-e.y)<220);if(!target){target=this.entities.filter(o=>!o.dead&&TYPES[o.type]&&Math.hypot(o.x-e.x,o.y-e.y)<ITEMS.laser.radius).sort((a,b)=>(b.type==='giant')-(a.type==='giant')||Math.hypot(a.x-e.x,a.y-e.y)-Math.hypot(b.x-e.x,b.y-e.y))[0];e.target=target?.id;}if(target){e.beamX=target.x;e.beamY=target.y;e.tick-=dt;if(e.tick<=0){e.tick=.1;this.hurt(target,target.type==='giant'?42:75,'laser');}}else{e.beamX=null;e.beamY=null;}}
 }
''' + s[b:]
s=s.replace("if(o.type==='giant'){o.y=Math.min", "const motion=dt*(o.slow>0?.22:1);o.slow=Math.max(0,(o.slow||0)-dt);\n if(o.type==='giant'){o.y=Math.min")
s=s.replace('o.y+o.speed*dt);o.x+=(this.x-o.x)*dt*.2','o.y+o.speed*motion);o.x+=(this.x-o.x)*motion*.2').replace('}else{o.y+=o.speed*dt;if(o.y>475)o.x+=clamp(this.x-o.x,-1,1)*o.speed*.8*dt;', '}else{o.y+=o.speed*motion;if(o.y>475)o.x+=clamp(this.x-o.x,-1,1)*o.speed*.8*motion;')
s=s.replace("this.emit('message',{text:'长按右侧战术图标，拖到尸群上空投放'})","this.emit('message',{text:'打开支援终端，连线呼叫支援'})")
p.write_text(s,encoding='utf-8')
