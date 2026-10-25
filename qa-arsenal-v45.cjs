const {chromium}=require('C:/Users/31681/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');const a=require('node:assert/strict');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true});try{for(const [width,height]of[[390,844],[1440,960]]){
const p=await b.newPage({viewport:{width,height}}),errors=[];p.on('pageerror',e=>errors.push(e.message));
await p.addInitScript(()=>localStorage.setItem('ember-front-record',JSON.stringify({campaignVersion:24,storySkipVersion:25,prologueCompleted:true,skipStory:true,difficulty:'easy'})));
await p.route('**/frontline.js*',async r=>{const v=await r.fetch();await r.fulfill({response:v,body:(await v.text()).replace('window.emberSnapshot=','window.vfxQA={getRun:()=>run,events,gallery};window.emberSnapshot=')});});
await p.goto('http://localhost:4186/?v=45');await p.click('#start');await p.click('#missionDeploy');await p.click('#prepNext');await p.click('#deployStart');
await p.evaluate(()=>{const r=vfxQA.getRun();r.entities=[];r.effects=[];r.nextWave=Infinity;r.shotClock=Infinity;r.inventory=[{type:'orbitalBomb',count:1}];r.deploy(0,216,350);vfxQA.events();});
await p.waitForTimeout(180);a.equal(await p.evaluate(()=>EmberOrbitalVFX.phase(vfxQA.getRun().effects[0])),'designation');await p.screenshot({path:`preview-orbital-designation-${width}.png`});
await p.evaluate(()=>vfxQA.getRun().effects[0].age=2.65);await p.waitForTimeout(70);a.equal(await p.evaluate(()=>EmberOrbitalVFX.phase(vfxQA.getRun().effects[0])),'incoming');await p.screenshot({path:`preview-orbital-shell-${width}.png`});
await p.evaluate(()=>{const r=vfxQA.getRun();r.effects[0].age=3;r.step(.01);vfxQA.events();r.effects[0].age=4.4;});await p.waitForTimeout(100);await p.screenshot({path:`preview-orbital-cloud-${width}.png`});
a.ok(await p.evaluate(()=>(emberAudioSnapshot().counts['orbital-designate-v44']||0)>0));a.ok(await p.evaluate(()=>(emberAudioSnapshot().counts['orbital-impact-v44']||0)>0));
await p.evaluate(()=>{const r=vfxQA.getRun();r.effects=[];r.entities=[];r.level=7;r.stageId=14;r.unit('sentry',106,275,{holdY:275,fireClock:9});r.unit('cannon',326,285,{holdY:285,fireClock:9});r.unit('tripod',216,335,{holdY:335,fireClock:0});r.step(.01);vfxQA.events();});
await p.waitForTimeout(120);a.ok(await p.evaluate(()=>vfxQA.getRun().effects.some(e=>e.type==='enemyLaser'&&!e.fired)));await p.screenshot({path:`preview-robots-warning-${width}.png`});
await p.evaluate(()=>{const r=vfxQA.getRun();r.x=r.targetX=350;const e=r.effects.find(e=>e.type==='enemyLaser');e.age=1.31;r.step(.01);vfxQA.events();});await p.waitForTimeout(60);await p.screenshot({path:`preview-robots-beam-${width}.png`});
await p.evaluate(()=>{const r=vfxQA.getRun();r.pause();r.entities=[];r.effects=[];vfxQA.gallery();});await p.click('[data-gallery="robot"]');await p.click('#galleryNext');a.ok((await p.locator('#galleryLore').textContent()).includes('炮'));await p.screenshot({path:`preview-robots-gallery-${width}.png`});
const decoded=await p.evaluate(()=>Promise.all(['orbital-designate-v44','orbital-incoming-v44','orbital-impact-v44'].map(name=>new Promise((resolve,reject)=>{const el=new Audio('assets/audio/'+name+'.wav');el.onloadedmetadata=()=>resolve(el.duration);el.onerror=()=>reject(Error(name));}))));a.ok(decoded[2]>6);a.deepEqual(errors,[]);await p.close();}
console.log('PASS orbital designation/shell/cloud and layered cue decode; stationary cannon and tripod warning/beam; gallery sprites; phone and desktop');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});
