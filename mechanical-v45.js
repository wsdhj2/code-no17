/* Original canvas-native mechanical enemy sprites and fixed-direction beam telegraphs. */
(() => {
'use strict';
function draw(g,type,x,y,height=78,time=0,firing=false,hit=false,flightDir=1,motion=null){
 if(['dropship','sapper'].includes(type)&&window.EmberVehicles?.draw(g,type,x,y,type==='dropship'?height:height*.72,time,{direction:type==='dropship'?flightDir:1,hit,firing,moving:!!motion?.walking,unloading:type==='dropship'&&firing}))return;
 g.save();g.translate(x,y);g.scale(height/90,height/90*(g.canvas.spriteYRatio||1));
 if(type==='dropship'){g.translate(0,Math.sin(time*2.7)*2.2);g.rotate(Math.PI/2*flightDir);g.translate(0,36);}if(hit)g.filter='brightness(1.8)';
 const box=(x,y,w,h,c)=>{g.fillStyle=c;g.fillRect(Math.round(x),Math.round(y),w,h);};
 const poly=(points,c)=>{g.fillStyle=c;g.beginPath();points.forEach((p,i)=>i?g.lineTo(...p):g.moveTo(...p));g.closePath();g.fill();};
 g.fillStyle='#030a0c66';g.beginPath();g.ellipse(0,1,29,7,0,0,Math.PI*2);g.fill();
 if(type==='dropship'){
  // Twin ducted thrusters, armored cargo bay and a forward cockpit.
  poly([[-18,-74],[18,-74],[25,-54],[22,-9],[0,3],[-22,-9],[-25,-54]],'#111b24');
  poly([[-16,-70],[16,-70],[20,-16],[0,-6],[-20,-16]],'#58656b');
  poly([[-12,-70],[12,-70],[15,-53],[-15,-53]],'#263b46');box(-9,-66,18,5,'#b6d2d4');
  poly([[-20,-51],[-48,-47],[-54,-16],[-29,-25],[-19,-24]],'#26333e');
  poly([[20,-51],[48,-47],[54,-16],[29,-25],[19,-24]],'#26333e');
  for(const side of [-1,1]){box(side*39-10,-48,20,34,'#101a23');box(side*39-7,-45,14,24,'#64716f');box(side*39-4,-42,8,17,'#1b3039');box(side*39-8,-17,16,5,'#dd7953');box(side*39-5,-12,10,8+Math.sin(time*28)*3,'#f5bb72');box(side*25-2,-32,4,12,'#c5a65c');}
  box(-13,-45,26,27,'#202a32');box(-10,-41,20,20,firing?'#cf9257':'#424e52');
  for(let i=0;i<3;i++)box(-9,-37+i*6,18,2,'#171f26');box(-3,-13,6,6,'#e35840');
 }else if(type==='sapper'){
  box(-19,-30,9,30,'#172a31');box(10,-30,9,30,'#172a31');
  for(let i=-28;i<0;i+=7){box(-18,i,6,4,'#8c9682');box(12,i,6,4,'#8c9682');}
  box(-12,-32,24,31,'#697b72');box(-9,-28,18,23,'#243c43');
  box(-7,-25,14,16,'#a8744b');box(-5,-23,10,12,'#c8b284');box(-1,-22,2,11,'#e8d29b');
  box(-10,-6,20,5,'#95a58d');box(-7,-2,4,3,'#f0d496');box(3,-2,4,3,'#f0d496');
  for(const side of [-1,1])for(let i=0;i<4;i++){box(side<0?-18:12,-29+((i*7+time*45)%28),6,2,'#c0b89a');}
  const blink=firing&&Math.sin(time*25)>0;box(-4,-33,8,5,blink?'#fff0b1':'#cf563a');
  if(firing){g.globalAlpha=.6;g.strokeStyle='#ff6d4b';g.lineWidth=2;g.beginPath();g.arc(0,-14,24,0,Math.PI*2);g.stroke();g.globalAlpha=1;}
 }else if(type==='tripod'){
  // Three separate articulated legs and a suspended armored optical core.
  const sway=Math.sin(time*3)*3,walking=motion?.walking?1:0;
  poly([[3,-54],[13,-54],[24,-28],[11,-5],[5,-7],[15,-28]],'#4c5d5b');box(5,-8,13,5,'#9b9e89');
  for(const sign of [-1,1]){
   g.save();g.translate(sign*9,-48);g.rotate(Math.sin(time*5+sign*1.57)*.2*walking);g.translate(-sign*9,48);
   poly([[sign*7,-50],[sign*15,-48],[sign*25,-25],[sign*33,-1],[sign*25,0],[sign*17,-24]],'#273c43');
   poly([[sign*13,-45],[sign*17,-41],[sign*24,-24],[sign*28,-6],[sign*25,-6],[sign*19,-24]],'#82918b');
   box(sign<0?-34:22,-4,13,5,'#b2ad92');box(sign<0?-26:17,-27,10,8,'#b28c65');g.restore();
  }
  poly([[-18,-69+sway],[-10,-79+sway],[10,-79+sway],[20,-68+sway],[16,-44+sway],[-15,-44+sway]],'#152a33');
  poly([[-16,-68+sway],[-9,-75+sway],[8,-75+sway],[15,-66+sway],[11,-49+sway],[-12,-49+sway]],'#71817a');
  box(-15,-65+sway,30,12,'#2d4148');box(-5,-66+sway,10,14,'#6b2824');
  box(-3,-63+sway,6,7,firing?'#fff3b9':'#f77c54');box(-1,-61+sway,2,3,'#fff1cd');box(-7,-46+sway,14,6,'#b5aa88');
  for(const sign of [-1,1]){box(sign<0?-21:15,-72+sway,7,12,'#9a9177');box(sign<0?-19:17,-69+sway,3,7,'#36464b');}
 }else{
  const cannon=type==='cannon';
  poly([[-35,2],[-30,-24],[-20,-29],[20,-29],[30,-24],[35,2]],'#414e4d');
  box(-30,-20,60,22,'#7c8273');box(-28,-19,56,5,'#a1a28b');
  for(let i=-25;i<26;i+=13)box(i,-11,8,3,'#394c4e');
  box(-27,-17,54,17,'#182b32');box(-23,-14,46,10,'#65756e');
  for(let i=-23;i<24;i+=8){box(i,-15,4,12,'#263c41');box(i,-14,4,2,'#97a08a');}
  g.translate(0,firing?Math.abs(Math.sin(time*28))*3:0);
  box(-18,-37,36,22,'#273d44');box(-15,-35,30,15,cannon?'#827967':'#788679');box(-18,-34,6,16,'#a39b80');box(12,-34,6,16,'#a39b80');
  box(-10,-47,20,15,'#1b3138');box(-8,-45,16,10,'#a9a387');box(-3,-43,6,4,'#f2a56b');
  if(cannon){box(-7,-29,14,29,'#14262f');box(-5,-27,10,25,'#87938a');box(-8,-3,16,6,'#273b42');box(-4,-2,8,2,firing?'#fff3b2':'#0b2028');}
  else for(const bx of [-12,6]){box(bx,-29,6,23,'#20353d');box(bx+1,-28,3,20,'#a6ac98');box(bx-1,-7,8,5,firing?'#ffca73':'#30464b');}
  box(-21,-31,3,8,'#d3b56e');box(18,-31,3,8,'#d3b56e');
 }
 g.restore();
}
function beam(g,e,project){
 const trace=()=>{g.beginPath();for(let i=0;i<=18;i++){const t=i/18,p=project(e.x+(e.endX-e.x)*t,e.y+(e.endY-e.y)*t);if(i)g.lineTo(p.x,p.y);else g.moveTo(p.x,p.y);}};
 g.save();if(!e.fired){g.globalAlpha=.65+.2*Math.sin(e.age*17);g.setLineDash([7,5]);g.strokeStyle='#ff4545';g.lineWidth=2;trace();g.stroke();g.setLineDash([]);g.globalAlpha=.15;g.lineWidth=8;g.stroke();}
 else{g.globalAlpha=Math.max(0,1-(e.age-e.delay)/.65);g.strokeStyle='#ff372b44';g.lineWidth=18;trace();g.stroke();g.strokeStyle='#ff7660';g.lineWidth=e.width;g.stroke();g.strokeStyle='#fff0c2';g.lineWidth=3;g.stroke();}
 g.restore();
}
function crash(g,e,project,roadSpeed=30){
 const t=e.age,q=Math.min(1,t/.9),y=e.y+65*q*q+Math.max(0,t-.9)*roadSpeed,p=project(e.x+22*q,y);
 g.save();
 for(let i=0;i<10;i++){const a=Math.max(0,t-i*.07),r=6+i*2;g.globalAlpha=Math.max(0,.5-i*.035)*(1-Math.min(1,t/4.5));g.fillStyle=i%2?'#44474b':'#242c31';g.beginPath();g.ellipse(p.x-i*4,p.y-35-a*24,r,r*.8,0,0,Math.PI*2);g.fill();}
 g.globalAlpha=1;
 if(t<.9){g.translate(p.x,p.y);g.rotate(q*.75);draw(g,'dropship',0,0,82,t,true,true,e.flightDir||1);g.fillStyle='#ffc473';g.fillRect(-37,-21,12,8);}
 else{const impact=t-.9;g.translate(p.x,p.y);if(window.EmberVehicles){g.save();g.globalAlpha=.45;g.rotate(.22);g.filter='brightness(.3) saturate(.3)';EmberVehicles.draw(g,'dropship',0,15,66,0,{direction:e.flightDir||1});g.restore();}g.rotate(.5);g.fillStyle='#1b252a';g.fillRect(-27,-20,54,20);g.fillStyle='#5b5e53';g.fillRect(-12,-28,24,25);g.fillStyle='#c76e3a';g.fillRect(-10,-12,14,7);g.rotate(-.5);for(let i=0;i<12;i++){const angle=i*2.4,r=Math.min(70,impact*110),alpha=Math.max(0,1-impact/1.2);g.globalAlpha=alpha;g.fillStyle=i%2?'#ffdf91':'#da713c';g.fillRect(Math.cos(angle)*r-4,Math.sin(angle)*r*.55-15,8,8);}g.globalAlpha=Math.max(0,1-impact/.6);g.fillStyle='#ffe5a0';g.beginPath();g.ellipse(0,-14,12+impact*70,10+impact*45,0,0,Math.PI*2);g.fill();}
 g.restore();
}
window.EmberMechanicalVFX={draw,beam,crash};
})();
