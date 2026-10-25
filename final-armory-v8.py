from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace('rate:w.rate*speed,rateScale:speed','rate:this.weapon===\'laserCannon\'?w.rate:w.rate*speed,rateScale:speed');p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8-sig');s=s.replace("screen='briefing';const unlocked=", "screen='briefing';$('#overlay').dataset.view='briefing';const unlocked=")
s=s.replace("const w=F.WEAPONS[b.weapon];$('#overlay').innerHTML", "const base=F.WEAPONS[b.weapon],power=b.continuing&&run?run.damage/5:1,speed=b.continuing&&run?run.rate/2.15:1,w={...base,damage:Number((base.damage*power).toFixed(1)),rate:Number((base.rate*speed).toFixed(2))};$('#overlay').innerHTML")
s=s.replace("?'<b>20<small>伤害 / 人·秒</small></b><b>聚能<small>全队合束</small></b><b>束宽 ↑<small>攻速升级</small></b>'", "?`<b>${Number((w.damage*(1+.4*(speed-1))).toFixed(1))}<small>伤害 / 人·秒</small></b><b>聚能<small>全队合束</small></b><b>束宽 ↑<small>攻速升级</small></b>`")
p.write_text(s,encoding='utf-8')
