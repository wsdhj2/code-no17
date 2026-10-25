from pathlib import Path
p=Path('frontline.js');s=p.read_text(encoding='utf-8');s=s.replace('<canvas id="characterGallery" width="374" height="375"></canvas>', '<canvas id="characterGallery" width="374" height="375" aria-label="图鉴模型，点击查看设定"></canvas><div id="galleryLore"></div>')
s=s.replace("galleryMode=el.dataset.gallery;document", "galleryMode=el.dataset.gallery;gallerySelection=0;document")
s=s.replace("g.strokeStyle='#a0ad9044';g.strokeRect", "g.strokeStyle=i===gallerySelection?'#d5c570':'#a0ad9044';g.strokeRect")
a=s.index('function drawGallery()');b=s.index('function help()',a);seg=s[a:b];old="x+94,y+107);}}"
new="""x+94,y+107);}gallerySelection=Math.min(gallerySelection,kinds.length-1);const kind=kinds[gallerySelection],lore={walker:'靠近队伍后抓咬，及时消灭或用路障阻挡。',runner:'移动迅速，会从尸群中快速逼近队伍。',armored:'防护装甲吸收部分伤害，高单发伤害武器更容易破甲。',bloater:'死亡时爆炸，能引爆附近感染者。',spitter:'远程精英。酸液落地前有预警，酸池持续存在，踩入会间隔减员。',soldier:'解救后加入编队，装备与武器升级对全队生效。',mgTank:'180发机枪弹，自动锁敌。空弹后继续阻挡丧尸，耐久耗尽才退出。',grenadeTank:'28发榴弹，范围伤害。弹药耗尽后仍然提供前排护卫。'};$('#galleryLore').innerHTML=`<b>${galleryMode==='boss'?F.LEVELS[kind].boss:names[kind]}</b><span>${galleryMode==='boss'?({smash:'瞄准队伍位置砸击。离开预警区域，趁攻击间隙集中火力。',summon:'召来感染者并发动重击，注意清理接近队伍的召唤物。',charge:'锁定一路后冲锋，提前转移到另一侧。',artillery:'连续炮击不同区域，利用爆炸的时间差移动。',final:'酸池、交错打击与召唤交替出现，保留重型支援应对。'})[F.LEVELS[kind].kind]:lore[kind]}</span>`;target.onclick=e=>{const box=target.getBoundingClientRect(),i=Math.floor((e.clientY-box.top)/box.height*375/125)*2+Math.floor((e.clientX-box.left)/box.width*374/187);if(i>=0&&i<kinds.length){gallerySelection=i;drawGallery();}};}
"""
if old not in seg:raise RuntimeError('gallery ending missing')
seg=seg.replace(old,new);s=s[:a]+seg+s[b:];p.write_text(s,encoding='utf-8')
