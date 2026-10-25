from pathlib import Path
p=Path('story.js');s=p.read_text(encoding='utf-8');pos=s.index('class Prologue{')
s=s[:pos]+'''for(let chapter=0;chapter<10;chapter++)SCRIPTS['chapter'+chapter]=[['liaison',CHAPTER_BRIEFS[chapter]],['commander',[
'余烬小队，沿途幸存者优先。指挥部会把支援送到你们标记的位置。',
'医院仍有备用电源。救出里面的人，再向东侧化工管廊转移。',
'别在泄漏区停留太久。路障和空袭的申请通道都为你们保留。',
'港区的船已经离开。先打通陆路，我们正在联系下一处基地。',
'如果基地失守，就不要固守。把幸存者带上，我们继续向北。',
'控制这些机械单位的信号来自更北方。我们会陪你们查清它的源头。',
'铁路是撤离车队的生命线。替他们打开通道，别和装甲列车正面硬拼。',
'轨道炮会锁定你们的位置。看清预警再移动，我会批准必要的重型支援。',
'先摧毁母体，阻止无人机继续起飞。最后一段路线已经不远。',
'安全区已经准备开门。这一次，我们会把每一个人的名字带回去。'][chapter]];
SCRIPTS.epilogue=[['liaison','余烬小队，收到你们的定位了。安全区大门正在打开。'],['commander','任务完成。把武器放低，你们到家了。'],['liaison','通讯不会断开。指挥部，始终在线。']];
'''+s[pos:];p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8')
s=s.replace("run.pause();mixer.dialogue=true;", "if(run?.state==='playing')run.pause();mixer.dialogue=true;")
s=s.replace("$('#tutorialExit').hidden=true;", "if($('#tutorialExit'))$('#tutorialExit').hidden=true;")
s=s.replace("function start(level=0,continuing=false,stageId=null){", "function start(level=0,continuing=false,stageId=null,afterStory=false){")
s=s.replace("const m=F.STAGES[stageId]||F.stageFor(level);clearAim();", "const m=F.STAGES[stageId]||F.stageFor(level);if(!afterStory&&m.part===0&&!record.skipStory&&!record.chapterBriefSeen?.[m.chapter]){prologue=new EmberStory.Prologue();showComms('chapter'+m.chapter,()=>{prologue=null;record.chapterBriefSeen=record.chapterBriefSeen||{};record.chapterBriefSeen[m.chapter]=true;saveRecord();start(level,continuing,m.id,true);});return;}clearAim();")
s=s.replace("record.prologueCompleted=true;saveRecord();", "record.prologueCompleted=true;record.chapterBriefSeen=record.chapterBriefSeen||{};record.chapterBriefSeen[0]=true;saveRecord();")
s=s.replace("$('#home').onclick=menu;sound('end');}", "$('#home').onclick=menu;sound('end');if(win&&!record.skipStory&&!record.storyFinalSeen){record.storyFinalSeen=true;saveRecord();prologue=new EmberStory.Prologue();showComms('epilogue',()=>{prologue=null;});}}")
p.write_text(s,encoding='utf-8')
