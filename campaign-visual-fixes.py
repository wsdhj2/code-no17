from pathlib import Path
p=Path('inspect-campaign.py');s=p.read_text(encoding='utf-8');s=s.replace("data={'boss':bosses,'escort':escorts}", "# Use complete idle figures for portraits where the large illustrated column overlaps rows.\nbosses[2][0]=dict(bosses[2][1]);bosses[4][0]=dict(bosses[4][1])\ndata={'boss':bosses,'escort':escorts}")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace("const sy=g.canvas.spriteYRatio||1,w=height*data.w/data.h;", "height=Math.min(height,g.canvas.width*.9*data.h/data.w);const sy=g.canvas.spriteYRatio||1,w=height*data.w/data.h;")
s=s.replace("(o.spit||0)<.5?1:0", "o.y>=330&&(o.spit||0)<.5?1:0")
p.write_text(s,encoding='utf-8')
p=Path('qa-support.cjs');s=p.read_text(encoding='utf-8');s=s.replace("assert.ok(await p.evaluate(()=>emberSnapshot().aim));", "assert.ok(await p.evaluate(()=>emberSnapshot().aim));assert.equal(await p.evaluate(()=>emberSnapshot().timeScale),.25);")
p.write_text(s,encoding='utf-8')
