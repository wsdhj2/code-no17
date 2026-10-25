from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8');s=s.replace("if(i===1&&(this.wave%2===1||this.level>0))type='spitter';", "if(i===1&&(this.wave%2===1||this.level>2&&this.wave%3===0)&&this.entities.filter(o=>o.type==='spitter'&&!o.dead).length<2)type='spitter';")
s=s.replace("tank.hp=Math.max(0,tank.hp-damage*75);for(const unit", "{tank.hp=Math.max(0,tank.hp-damage*75);if(tank.hp===0)this.emit('vehicleHit',{x:tank.x,y:tank.y,destroyed:true});}for(const unit")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace("${i<unlocked?'passed':''}","${i<unlocked||i===F.STAGES.length-1&&record.safeReached?'passed':''}");p.write_text(s,encoding='utf-8')
for name in ['qa-support.cjs','qa-offline.cjs']:
 p=Path(name);s=p.read_text(encoding='utf-8-sig').replace("await p.click('#start');await p.click('#deployStart');", "await p.click('#start');await p.click('#missionDeploy');await p.click('#deployStart');")
 p.write_text(s,encoding='utf-8')
Path('qa-campaign.cjs').write_text("// Current full route regression; prior five-mission campaign was replaced in v0.9.\nrequire('./qa-chapters-v9.cjs');\n",encoding='utf-8')
