from pathlib import Path

p=Path('frontline.js');s=p.read_text(encoding='utf-8-sig')
s=s.replace("if(!EmberCharacters.draw(ctx,'soldier',x,y,scale,frame))legacySoldier(x,y,scale,special,trapped,index);", "EmberCharacters.draw(ctx,'soldier',x,y,scale,frame);")
s=s.replace("if(!EmberCharacters.draw(ctx,type,x,y,scale,frame,hit))legacyZombie(x,y,type,scale,age,hit);", "EmberCharacters.draw(ctx,type,x,y,type==='giant'?scale:scale*1.12,frame,hit);")
a=s.index('function legacySoldier(');b=s.index('function icon(',a);s=s[:a]+s[b:]
s=s.replace("night.addColorStop(.6,'#1521260a')", "night.addColorStop(.6,'#10202a33')")
s=s.replace('for(const c of corpses)c.age+=dt;', 'for(const c of corpses){c.age+=dt;c.y+=30*dt;}')
p.write_text(s,encoding='utf-8')
p=Path('engine.js');s=p.read_text(encoding='utf-8-sig').replace(')*20,y:610',')*22,y:610').replace('Math.floor(i/cols)*14','Math.floor(i/cols)*18');p.write_text(s,encoding='utf-8')
p=Path('assets/characters-v5-manifest.js');s=p.read_text(encoding='utf-8').replace('"height":43,"nominal":245','"height":48,"nominal":245');p.write_text(s,encoding='utf-8')
p=Path('inspect-characters.py');s=p.read_text(encoding='utf-8').replace('heights=[43,41','heights=[48,41');p.write_text(s,encoding='utf-8')
p=Path('characters.js');s=p.read_text(encoding='utf-8').replace('ctx.imageSmoothingEnabled=false;ctx.globalAlpha=opacity;ctx.drawImage(normal',"ctx.imageSmoothingEnabled=false;ctx.globalAlpha=opacity;ctx.filter=type==='soldier'?'brightness(1.3)':'brightness(1.15)';ctx.drawImage(normal").replace("if(hit){ctx.globalAlpha=opacity*.6;", "if(hit){ctx.filter='none';ctx.globalAlpha=opacity*.6;");p.write_text(s,encoding='utf-8')
