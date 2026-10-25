from pathlib import Path

p=Path('frontline.js');s=p.read_text(encoding='utf-8-sig')
a=s.index('function menu(){');b=s.index('\nfunction gallery()',a)
s=s[:a]+'''function menu(){clearAim();screen='menu';run=null;mixer.setMode('menu');overlayState='menu';$('#overlay').dataset.view='menu';$('#hud').hidden=true;$('#toast').style.opacity=0;
 $('#overlay').innerHTML=`<h2 class="home-title">余烬防线</h2><div class="home-controls"><button class="primary" id="start">开始游戏</button><div class="menu-actions"><button class="secondary" id="help">玩法</button><button class="secondary" id="models">图鉴</button></div>${Number(record.best||0)>0?`<div class="home-record">最高分 ${Number(record.best).toLocaleString()}</div>`:''}</div>`;
 $('#start').onclick=start;$('#help').onclick=help;$('#models').onclick=gallery;
 const startButton=$('#start');if(!EmberCharacters.snapshot().loaded){startButton.disabled=true;startButton.textContent='加载中…';EmberCharacters.ready.then(ok=>{startButton.disabled=false;startButton.textContent=ok?'开始游戏':'加载失败，重试';if(!ok)startButton.onclick=()=>location.reload();});}
}
''' +s[b:]
a=s.index('function gallery(){');b=s.index('\nfunction drawGallery()',a)
s=s[:a]+'''function gallery(){overlayState='gallery';$('#overlay').innerHTML='<h2 class="panel-title">角色图鉴</h2><canvas id="characterGallery" width="374" height="375"></canvas><button id="back" class="secondary" style="margin-top:18px">返回</button>';$('#back').onclick=menu;drawGallery();}
''' +s[b:]
s=s.replace("i===5?1.3:1.55", "i===5?1.45:1.65")
s=s.replace("g.font='9px Microsoft YaHei';g.fillStyle='#92a59c';g.fillText(notes[i],x+94,y+115);",'')
a=s.index('function help(){');b=s.index('\nfunction start()',a)
s=s[:a]+'''function help(){overlayState='help';$('#overlay').innerHTML='<h2 class="panel-title">玩法</h2><div class="infoList"><p>左右拖动，队伍自动向前开火。</p><p>左边救人、拿装备，右边挡丧尸。</p><p>拖动右侧道具，松手投放。</p><p class="keyboard-help">电脑：A / D 移动，1 / 2 选道具，P 暂停。</p></div><button id="back" class="secondary">返回</button>';$('#back').onclick=menu;}
''' +s[b:]
a=s.index('function result(){');b=s.index('\nfunction pause()',a)
s=s[:a]+'''function result(){clearAim();overlayState=run.state;const win=run.state==='won';record.best=Math.max(Number(record.best||0),run.score);if(win)record.wins=Number(record.wins||0)+1;try{localStorage.setItem('ember-front-record',JSON.stringify(record));}catch{}
 $('#overlay').innerHTML=`<h2 class="panel-title result-title">${win?'撤离成功':'全队阵亡'}</h2><div class="resultgrid"><div><b>${run.score.toLocaleString()}</b><small>得分</small></div><div><b>${run.army}</b><small>幸存</small></div><div><b>${run.rescued}</b><small>解救</small></div><div><b>${run.kills}</b><small>击杀</small></div></div><button id="again" class="primary">再来一局</button><button id="home" class="secondary" style="margin-top:10px">返回首页</button><div class="hint">${timeLabel(run.time)}</div>`;
 $('#again').onclick=start;$('#home').onclick=menu;sound('end');}
''' +s[b:]
a=s.index('function pause(){');b=s.index('\nfunction inventoryDialog()',a)
s=s[:a]+'''function pause(){if(!run)return;if(run.state==='playing'){clearAim();run.pause();overlayState='paused';$('#overlay').innerHTML='<h2 class="panel-title">已暂停</h2><button class="primary" id="resume">继续游戏</button><button class="secondary" id="home" style="margin-top:10px">返回首页</button>'+mixer.controls();mixer.bind();$('#resume').onclick=pause;$('#home').onclick=menu;}else if(run.state==='paused'){run.resume();overlayState='';$('#overlay').innerHTML='';}}
''' +s[b:]
s=s.replace('<div class="kicker">TACTICAL STORAGE FULL</div>','').replace('战术栏已满','道具已满').replace('发现「${name}」。<br>选择一个槽位替换，或保留现有道具。<br>选择期间战场暂停。','拾取：${name}').replace('保留现有道具','不替换')
s=s.replace("String(run.army).padStart(2,'0')",'String(run.army)')
s=s.replace("if(e.type==='message')toast(e.text);",'')
s=s.replace("floating('包围已解除',e.x,e.y-25,C.green);",'')
s=s.replace("`+${e.count} 名同伴`", "`+${e.count}人`")
s=s.replace("toast(e.capped?'36人编队已满，保持火力':'同伴已归队 · 全队继续射击',2);", "if(e.capped)toast('队伍已满',1.2);")
s=s.replace("`${F.ITEMS[e.reward].name}已收存 · 拖拽投放`", "`${F.ITEMS[e.reward].name} +1`")
s=s.replace("toast('灾厄巨躯挡住出口 · 集中火力，使用战术支援',4)", "toast('灾厄巨躯',1.8)")
s=s.replace("const names=$('#laneNames').children;names[0].textContent=nearest?(nearest.type==='rescue'?'◈ 左路 · 清围解救':'◈ 左路 · 击破护盾'):'◈ 左路 · 解救 / 装备';names[1].textContent='右路 · 丧尸来袭 ◈';", "const names=$('#laneNames').children;names[0].textContent=nearest?(nearest.type==='rescue'?'救援':'装备'):'救援 / 装备';names[1].textContent='尸群';")
s=s.replace("label('灾厄巨躯 / THE COLOSSUS'", "label('灾厄巨躯'")
s=s.replace("label('撤离封锁线 / FINAL CONTACT',216,137,'#efb0a0',10);",'')
s=s.replace("label('EVAC · 撤离通道',216,146,'#d4d6aa',10);",'')
s=s.replace("label('正在归队',p.x,p.y-32,C.green,10);",'')
a=s.index('if(!run){const demo=');b=s.index('}else{\nfor(const e of run.effects)',a)
s=s[:a]+'''if(!run){
 for(const [x,y] of [[192,414],[240,414],[216,456]]){EmberCharacters.shadow(ctx,x,y,16,5,.5);EmberCharacters.draw(ctx,'soldier',x,y,1.8,0);}
''' +s[b:]
s=s.replace("}render();if(overlayState==='gallery')", "}if($('#overlay').dataset.view!==overlayState)$('#overlay').dataset.view=overlayState;render();if(overlayState==='gallery')")
p.write_text(s,encoding='utf-8')
p=Path('audio.js');s=p.read_text(encoding='utf-8-sig').replace('战术音频 / MIX','声音');p.write_text(s,encoding='utf-8')
p=Path('index.html');s=p.read_text(encoding='utf-8-sig');a=s.index('<aside class="editorial">');b=s.index('<main id="frame">',a);s=s[:a]+s[b:];a=s.index('<aside class="fieldnotes">');b=s.index('<script src="engine.js">',a);s=s[:a]+s[b:]
s=s.replace('SQUAD','队伍').replace('名队员','人').replace('战术瞄准 · ¼ 速 <small>松手投放，拖回取消</small>','选择落点 <small>松手投放，拖回取消</small>')
p.write_text(s,encoding='utf-8')
