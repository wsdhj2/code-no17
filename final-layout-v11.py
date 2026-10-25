from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace("function result(){const stars=", "function result(){$('#hud').hidden=true;const stars=").replace("function levelClear(){const stars=", "function levelClear(){$('#hud').hidden=true;const stars=")
s=s.replace("if(e.type==='laser'){if(e.beamX!=null){", "if(e.type==='laser'){if(e.beamX!=null){")
# Keep an orbital ray above world sprites but below the HUD band.
s=s.replace("ctx.shadowColor='#efd975';ctx.shadowBlur=18;", "ctx.beginPath();ctx.rect(0,125,W,H-125);ctx.clip();ctx.shadowColor='#efd975';ctx.shadowBlur=18;")
p.write_text(s,encoding='utf-8')
