const F=require('../engine'),fs=require('node:fs'),assert=require('node:assert/strict');
const curves=[.3,.45,.7].map(weight=>({weight,bonusAt16:weight*(Math.sqrt(2)-1),bonusAt24:weight*(Math.sqrt(3)-1),bonusAt36:weight*(Math.sqrt(4.5)-1)}));
let comparisons=0,added=0,maxAdded=0;const start=performance.now();
for(const difficulty of Object.keys(F.DIFFICULTIES))for(let level=0;level<10;level++)for(const army of [4,8,16,36,80])for(const speed of [0,.5,1])for(const seed of [22,77,771]){
 const r=new F.Run({difficulty,level,seed});r.army=army;r.rate=2.15*(1+speed);r.time=40;r.wave=7;r.entities=[];r.growthPressure=r.growthTarget();r.spawnFlanks(30,2);const actual=r.entities.length;
 const baseline=new F.Run({difficulty,level,seed});baseline.army=army;baseline.rate=r.rate;baseline.time=40;baseline.wave=7;baseline.entities=[];baseline.growthPressure=1;baseline.spawnFlanks(30,2);assert.ok(actual>=baseline.entities.length);added+=actual-baseline.entities.length;maxAdded=Math.max(maxAdded,actual-baseline.entities.length);comparisons++;
}
const r=new F.Run();const trace=[];r.army=32;for(let sec=0;sec<=24;sec++){if(sec===12)r.army=6;for(let i=0;i<100;i++)r.updateGrowthPressure(.01);trace.push({second:sec+1,army:r.army,multiplier:+r.growthPressure.toFixed(4)});}
const report={note:'Deterministic wave and growth simulation; not human comfort ratings or player win rates.',curves,selectedWeight:.45,comparisons,allAtLeastV61:true,meanAdded:added/comparisons,maxAdded,elapsedMs:Math.round(performance.now()-start),growthAndLossTrace:trace};fs.writeFileSync('director-v62-report.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
