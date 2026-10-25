from pathlib import Path
p=Path('tests/frontline.test.cjs');s=p.read_text(encoding='utf-8').replace("r.strike(r.x,90,.01,4);advance(r,.02);assert.equal(r.effects.find(e=>e.type==='energyShield').hp,0)","const shield=r.effects.find(e=>e.type==='energyShield');r.strike(r.x,90,.01,4);advance(r,.02);assert.equal(shield.hp,0)");p.write_text(s,encoding='utf-8')
