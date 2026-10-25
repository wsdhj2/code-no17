from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace("command.path=[];command.pointer=e.pointerId;", "command.path=[];command.last=null;command.pointer=e.pointerId;")
a=s.index('function commandPoint(e)');b=s.index('\nfunction drawCommand',a)
s=s[:a]+'''function commandPoint(e){if(!command)return;const box=$('#gestureGrid').getBoundingClientRect(),x=(e.clientX-box.left)*240/box.width,y=(e.clientY-box.top)*240/box.height,old=command.last||{x,y},steps=Math.max(1,Math.ceil(Math.hypot(x-old.x,y-old.y)/10));for(let i=1;i<=steps;i++){const px=old.x+(x-old.x)*i/steps,py=old.y+(y-old.y)*i/steps;for(let n=0;n<9;n++)if(Math.hypot(px-(40+n%3*80),py-(40+Math.floor(n/3)*80))<27&&!command.path.includes(n)){command.path.push(n);mixer.play('radio',.12);break;}}command.last={x,y};drawCommand();}
''' +s[b:];p.write_text(s,encoding='utf-8')
