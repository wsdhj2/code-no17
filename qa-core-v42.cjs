const {chromium}=require('C:/Users/31681/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const a=require('node:assert/strict');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true});try{for(const [width,height]of[[360,640],[390,844],[1440,960]]){
const mobile=width<500,p=await b.newPage({viewport:{width,height},isMobile:mobile,hasTouch:mobile}),errors=[];
p.on('pageerror',e=>errors.push(e.message));
await p.addInitScript(()=>localStorage.setItem('ember-front-record',JSON.stringify({campaignVersion:24,storySkipVersion:25,prologueCompleted:true,skipStory:true,difficulty:'easy'})));
await p.route('**/frontline.js*',async r=>{const v=await r.fetch();await r.fulfill({response:v,body:(await v.text()).replace('window.emberSnapshot=','window.coreQA={getRun:()=>run};window.emberSnapshot=')});});
await p.goto('http://localhost:4186');await p.click('#start');await p.click('#missionDeploy');await p.click('#prepNext');await p.click('#deployStart');
await p.evaluate(()=>{const r=coreQA.getRun();r.entities=[];r.nextWave=Infinity;r.wave=1;r.random=()=>0;r.spawnWave();for(const o of r.entities)o.y+=145;r.giveItem('strafe');});
await p.waitForTimeout(250);
const layout=await p.evaluate(()=>{const r=coreQA.getRun();return {lanes:[...new Set(r.entities.filter(o=>Frontline.TYPES[o.type]).map(o=>o.lane))].sort(),resources:r.entities.filter(o=>o.type==='shield').map(o=>o.x),width:Math.max(...r.formation().map(s=>s.x))-Math.min(...r.formation().map(s=>s.x))};});
a.deepEqual(layout.lanes,[0,1]);a.deepEqual(layout.resources,[216]);a.ok(layout.width<=54);
await p.screenshot({path:`preview-core-v42-${width}.png`});await p.click('#supportOpen');
for(const selector of ['#supportPanel','#supportPanel header','#commandArea','#supportOpen'])a.equal(await p.locator(selector).evaluate(e=>getComputedStyle(e).backgroundColor),'rgba(0, 0, 0, 0)');
await p.screenshot({path:`preview-support-v42-${width}.png`});
const g=await p.locator('#gestureGrid').boundingBox(),x=g.x+g.width/2,start=g.y+g.height*5/6,end=g.y+g.height/6;
if(mobile){const cdp=await p.context().newCDPSession(p);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{id:1,x,y:start}]});for(let i=1;i<=18;i++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{id:1,x,y:start+(end-start)*i/18}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
else{await p.mouse.move(x,start);await p.mouse.down();await p.mouse.move(x,end,{steps:18});await p.mouse.up();}
await p.waitForFunction(()=>emberSnapshot().aim?.type==='strafe');a.equal(await p.locator('#supportPanel').count(),0);
a.equal(await p.evaluate(()=>emberSnapshot().timeScale),.25);
const c=await p.locator('#game').boundingBox(),tx=c.x+c.width*.5,ty=c.y+c.height*320/768;
if(mobile)await p.touchscreen.tap(tx,ty);else await p.mouse.click(tx,ty);
a.equal(await p.evaluate(()=>emberSnapshot().aim),null);
const effect=await p.evaluate(()=>coreQA.getRun().effects.find(e=>e.type==='strafe'));
a.equal(effect.angle,-Math.PI/2);a.ok(Math.abs(effect.x-216)<2);a.ok(Math.abs(effect.y-320)<2);
await p.evaluate(()=>coreQA.getRun().giveItem('strafe'));await p.waitForTimeout(80);await p.click('#supportOpen');
const again=await p.locator('#gestureGrid').boundingBox(),gx=again.x+again.width/2;
await p.mouse.move(gx,again.y+again.height*5/6);await p.mouse.down();await p.mouse.move(gx,again.y+again.height/6,{steps:16});await p.mouse.up();
await p.waitForFunction(()=>emberSnapshot().aim?.type==='strafe');await p.mouse.move(tx-45,ty);await p.mouse.down();await p.mouse.move(tx+45,ty,{steps:10});await p.mouse.up();
const horizontal=await p.evaluate(()=>coreQA.getRun().effects.filter(e=>e.type==='strafe').at(-1));a.ok(Math.abs(horizontal.angle+Math.PI/2)<.001);

a.deepEqual(errors,[]);await p.close();}
console.log('PASS two hostile lanes, central resource, narrow squad, transparent controls, real touch/mouse upward command and single-tap targeting and fixed strafe direction at three sizes');
}finally{await b.close();}})().catch(e=>{console.error(e);process.exit(1)});
