/* Original raster characters. Atlas source and anchors remain inspectable in assets/. */
(() => {
'use strict';
const data=window.EmberSpriteManifest,image=new Image(),tiles=new Map();let loaded=false,failed=false;
const ready=new Promise(resolve=>{image.onload=()=>{loaded=true;resolve(true);};image.onerror=()=>{failed=true;resolve(false);};});image.src=data.image;
function tile(type,frame){
 const key=type+frame;if(tiles.has(key))return tiles.get(key);
 const char=data.characters[type]||data.characters.walker,f=char.frames[frame],normal=document.createElement('canvas');normal.width=f.w;normal.height=f.h;
 const c=normal.getContext('2d');c.imageSmoothingEnabled=false;c.drawImage(image,f.x,f.y,f.w,f.h,0,0,f.w,f.h);
 const flash=document.createElement('canvas');flash.width=f.w;flash.height=f.h;const g=flash.getContext('2d');g.drawImage(normal,0,0);g.globalCompositeOperation='source-atop';g.fillStyle='#fff0cc';g.fillRect(0,0,f.w,f.h);
 const result={normal,flash,f,char};tiles.set(key,result);return result;
}
function draw(ctx,type,x,y,scale=1,frame=0,hit=false,opacity=1,motion=null){
 if(!loaded)return false;frame=Math.max(0,Math.min(3,frame|0));const {normal,flash,f,char}=tile(type,frame),factor=char.height/char.nominal*scale;
 const sy=ctx.canvas.spriteYRatio||1;
 // One stable foot pivot: animation never swaps the whole firing silhouette.
 const dx=(f.x-f.center)*factor,dy=(f.y-char.base)*factor*sy,dw=f.w*factor,dh=f.h*factor*sy;
 ctx.save();ctx.translate(x,y);ctx.globalAlpha=opacity;ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high';
 if(motion&&frame!==3){
  const phase=motion.phase||0,stride=motion.moving?1:0,recoil=motion.recoil||0;
  const bob=Math.cos(phase*2)*1.05*stride;
  const waist=Math.floor(f.h*.66),legH=f.h-waist;
  // Feet alternate around the pelvis; shoulders retain a continuous, readable silhouette.
  for(let side=0;side<2;side++){
   const half=f.w/2,step=Math.sin(phase+side*Math.PI)*stride;
   ctx.save();ctx.translate(dx+side*dw/2+dw/4,dy+waist*factor*sy);
   // Push the foot forward/back in depth, lift the knee, then plant it.
   const lift=Math.max(0,step)*2.1*scale*sy;
   ctx.rotate(step*.23);ctx.translate(0,-lift);
   ctx.drawImage(normal,side*half,waist,half,legH,-dw/4,0,dw/2,legH*factor*sy*(1+step*.29));ctx.restore();
  }
  ctx.save();ctx.translate(motion.lean||0,bob+recoil*.9);ctx.rotate(Math.sin(phase)*.025*stride);
  if(stride){
   const shoulder=Math.floor(f.h*.34),edge=Math.floor(f.w*.24),armHeight=waist-shoulder;
   // Keep the helmet and rifle steady while the elbows counter-swing with the legs.
   ctx.drawImage(normal,0,0,f.w,shoulder,dx,dy,dw,shoulder*factor*sy+.3);
   ctx.drawImage(normal,edge,shoulder,f.w-edge*2,armHeight,dx+edge*factor,dy+shoulder*factor*sy,(f.w-edge*2)*factor,armHeight*factor*sy+.4);
   for(let side=0;side<2;side++){
    const sx=side?f.w-edge:0,px=dx+(side?f.w-edge/2:edge/2)*factor;
    ctx.save();ctx.translate(px,dy+shoulder*factor*sy);ctx.rotate(-Math.sin(phase+side*Math.PI)*.115);
    ctx.drawImage(normal,sx,shoulder,edge,armHeight,-edge*factor/2,0,edge*factor,armHeight*factor*sy+.4);ctx.restore();
   }
  }else ctx.drawImage(normal,0,0,f.w,waist,dx,dy,dw,waist*factor*sy+.4);
  if(hit){ctx.globalAlpha=opacity*.22;ctx.drawImage(flash,0,0,f.w,waist,dx,dy,dw,waist*factor*sy+.4);}
  ctx.restore();
 }else{ctx.drawImage(normal,dx,dy,dw,dh);if(hit){ctx.globalAlpha=opacity*.22;ctx.drawImage(flash,dx,dy,dw,dh);}}
 ctx.restore();return true;
}
function shadow(ctx,x,y,rx=13,ry=5,opacity=.5){ctx.save();const shade=ctx.createRadialGradient(0,0,0,0,0,1);shade.addColorStop(0,`rgba(3,7,11,${opacity})`);shade.addColorStop(1,'rgba(3,7,11,0)');ctx.translate(x,y+2);ctx.scale(rx*1.4,ry*1.6);ctx.fillStyle=shade;ctx.beginPath();ctx.ellipse(0,0,1,1,0,0,Math.PI*2);ctx.fill();ctx.restore();}
window.EmberCharacters={draw,shadow,ready,snapshot:()=>({loaded,failed,types:Object.keys(data.characters),frames:4,cachedFrames:tiles.size})};
})();
