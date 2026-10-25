const F=require('./engine');
function play(seed,mode){const r=new F.Run({seed});let ticks=0,nextDecision=0;
while(r.state!=='lost'&&r.state!=='won'&&r.time<260&&ticks++<40000){
 if(r.state==='inventory'){r.resolveItem(1);continue;}
 if(r.time>=nextDecision){nextDecision=r.time+.12;const visible=r.entities.filter(o=>!o.dead&&o.y>120),threats=visible.filter(o=>F.TYPES[o.type]),rewards=visible.filter(o=>!F.TYPES[o.type]);let target;
 if(mode==='grow')target=rewards.sort((a,b)=>b.y-a.y)[0]||threats.sort((a,b)=>b.y-a.y)[0];
 else if(mode==='clear')target=threats.sort((a,b)=>b.y-a.y)[0]||rewards[0];
 else {const urgent=threats.filter(o=>o.y>460).sort((a,b)=>b.y-a.y);target=urgent[0]||rewards.sort((a,b)=>b.y-a.y)[0]||threats.sort((a,b)=>b.y-a.y)[0];}
 if(target)r.move(F.clamp(target.x,72,360));
 if(mode==='smart'&&threats.length){const c=threats.sort((a,b)=>b.y-a.y)[0];for(let i=0;i<2;i++)if(r.inventory[i]&&(c.y>410||threats.length>18||c.type==='giant')){r.deploy(i,F.clamp(c.x,36,396),F.clamp(c.y-12,120,565));break;}}
 }
 r.step(.02);r.drain();
}
return{seed,mode,state:r.state,time:Math.round(r.time),army:r.army,rescued:r.rescued,casualties:r.casualties,score:r.score,peak:r.peak};}
const results=[];for(const mode of ['grow','clear','smart'])for(let seed=1;seed<=12;seed++)results.push(play(seed,mode));
for(const mode of ['grow','clear','smart']){const a=results.filter(r=>r.mode===mode);console.log(mode,JSON.stringify({wins:a.filter(r=>r.state==='won').length,total:a.length,avgTime:Math.round(a.reduce((s,r)=>s+r.time,0)/a.length),avgRescued:Math.round(a.reduce((s,r)=>s+r.rescued,0)/a.length),avgSurvivors:Math.round(a.reduce((s,r)=>s+r.army,0)/a.length)}));}
require('fs').writeFileSync('balance-report.json',JSON.stringify({note:'Deterministic heuristic bot simulations, not human win rates.',results},null,2));

