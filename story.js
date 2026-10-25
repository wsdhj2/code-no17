/* Original communications script and tutorial state. */
(function(root,factory){if(typeof module==='object')module.exports=factory();else root.EmberStory=factory();})(globalThis,function(){
const CAST={unknown:{name:'？？？',role:'未知信号',portrait:null},liaison:{name:'联络员',role:'指挥部 · 联络员',portrait:0},commander:{name:'弈崎',role:'指挥部 · 少校',portrait:1},squad:{name:'17小队',role:'幸存者编队',portrait:2}};
const SCRIPTS={
 opening:[['unknown','……滋……滋滋……还有活人吗？'],['unknown','高架下面……我们被困住了。有人能听见吗？'],['squad','这里是17小队。听得见，别出声，我们正在靠近。'],['liaison','17小队，这里是指挥部联络员。你们的信号接通了。'],['commander','我是弈崎。先救人。沿公路向右侧信号点靠拢，我们会一直保持联系。']],
 rescue:[['liaison','看到右前方的幸存者了吗？清掉围困他们的感染者，他们就能加入你们。'],['commander','队伍会自动向前开火。你来决定走哪条路，把枪口对准敌人。']],
 airstrike:[['unknown','得救了……谢谢。街口还有很多，它们跟过来了！'],['liaison','我已向指挥官申请空中支援。17小队，支援终端现在由你们操作。'],['liaison','打开左侧「支援」，照着图案一笔连线。指令确认后，拖到尸群的位置，松手投放。']],
 orbital:[['liaison','空袭命中。记住，飞机需要抵达时间，要提前呼叫。'],['commander','前方有重装感染者。常规火力压不住，我授权一次轨道激光。'],['liaison','仍然向我提交指令。锁定落点后，轨道激光会持续追踪敌人。']],
 ending:[['liaison','威胁清除。轨道链路稳定，后续支援由我为你们调度。'],['commander','通往安全区的路还很长。救下更多人，别让任何人独自留下。'],['liaison','第一段撤离路线已经上传。17小队，指挥部会一直听着。']]
};
const CHAPTER_BRIEFS=['我们听得见。先穿过封锁公路，把还能行动的人带出来。','医院还有呼救信号。别让他们等到通讯彻底消失。','化工管廊是唯一的近路。留意酸液，保持队伍移动。','港区撤离点正在失守。先清通集装箱之间的道路。','基地没有回应。靠近之前，保留一份重型支援。','那些机械单位不是友军。我们正在查明是谁接管了工区。','装甲列车封住了铁路。拆掉它，撤离车队才能通过。','电站为机械防线供能。切断轨道炮平台，我们就能穿过去。','无人机从军港不断起飞。母体机甲必须在这里停止运转。','这是最后一道闸门。摧毁战争中枢，安全区就在它后面。'];
for(let chapter=0;chapter<10;chapter++)SCRIPTS['chapter'+chapter]=[['liaison',CHAPTER_BRIEFS[chapter]],['commander',[
'17小队，沿途幸存者优先。指挥部会把支援送到你们标记的位置。',
'医院仍有备用电源。救出里面的人，再向东侧化工管廊转移。',
'别在泄漏区停留太久。路障和空袭的申请通道都为你们保留。',
'港区的船已经离开。先打通陆路，我们正在联系下一处基地。',
'如果基地失守，就不要固守。把幸存者带上，我们继续向北。',
'控制这些机械单位的信号来自更北方。我们会陪你们查清它的源头。',
'铁路是撤离车队的生命线。替他们打开通道，别和装甲列车正面硬拼。',
'轨道炮会锁定你们的位置。看清预警再移动，我会批准必要的重型支援。',
'先摧毁母体，阻止无人机继续起飞。最后一段路线已经不远。',
'安全区已经准备开门。这一次，我们会把每一个人的名字带回去。'][chapter]]];
SCRIPTS.epilogue=[['liaison','17小队，收到你们的定位了。安全区大门正在打开。'],['commander','任务完成。把武器放低，你们到家了。'],['liaison','通讯不会断开。指挥部，始终在线。']];
class Prologue{constructor(){this.phase='opening';this.cast=null;this.startKills=0;this.dialogue=[];this.line=0;this.revealed=false;this.phaseStarted=0;}setPhase(phase,run){this.phase=phase;this.cast=null;this.startKills=run.kills;this.phaseStarted=run.time;}observe(run){if(this.phase==='move'&&run.x>275)return'rescue';if(this.phase==='rescue'&&run.rescued>=4)return'airstrike';if(this.phase==='airstrike'&&this.cast==='bomb'&&run.effects.some(e=>e.type==='bomb'&&e.detonated)&&run.kills>this.startKills)return'orbital';if(this.phase==='evacuation'&&run.time-this.phaseStarted>=14&&!run.entities.some(o=>!o.dead&&o.type!=='rescue'&&o.type!=='shield')&&!run.joins.length)return'evacuated';if(this.phase==='orbital'&&this.cast==='laser'&&run.kills>this.startKills)return'ending';return null;}}
return{CAST,SCRIPTS,CHAPTER_BRIEFS,Prologue};});
