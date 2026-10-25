/* Raster vehicle art with independent ground shadows, thrusters, treads and unloading motion. */
(()=>{
'use strict';
const sources={dropship:'assets/dropship-v75.png',sapper:'assets/sapper-v75.png',truck:'assets/supply-truck-v75.png'},images={};
const ready=Promise.all(Object.entries(sources).map(([type,path])=>new Promise(resolve=>{const im=images[type]=new Image();im.onload=()=>resolve(true);im.onerror=()=>resolve(false);im.src=path;})));
function shadow(g,x,y,rx,ry,alpha){g.save();g.translate(x,y);g.scale(rx,ry);const grad=g.createRadialGradient(0,0,0,0,0,1);grad.addColorStop(0,`rgba(0,5,9,${alpha})`);grad.addColorStop(1,'rgba(0,5,9,0)');g.fillStyle=grad;g.beginPath();g.arc(0,0,1,0,Math.PI*2);g.fill();g.restore();}
function draw(g,type,x,y,height,time=0,options={}){
 const im=images[type];if(!im?.complete||!im.naturalWidth)return false;
 const sy=g.canvas.spriteYRatio||1,w=height*im.naturalWidth/im.naturalHeight,air=type==='dropship',truck=type==='truck';
 shadow(g,x+(air?9:2),y+(air?14:2),w*(air?.43:.4),height*(air?.12:.09)*sy,air?.38:.62);
 g.save();g.translate(x,y);g.scale(options.direction===-1?-1:1,sy);
 if(options.angle)g.rotate(options.angle);
 if(air)g.translate(0,-9+Math.sin(time*2.8)*1.4);
 else if(options.moving)g.translate(0,Math.sin(time*(truck?18:25))*(truck?.45:.7));
 g.imageSmoothingEnabled=true;g.imageSmoothingQuality='high';if(options.hit)g.filter='brightness(1.45)';
 g.drawImage(im,-w/2,-height,w,height);g.filter='none';
 if(air){
  // Jet light lives beneath the solid hull, pulsing independently of the sprite.
  for(const sign of [-1,1]){g.save();g.globalCompositeOperation='screen';const px=sign*w*.3,py=-height*.3,flame=5+Math.sin(time*31+sign)*1.6;const glow=g.createRadialGradient(px,py,0,px,py,flame*2);glow.addColorStop(0,'#ffe4ac99');glow.addColorStop(.35,'#f2854e55');glow.addColorStop(1,'#ec734000');g.fillStyle=glow;g.fillRect(px-flame*2,py-flame*2,flame*4,flame*4);g.restore();}
  if(options.unloading){g.strokeStyle='#d4a87277';g.lineWidth=1;for(const dx of [-18,0,18]){g.beginPath();g.moveTo(dx,-height*.22);g.lineTo(dx,8);g.stroke();}g.fillStyle='#f0be6d';g.fillRect(-12,-height*.25,24,2);}
 }else if(type==='sapper'){
  if(options.moving){g.strokeStyle='#c1b9a36b';g.lineWidth=1;for(const sign of [-1,1])for(let i=0;i<4;i++){const yy=-height*.68+(i*8+time*34)%(height*.48);g.beginPath();g.moveTo(sign*w*.34-2,yy);g.lineTo(sign*w*.34+2,yy);g.stroke();}}
  const pulse=options.firing?.45+.45*Math.sin(time*27):.25;
  g.globalAlpha=Math.max(.1,pulse);g.fillStyle='#ff6d44';g.beginPath();g.arc(0,-height*.25,options.firing?4:2,0,Math.PI*2);g.fill();g.globalAlpha=1;
 }else if(truck&&options.unloading){
  g.strokeStyle='#efd19366';g.lineWidth=1;g.beginPath();g.moveTo(-w*.23,-height*.18);g.lineTo(w*.23,-height*.18);g.stroke();

 }
 g.restore();return true;
}
window.EmberVehicles={draw,ready,snapshot:()=>Object.fromEntries(Object.entries(images).map(([k,im])=>[k,im.complete&&im.naturalWidth>0]))};
})();
