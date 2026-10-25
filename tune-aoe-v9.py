from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace("this.acid(this.x<216?326:106,624,65,1.1);this.strike(this.x,58,1.8,3);", "this.acid(this.x<216?326:106,624,38,1.1);this.strike(this.x,40,1.8,3);")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace("ctx.fillRect(p.x-e.radius,548,e.radius*2,150)","ctx.fillRect(p.x-e.radius,e.y-78,e.radius*2,156)").replace("ctx.strokeRect(p.x-e.radius,548,e.radius*2,150)","ctx.strokeRect(p.x-e.radius,e.y-78,e.radius*2,156)").replace("rect(p.x-e.radius,694,e.radius*2*ratio,3", "rect(p.x-e.radius,e.y+78,e.radius*2*ratio,3")
p.write_text(s,encoding='utf-8')
