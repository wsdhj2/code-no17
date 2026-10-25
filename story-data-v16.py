from pathlib import Path
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace("mission(){return STAGES[this.stageId];}","mission(){return this.tutorial?{id:-1,chapter:0,part:0,name:'断线重连',code:'00',boss:false,duration:99999}:STAGES[this.stageId];}")
s=s.replace("completeStage(){if(this.state!=='playing')return;", "completeStage(){if(this.tutorial||this.state!=='playing')return;")
p.write_text(s,encoding='utf-8')
Path('story.js').write_text('''/* Original communications script and tutorial state. */
(function(root,factory){if(typeof module==='object')module.exports=factory();else root.EmberStory=factory();})(globalThis,function(){
const CAST={unknown:{name:'？？？',role:'未知信号',portrait:null},liaison:{name:'林澈',role:'指挥部 · 联络员',portrait:0},commander:{name:'陈砚',role:'指挥部 · 指挥官',portrait:1},squad:{name:'余烬小队',role:'地面通讯',portrait:null}};
const SCRIPTS={
 opening:[['unknown','……滋……滋滋……还有活人吗？'],['unknown','高架下面……我们被困住了。有人能听见吗？'],['squad','这里是余烬小队。听得见，别出声，我们正在靠近。'],['liaison','余烬小队，这里是指挥部联络员林澈。你们的信号接通了。'],['commander','我是陈砚。先救人。沿公路向右侧信号点靠拢，我们会一直保持联系。']],
 rescue:[['liaison','看到右前方的幸存者了吗？清掉围困他们的感染者，他们就能加入你们。'],['commander','队伍会自动向前开火。你来决定走哪条路，把枪口对准敌人。']],
 airstrike:[['unknown','得救了……谢谢。街口还有很多，它们跟过来了！'],['liaison','我已向指挥官申请空中支援。余烬小队，支援终端现在由你们操作。'],['liaison','打开左侧「支援」，照着图案一笔连线。指令确认后，拖到尸群的位置，松手投放。']],
 orbital:[['liaison','空袭命中。记住，飞机需要抵达时间，要提前呼叫。'],['commander','前方有重装感染者。常规火力压不住，我授权一次轨道激光。'],['liaison','仍然向我提交指令。锁定落点后，轨道激光会持续追踪敌人。']],
 ending:[['liaison','威胁清除。轨道链路稳定，后续支援由我为你们调度。'],['commander','通往安全区的路还很长。救下更多人，别让任何人独自留下。'],['liaison','第一段撤离路线已经上传。余烬小队，指挥部会一直听着。']]
};
const CHAPTER_BRIEFS=['我们听得见。先穿过封锁公路，把还能行动的人带出来。','医院还有呼救信号。别让他们等到通讯彻底消失。','化工管廊是唯一的近路。留意酸液，保持队伍移动。','港区撤离点正在失守。先清通集装箱之间的道路。','基地没有回应。靠近之前，保留一份重型支援。','那些机械单位不是友军。我们正在查明是谁接管了工区。','装甲列车封住了铁路。拆掉它，撤离车队才能通过。','电站为机械防线供能。切断轨道炮平台，我们就能穿过去。','无人机从军港不断起飞。母体机甲必须在这里停止运转。','这是最后一道闸门。摧毁战争中枢，安全区就在它后面。'];
class Prologue{constructor(){this.phase='opening';this.cast=null;this.startKills=0;this.dialogue=[];this.line=0;this.revealed=false;this.phaseStarted=0;}setPhase(phase,run){this.phase=phase;this.cast=null;this.startKills=run.kills;this.phaseStarted=run.time;}observe(run){if(this.phase==='move'&&run.x>275)return'rescue';if(this.phase==='rescue'&&run.rescued>=4)return'airstrike';if(this.phase==='airstrike'&&this.cast==='bomb'&&run.effects.some(e=>e.type==='bomb'&&e.detonated)&&run.kills>this.startKills)return'orbital';if(this.phase==='orbital'&&this.cast==='laser'&&run.kills>this.startKills)return'ending';return null;}}
return{CAST,SCRIPTS,CHAPTER_BRIEFS,Prologue};});
''',encoding='utf-8')
p=Path('index.html');s=p.read_text(encoding='utf-8').replace('<script src="frontline.js">','<script src="story.js"></script><script src="frontline.js">');s=s.replace('<link rel="stylesheet" href="operation-ui.css">','<link rel="stylesheet" href="operation-ui.css"><link rel="stylesheet" href="story-ui.css">');p.write_text(s,encoding='utf-8')
