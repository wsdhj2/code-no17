const {chromium}=require('C:/Users/31681/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:960}}),page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{let queue=[],now=0;window.__qaFrames={};window.requestAnimationFrame=cb=>(queue.push(cb),queue.length);window.__advance=ms=>{const steps=Math.ceil(ms/33.333);for(let i=0;i<steps;i++){now+=ms/steps;const current=queue;queue=[];current.forEach(cb=>cb(now));}};});
 await page.goto('http://localhost:4186');await page.evaluate(()=>__advance(100));await page.screenshot({path:'preview-menu-v2.png'});
 await page.click('#help');assert.ok(await page.locator('.infoList').isVisible());await page.click('#back');await page.click('#start');
 await page.evaluate(()=>__advance(450));await page.screenshot({path:'preview-rescue-v2.png'});
 await page.evaluate(()=>__advance(3500));let s=await page.evaluate(()=>emberSnapshot());assert.equal(s.army,12);assert.equal(s.rescued,4);
 // Real pointer input: cancel, slow-time targeting, then a successful deployment.
 let bar=await page.locator('[data-index="0"]').boundingBox(),map=await page.locator('canvas').boundingBox();
 await page.mouse.move(bar.x+20,bar.y+20);await page.mouse.down();const before=s.time;await page.evaluate(()=>__advance(1000));s=await page.evaluate(()=>emberSnapshot());assert.equal(s.timeScale,.25);assert.ok(s.time-before>.24&&s.time-before<.27);
 await page.mouse.up();s=await page.evaluate(()=>emberSnapshot());assert.equal(s.inventory[0].count,1);assert.equal(s.timeScale,1);
 bar=await page.locator('[data-index="0"]').boundingBox();await page.mouse.move(bar.x+20,bar.y+20);await page.mouse.down();await page.mouse.move(map.x+map.width*.73,map.y+map.height*.45,{steps:8});await page.evaluate(()=>__advance(150));await page.screenshot({path:'preview-targeting-v2.png'});await page.mouse.up();s=await page.evaluate(()=>emberSnapshot());assert.equal(s.inventory[0],null);assert.equal(s.effects[0].type,'bomb');
 await page.click('#pause');let paused=await page.evaluate(()=>emberSnapshot().time);await page.evaluate(()=>__advance(5000));assert.equal(await page.evaluate(()=>emberSnapshot().time),paused);await page.click('#resume');await page.evaluate(()=>__advance(1000));assert.ok(await page.evaluate(()=>emberSnapshot().time)>paused+.9);
 await page.screenshot({path:'preview-game-v2.png'});
 const progress=await page.evaluate(()=>{
  let checkpoints=[],i=0,bossSaved=false,keydown='';
  const key=(name,down)=>window.dispatchEvent(new KeyboardEvent(down?'keydown':'keyup',{key:name}));
  while(i++<2700){const s=emberSnapshot();if(s.state==='lost'||s.state==='won')return{state:s.state,time:s.time,rescued:s.rescued,casualties:s.casualties,army:s.army,checkpoints};
   if(s.state==='inventory'){document.querySelector('[data-slot="1"]').click();continue;}
   if(s.time>132&&!bossSaved){bossSaved=true;checkpoints.push({time:s.time,kind:'boss'});}
   if(s.time>31&&!window.__qaFrames.battle)window.__qaFrames.battle=document.querySelector('canvas').toDataURL();
   if(s.time>135&&!window.__qaFrames.boss)window.__qaFrames.boss=document.querySelector('canvas').toDataURL();
   const enemies=s.targets.filter(o=>!['rescue','shield'].includes(o.type)&&o.y>120).sort((a,b)=>b.y-a.y),rewards=s.targets.filter(o=>['rescue','shield'].includes(o.type)&&o.y>120).sort((a,b)=>b.y-a.y);
   const target=enemies.find(o=>o.y>460)||rewards[0]||enemies[0];
   const desired=target?Math.max(72,Math.min(360,target.x)):s.x;
   const next=Math.abs(desired-s.x)>5?(desired<s.x?'a':'d'):'';
   if(next!==keydown){if(keydown)key(keydown,false);if(next)key(next,true);keydown=next;}
   if(enemies.length&&(enemies[0].y>420||enemies[0].type==='giant')){const slot=s.inventory.findIndex(Boolean);if(slot>=0){key(String(slot+1),true);key(String(slot+1),false);const box=document.querySelector('canvas').getBoundingClientRect(),e=enemies[0],y=Math.max(120,Math.min(565,e.y-15)),x=Math.max(36,Math.min(396,e.x)),sx=216+(x-216)*(.61+.39*y/680);document.querySelector('canvas').dispatchEvent(new PointerEvent('pointerdown',{clientX:box.x+sx/432*box.width,clientY:box.y+y/768*box.height,bubbles:true,pointerId:7}));}}
   __advance(100);
  }return emberSnapshot();
 });
 console.log('browser progression',progress);assert.equal(progress.state,'won');await page.screenshot({path:'preview-victory-v2.png'});
 for(const [key,data] of Object.entries(await page.evaluate(()=>window.__qaFrames)))fs.writeFileSync(`preview-${key}-v2.png`,Buffer.from(data.split(',')[1],'base64'));
 await page.click('#again');await page.evaluate(()=>__advance(100));assert.equal(await page.evaluate(()=>emberSnapshot().army),8);
 const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});const mp=await mobile.newPage();mp.on('pageerror',e=>errors.push(e.message));await mp.goto('http://localhost:4186');await mp.click('#start');await mp.touchscreen.tap(300,640);await mp.waitForTimeout(350);assert.ok(await mp.evaluate(()=>emberSnapshot().x)>250);await mp.screenshot({path:'preview-mobile-v2.png'});
 assert.equal(await mp.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 const cdp=await mobile.newCDPSession(mp),mb=await mp.locator('[data-index="0"]').boundingBox(),mc=await mp.locator('canvas').boundingBox();
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:mb.x+25,y:mb.y+25}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:mc.x+mc.width*.45,y:mc.y+mc.height*.4}]});
 assert.equal(await mp.evaluate(()=>emberSnapshot().timeScale),.25);await mp.screenshot({path:'preview-mobile-target-v2.png'});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});assert.equal(await mp.evaluate(()=>emberSnapshot().inventory[0]),null);
 console.log('page errors',errors);assert.deepEqual(errors,[]);fs.writeFileSync('browser-report.json',JSON.stringify({pointerCancel:true,globalSlowTime:true,bombDeploy:true,pauseResume:true,rescueJoin:true,progression:progress,mobileTouch:true,noHorizontalOverflow:true,pageErrors:errors},null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});


