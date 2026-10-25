from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace("const angle=Math.atan2(624-o.y,this.x-o.x),fan=o.type==='gunner'", "const target=this.formation()[o.id%this.army]||{x:this.x,y:624},angle=Math.atan2(target.y-o.y-10,target.x-o.x),fan=o.type==='gunner'");p.write_text(s,encoding='utf-8')
