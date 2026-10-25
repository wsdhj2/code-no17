from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace("command.path=[];command.pointer=e.pointerId;grid.setPointerCapture", "command.path=[];command.pointer=e.pointerId;$('#commandHint').textContent='沿淡线一笔连接';grid.setPointerCapture")
s=s.replace("$('#slowBanner').hidden=false;document.body", "$('#slowBanner').innerHTML=aim.type==='strafe'?'拖动调整扫射方向 <small>松手确认 · Esc 取消</small>':'选择落点 <small>松手投放 · 拖回取消</small>';$('#slowBanner').hidden=false;document.body")
s=s.replace("if(e.type==='wallBreak')", "if(e.type==='message'&&e.text==='该支援已就绪')toast(e.text,1.2);if(e.type==='wallBreak')")
p.write_text(s,encoding='utf-8')
