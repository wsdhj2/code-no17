/* Deterministic pixel-stepped orbital strike: designation, shell, blast, mushroom cloud. */
(function(root,factory){if(typeof module==='object')module.exports=factory();else root.EmberOrbitalVFX=factory();})(globalThis,function(){
'use strict';
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function phase(e){if(!e.detonated)return e.age<(e.arrival||3)-.55?'designation':'incoming';const t=e.age-(e.arrival||3);return t<.3?'impact':t<4?'cloud':'fade';}
function draw(ctx,e,project,radius=180,roadSpeed=30){
 const arrival=e.arrival||3,t=e.age-arrival,worldY=e.y+(e.detonated?Math.max(0,t)*roadSpeed:0),p=project(e.x,worldY),scale=.61+.39*worldY/680,R=radius*scale;
 ctx.save();ctx.beginPath();ctx.rect(0,95,432,650);ctx.clip();
 if(!e.detonated){
  const remaining=Math.max(0,-t),pulse=.7+.2*Math.sin(e.age*15);
  ctx.globalAlpha=.22;ctx.strokeStyle='#ff453b';ctx.lineWidth=1;ctx.setLineDash([7,9]);ctx.beginPath();ctx.arc(p.x,p.y,R,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);
  ctx.globalAlpha=pulse;ctx.strokeStyle='#ff4c40';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(p.x,95);ctx.lineTo(p.x,p.y);ctx.stroke();
  ctx.globalAlpha=.17;ctx.lineWidth=8;ctx.stroke();ctx.globalAlpha=1;
  ctx.fillStyle='#fff2ce';ctx.fillRect(Math.round(p.x)-2,Math.round(p.y)-2,4,4);
  ctx.strokeStyle='#ff5848';ctx.lineWidth=2;ctx.beginPath();ctx.arc(p.x,p.y,15,0,Math.PI*2);ctx.moveTo(p.x-25,p.y);ctx.lineTo(p.x-10,p.y);ctx.moveTo(p.x+10,p.y);ctx.lineTo(p.x+25,p.y);ctx.moveTo(p.x,p.y-25);ctx.lineTo(p.x,p.y-10);ctx.moveTo(p.x,p.y+10);ctx.lineTo(p.x,p.y+25);ctx.stroke();
  ctx.font='bold 10px Microsoft YaHei';ctx.textAlign='center';ctx.fillStyle='#120d0d';ctx.fillText('轨道标定 · '+remaining.toFixed(1)+'s',p.x+1,p.y-34);ctx.fillStyle='#ff9980';ctx.fillText('轨道标定 · '+remaining.toFixed(1)+'s',p.x,p.y-35);
  if(remaining<.55){
   const q=clamp(1-remaining/.55,0,1),y=p.y-440*(1-q*q),x=p.x+32*(1-q);
   ctx.globalAlpha=.7;ctx.fillStyle='#ffae56';ctx.fillRect(Math.round(x)-2,Math.round(y)-72,4,65);ctx.globalAlpha=.3;ctx.fillRect(Math.round(x)-5,Math.round(y)-58,10,52);ctx.globalAlpha=1;
   ctx.fillStyle='#1b2025';ctx.fillRect(Math.round(x)-5,Math.round(y)-20,10,18);ctx.fillStyle='#a6b2ac';ctx.fillRect(Math.round(x)-3,Math.round(y)-19,6,13);ctx.fillStyle='#fff0b0';ctx.fillRect(Math.round(x)-3,Math.round(y)-4,6,8);
  }
  ctx.restore();return;
 }
 const life=clamp(1-(t-3.5)/2.9,0,1),grow=1-Math.exp(-t*2.1);
 // Ground pressure rings are brief, separate from the one gameplay damage pulse.
 if(t<1.3){
  for(let i=0;i<2;i++){const q=clamp((t-i*.12)/.95,0,1);ctx.globalAlpha=(1-q)*.85;ctx.strokeStyle=i?'#d79b65':'#fff0bd';ctx.lineWidth=i?4:7;ctx.beginPath();ctx.ellipse(p.x,p.y,R*q*1.4,R*q*.75,0,0,Math.PI*2);ctx.stroke();}
 }
 if(t<.3){ctx.globalAlpha=(1-t/.3)*.85;ctx.fillStyle='#fff7d9';ctx.fillRect(p.x-R*.55,p.y-R*.4,R*1.1,R*.8);}
 // Pixel-stepped ellipses keep the cloud consistent with the game's sprites.
 function puff(x,y,rx,ry,color,alpha){
  ctx.globalAlpha=alpha*life;ctx.fillStyle=color;const step=5;
  for(let dy=-ry;dy<=ry;dy+=step){const half=rx*Math.sqrt(Math.max(0,1-dy*dy/(ry*ry)));ctx.fillRect(Math.round((x-half)/step)*step,Math.round((y+dy)/step)*step,Math.ceil(half*2/step)*step,step+1);}
 }
 const height=(100+Math.min(80,t*16))*grow,capY=p.y-height,capWidth=(62+R*.38)*grow;
 const heat=Math.exp(-t*.78),smoke=.4*life;
 // Narrow rising stem, broad rolling canopy, and a ground-level skirt.
 for(let i=0;i<9;i++){
  const q=i/8,xx=p.x+Math.sin(i*2.3+t*.6)*9*grow,yy=p.y-height*q;
  puff(xx,yy,(14+q*11)*grow,22*grow,'#4c4740',smoke+.12);
  if(t<2.8)puff(xx,yy,Math.max(3,(10+q*7)*grow),15*grow,i%2?'#f69b3b':'#ffd27a',heat*.6);
 }
 for(let i=0;i<9;i++){
  const q=(i-4)/4,x=p.x+q*capWidth*.78,y=capY+q*q*23*grow+Math.sin(i*3.7+t*.4)*5;
  puff(x,y,capWidth*.35,capWidth*.29,i%2?'#3c3b38':'#5c5245',smoke+.15);
  if(t<3)puff(x,y+9*grow,capWidth*.25,capWidth*.17,i%2?'#d66e2b':'#f5a84c',heat*.77);
 }
 puff(p.x,p.y+9,R*.65*grow,22*grow,'#847160',.27*life);
 if(t<1.3)puff(p.x,p.y,34*grow,29*grow,'#fff0b0',Math.exp(-t*2));
 for(let i=0;i<20;i++){const a=i*2.399,spread=(25+i*3)*grow,x=p.x+Math.cos(a)*spread,y=p.y-(t*40+i*8)%230;ctx.globalAlpha=life*.55;ctx.fillStyle=i%3?'#d99a58':'#ffe6a6';ctx.fillRect(Math.round(x),Math.round(y),i%3?2:3,3);}
 ctx.restore();
}
return{phase,draw};
});
