from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8');
for a,b in [('hp:4200','hp:14000'),('hp:4800','hp:16000'),('hp:5600','hp:18000'),('hp:6200','hp:20000'),('hp:7200','hp:24000')]:s=s.replace(a,b)
p.write_text(s,encoding='utf-8')
p=Path('tests/frontline.test.cjs');s=p.read_text(encoding='utf-8').replace('r.hurt(g,10000)','r.hurt(g,100000)');p.write_text(s,encoding='utf-8')
