from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace("if(crossChapter){this.army=8;", "if(crossChapter){this.x=this.targetX=LANES[0];this.lane=0;this.army=8;");p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace("<span>${run.mission().name}</span>`", "<span>${!run.mission().boss&&run.time>=run.mission().duration?'肃清 '+run.entities.filter(o=>F.TYPES[o.type]).length:run.mission().name}</span>`")
s=s.replace("document.querySelectorAll('.support-reference').forEach(el=>el.onclick=openSupport)", "document.querySelectorAll('.support-reference').forEach(el=>{el.onclick=openSupport;el.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openSupport();}};})")
p.write_text(s,encoding='utf-8')
