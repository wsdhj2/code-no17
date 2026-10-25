from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace('const contacts=[];b.hitIds=b.hitIds||[];',"const contacts=[];b.hitIds=b.hitIds||[];if(b.weapon!=='rifle')b.pierce=1;");p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace("readout.innerHTML=`${weaponIcon(run.weapon)}<span>${F.WEAPONS[run.weapon].name}</span>`;", "if(readout.dataset.weapon!==run.weapon){readout.dataset.weapon=run.weapon;readout.innerHTML=`${weaponIcon(run.weapon)}<span>${F.WEAPONS[run.weapon].name}</span>`;}")
p.write_text(s,encoding='utf-8')
