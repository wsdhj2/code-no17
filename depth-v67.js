/* Oblique 2.5D scenery. Ground coordinates and combat simulation stay independent. */
(() => {
'use strict';
const palette=[['#353b40','#45494a','#252b31'],['#555150','#68625b','#303438'],['#484844','#625b4b','#2b3031'],['#3f4c50','#526369','#273338'],['#46494c','#68615b','#2c3039']];
function polygon(g,points,color){g.fillStyle=color;g.beginPath();points.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();g.fill();}
function building(g,side,ground,index,level,texture){
 const near=.72+Math.max(0,Math.min(1,ground/768))*.28;
 const inner=side===0?55:377,outer=side===0?-24:456;
 const depth=(80+(index%3)*21)*near,height=(30+(index%3)*11)*near;
 const skew=side===0?-12:12,back=ground-depth,roofY=ground-height;
 const colors=palette[level%5];
 // The wall stands above its ground footprint; cast shadow points away from the street light.
 polygon(g,[[inner,ground],[inner+(side===0?26:-26),ground+16],[inner+(side===0?20:-20),back+19],[inner,back]],'#04080c54');
 polygon(g,[[outer,back],[inner,back],[inner+skew,back-height],[outer,back-height]],colors[2]);
 polygon(g,[[outer,ground],[inner,ground],[inner,roofY],[outer,roofY]],colors[0]);
 polygon(g,[[inner,ground],[inner+skew,ground-height],[inner+skew,back-height],[inner,back]],colors[2]);
 polygon(g,[[outer,roofY],[inner,roofY],[inner+skew,back-height],[outer,back-height]],colors[1]);
 g.strokeStyle='#c6beb126';g.lineWidth=1;g.beginPath();g.moveTo(outer,roofY);g.lineTo(inner,roofY);g.lineTo(inner+skew,back-height);g.stroke();
 // Reuse the chapter's actual masonry under the light planes, avoiding clean vector blocks.
 if(texture){g.save();g.beginPath();g.moveTo(outer,roofY);g.lineTo(inner,roofY);g.lineTo(inner+skew,back-height);g.lineTo(outer,back-height);g.closePath();g.clip();g.globalAlpha=.34;g.globalCompositeOperation='soft-light';g.drawImage(texture,side?texture.width*.87:0,(index*83)%Math.max(1,texture.height-110),texture.width*.13,110,Math.min(outer,inner+skew),back-height,Math.abs(outer-inner-skew),depth);g.restore();}
 for(let k=0;k<42;k++){const a=((k*37+index*13)%83)/83,b=((k*53+index*19)%97)/97;g.fillStyle=k%2?'#b8b2a014':'#00000024';g.fillRect(Math.min(outer,inner)+a*60,back-height+b*depth,1+(k%4),1+(k%3));}
 g.strokeStyle='#0e171b70';g.lineWidth=2;g.beginPath();g.moveTo(roofXSafe(side),back-height+7);g.lineTo(roofXSafe(side)+18,back-height+14);g.lineTo(roofXSafe(side)+20,roofY-8);g.stroke();
 // Rooftop ducts, parapets and facade openings retain separate height planes.
 const roofX=side===0?12:397;
 g.fillStyle='#171e24';g.fillRect(roofX,back-height+22,22,28*near);
 g.fillStyle='#717473';g.fillRect(roofX-2,back-height+17,22,25*near);
 for(let k=0;k<4;k++){g.fillStyle='#222c31';g.fillRect(roofX+1,back-height+21+k*4,15,1);}
 for(let k=0;k<3;k++){
  const x=side===0?k*17+1:383+k*17;
  g.fillStyle='#131d25';g.fillRect(x,roofY+8,10,height-14);
  if((index+k)%3===0){g.fillStyle='#d9a65d';g.fillRect(x+2,roofY+11,5,5);}
 }
 g.fillStyle='#b4afa326';g.fillRect(side===0?0:379,ground-3,53,2);
}
function roofXSafe(side){return side?411:11;}
function environment(g,time,level,texture){
 g.save();const distance=time*30;
 // Fixed world geometry slides with the road, never follows the squad.
 for(let side=0;side<2;side++)for(let n=-2;n<6;n++){
  const spacing=208,offset=side*103,serial=Math.floor(distance/spacing)-n;
  const y=n*spacing+distance%spacing+offset;
  building(g,side,y,((serial%12)+12)%12,level,texture);
 }
 // Soft street illumination is on the ground, not on the HUD or character art.
 for(let side=0;side<2;side++)for(let n=-1;n<4;n++){
  const y=n*270+distance%270+side*115,x=side?369:63;
  const light=g.createRadialGradient(x,y,0,x,y,64);light.addColorStop(0,'#eab77319');light.addColorStop(1,'#eab77300');g.fillStyle=light;g.fillRect(x-64,y-64,128,128);
 }
 g.restore();
}
window.EmberDepth={environment,snapshot:()=>({camera:'oblique',heightPlanes:3,groundCoordinatesUnchanged:true})};
})();
