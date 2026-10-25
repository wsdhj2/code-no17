from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8')
s=s.replace("this.spawnRescue(0,233,4,100);this.spawnHorde(1,145,8,0);this.emit('message',{text:'左侧清围解救士兵 · 右侧尸群正在逼近'});", "this.openingWave();")
pos=s.index(' spawnWave(){')
s=s[:pos]+" openingWave(){const lane=this.random()<.5?0:1;this.lastResourceLane=lane;this.resourceStreak=1;this.spawnRescue(lane,233,4,100);this.spawnHorde(1-lane,145,10+this.level,Math.min(2,Math.floor(this.level/2)));}\n"+s[pos:]
s=s.replace("lane=0,rewards=", "lane=this.random()<.5?0:1,rewards=")
# use mutable lane and prevent one side >3 successive resource waves
s=s.replace("spawnWave(){const w=", "spawnWave(){let w=")
s=s.replace("'rate','bomb'];if(w%3", "'rate','bomb'];if(this.resourceStreak>=3&&lane===this.lastResourceLane)lane=1-lane;this.resourceStreak=lane===this.lastResourceLane?(this.resourceStreak||0)+1:1;this.lastResourceLane=lane;if(w%3")
s=s.replace("this.spawnHorde(1,-50,3,stage)", "this.spawnHorde(1-lane,-50,3,stage)")
s=s.replace("this.spawnRescue(0,233,4,100);this.spawnHorde(1,145,8,Math.min(2,Math.floor(this.level/2)));", "this.openingWave();")
s=s.replace("this.spawnHorde(1,140,10+this.level*2,2)", "this.spawnHorde(this.random()<.5?0:1,140,10+this.level*2,2)")
s=s.replace("this.spawnHorde(this.wave%3===0?0:1,100", "this.spawnHorde(this.random()<.5?0:1,100")
s=s.replace("this.spawnShield(0,160,this.wave", "this.spawnShield(this.random()<.5?0:1,160,this.wave")
s=s.replace("this.spawnHorde(1,190,4,2)", "this.spawnHorde(this.random()<.5?0:1,190,6,2)")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace('左边救人、拿装备，右边挡丧尸。','尸群与资源会随机出现在左右两侧。');p.write_text(s,encoding='utf-8')
p=Path('tests/frontline.test.cjs');s=p.read_text(encoding='utf-8');a=s.index("test('all scripted roaming hordes");z=s.index("test(",a+7)
s=s[:a]+'''test('resource and horde lanes vary reproducibly and each wave offers opposite routes',()=>{const r=empty(),seen=new Set();for(let i=0;i<30;i++){r.entities=[];r.spawnWave();const resource=r.entities.find(o=>o.type==='rescue'||o.type==='shield');seen.add(resource.lane);assert.ok(r.entities.filter(o=>F.TYPES[o.type]).every(o=>o.lane===1-resource.lane));assert.ok(r.resourceStreak<=3);}assert.equal(seen.size,2);const lanes=seed=>{const r=new F.Run({seed});return Array.from({length:12},()=>{r.entities=[];r.spawnWave();return r.entities.find(o=>['rescue','shield'].includes(o.type)).lane});};assert.deepEqual(lanes(77),lanes(77));assert.notDeepEqual(lanes(77),lanes(12));});
'''+s[z:]
s=s.replace('assert.equal(boss.max,F.LEVELS[r.level].hp)', 'assert.equal(boss.max,F.LEVELS[r.level].hp*1.15)');p.write_text(s,encoding='utf-8')
