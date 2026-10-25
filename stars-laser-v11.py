from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8')
s=s.replace("this.casualties=0;this.peak=8", "this.casualties=0;this.stageStartCasualties=0;this.peak=8")
pos=s.index(' completeStage(){')
s=s[:pos]+" missionRating(){const deaths=Math.max(0,this.casualties-(this.stageStartCasualties||0)),total=this.army+deaths,survival=total?this.army/total:0;return this.state==='cleared'||this.state==='won'?(survival>=.9?3:survival>=.7?2:1):0;}\n"+s[pos:]
s=s.replace("this.part=next.part;this.unlockedLevel", "this.part=next.part;this.stageStartCasualties=this.casualties;this.unlockedLevel")
s=s.replace("this[key]=Math.max(0,Number(cp[key])||0);return true", "this[key]=Math.max(0,Number(cp[key])||0);this.stageStartCasualties=this.casualties;return true")
s=s.replace("mission:{...this.mission()},wounded", "mission:{...this.mission()},stars:this.missionRating(),stageCasualties:this.casualties-this.stageStartCasualties,wounded")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8')
s=s.replace("for(const e of run.effects)effect(e);drawCorpses();", "for(const e of run.effects)if(!['laser','squadBeam'].includes(e.type))effect(e);drawCorpses();")
s=s.replace("if(run.mech>0){const p=", "for(const e of run.effects)if(['laser','squadBeam'].includes(e.type))effect(e);\nif(run.mech>0){const p=")
pos=s.index('function levelClear()')
s=s[:pos]+'''function starDisplay(stars,large=false){return `<div class="mission-stars ${large?'large':''}" aria-label="${stars}星">${[1,2,3].map(n=>`<span class="${n<=stars?'earned':''}">★</span>`).join('')}</div>`;}
function saveMissionStars(){const id=run.stageId,stars=run.missionRating();record.stageStars=record.stageStars||{};record.stageStars[id]=Math.max(Number(record.stageStars[id])||0,stars);return stars;}
'''+s[pos:]
s=s.replace("function levelClear(){$('#bossIntro')", "function levelClear(){const stars=saveMissionStars();$('#bossIntro')")
s=s.replace('<span>行动完成</span></div><h2', '<span>行动完成</span></div>${starDisplay(stars,true)}<h2')
s=s.replace("function result(){clearAim();", "function result(){const stars=run.state==='won'?saveMissionStars():0;clearAim();")
s=s.replace("<div class=\"resultgrid\"><div><b>${run.score.toLocaleString()}", "${win?starDisplay(stars,true):''}<div class=\"resultgrid\"><div><b>${run.score.toLocaleString()}")
s=s.replace('<b>${m.code}</b></button>', '<b>${m.code}</b>${starDisplay(Number(record.stageStars?.[i])||0)}</button>')
s=s.replace("<p>${m.boss?F.LEVELS[m.chapter].boss:'清理尸群，沿撤离路线继续推进。'}</p>", "<p>${m.boss?F.LEVELS[m.chapter].boss:'清理尸群，沿撤离路线继续推进。'}</p>${starDisplay(Number(record.stageStars?.[id])||0)}")
s=s.replace('<p>尸群与资源会随机出现在左右两侧。</p>', '<p>尸群与资源会随机出现在左右两侧。</p><p>通关后按本关存活率评级：90%以上三星，70%以上两星，其余一星。</p>')
p.write_text(s,encoding='utf-8')
p=Path('tests/frontline.test.cjs');s=p.read_text(encoding='utf-8');s+='''\ntest('mission stars reward completion and survival, and reset casualty accounting each stage',()=>{const r=empty();assert.equal(r.missionRating(),0);r.state='cleared';assert.equal(r.missionRating(),3);r.army=7;r.casualties=1;assert.equal(r.missionRating(),2);r.army=5;r.casualties=3;assert.equal(r.missionRating(),1);r.nextLevel();r.state='cleared';assert.equal(r.missionRating(),3);r.army=0;r.state='lost';assert.equal(r.missionRating(),0);});\n''';p.write_text(s,encoding='utf-8')
