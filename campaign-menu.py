from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace('<button class="secondary" id="models">图鉴</button></div>', '<button class="secondary" id="models">图鉴</button><button class="secondary" id="campaign">关卡</button></div>')
s=s.replace("$('#start').onclick=start;$('#help').onclick=help;$('#models').onclick=gallery;", "$('#start').onclick=start;$('#help').onclick=help;$('#models').onclick=gallery;$('#campaign').onclick=campaignMenu;")
pos=s.index('function gallery()')
s=s[:pos]+'''function campaignMenu(){overlayState='campaign';const unlocked=Math.min(4,Number(record.unlocked)||0);$('#overlay').innerHTML=`<h2 class="panel-title">战役路线</h2><div class="map-list">${F.LEVELS.map((map,i)=>`<button class="map-entry" data-map="${i}" ${i>unlocked?'disabled':''}><span class="map-number">0${i+1}</span><span><b>${map.name}</b><small>${i>unlocked?'尚未解锁':map.boss}</small></span><em>${i>unlocked?'锁定':'出发 ›'}</em></button>`).join('')}</div><button id="back" class="secondary" style="margin-top:18px">返回</button>`;$('#back').onclick=menu;document.querySelectorAll('[data-map]').forEach(el=>el.onclick=()=>start(Number(el.dataset.map)));}
''' +s[pos:]
s=s.replace("function start(){", "function start(level=0){")
s=s.replace("run=new F.Run();screen='run'", "run=new F.Run({level:Number.isInteger(level)?level:0});screen='run'")
s=s.replace("$('#again').onclick=start;", "$('#again').onclick=()=>start(run.state==='won'?0:run.level);")
s=s.replace("function levelClear(){$('#bossIntro')?.remove();clearAim();", "function levelClear(){$('#bossIntro')?.remove();clearAim();record.unlocked=Math.max(Number(record.unlocked)||0,run.level+1);try{localStorage.setItem('ember-front-record',JSON.stringify(record));}catch{}")
s=s.replace("${win?'撤离成功':'全队阵亡'}", "${win?'战役完成':'全队阵亡'}")
s=s.replace('id="again" class="primary">再来一局','id="again" class="primary">重新出发')
p.write_text(s,encoding='utf-8')
