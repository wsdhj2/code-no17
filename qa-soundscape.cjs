const {chromium}=require('C:/Users/31681/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 try{
  const context=await browser.newContext({viewport:{width:432,height:768}}),p=await context.newPage(),errors=[];
  p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  // Isolate the real boss presentation/audio transition early, without changing release code.
  await p.route('**/engine.js',async route=>{const r=await route.fetch();await route.fulfill({response:r,body:(await r.text()).replace('END=132','END=5')});});
  await p.goto('http://localhost:4186');await p.evaluate(()=>document.fonts.ready);await p.click('#start');
  await p.waitForFunction(()=>emberAudioSnapshot().mode==='boss');await p.waitForTimeout(900);
  let a=await p.evaluate(()=>emberAudioSnapshot());assert.ok(!a.tracks.boss.paused&&a.tracks.boss.time>.2);assert.equal(a.tracks.boss.error,null);assert.ok(a.counts['infected-giant']>=1);
  await p.screenshot({path:'preview-art-boss-v4.png'});
  await p.click('#pause');await p.waitForTimeout(100);let paused=await p.evaluate(()=>emberAudioSnapshot().tracks.boss.time);assert.ok(await p.evaluate(()=>emberAudioSnapshot().tracks.boss.paused));
  await p.locator('[data-mix="music"]').fill('0.2');await p.locator('[data-mix="music"]').dispatchEvent('input');
  await p.click('#resume');await p.waitForTimeout(400);a=await p.evaluate(()=>emberAudioSnapshot());assert.ok(a.tracks.boss.time>paused+.2);assert.equal(a.levels.music,.2);
  await p.click('#sound');await p.waitForTimeout(150);a=await p.evaluate(()=>emberAudioSnapshot());assert.equal(a.enabled,false);assert.ok(Object.values(a.tracks).every(t=>t.paused));
  await p.click('#sound');await p.waitForTimeout(250);assert.equal(await p.evaluate(()=>emberAudioSnapshot().enabled),true);
  assert.deepEqual(errors,[]);
  const mob=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1}),mp=await mob.newPage();
  mp.on('pageerror',e=>errors.push(e.message));await mp.goto('http://localhost:4186');await mp.evaluate(()=>document.fonts.ready);await mp.click('#start');await mp.waitForTimeout(600);await mp.screenshot({path:'preview-art-mobile-v4.png'});
  assert.equal(await mp.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.equal(await mp.evaluate(()=>emberAudioSnapshot().mode),'patrol');
  for(const name of ['rifle-1','heavy','infected-walker','infected-runner','infected-armored','infected-bloater','infected-giant','music-patrol','music-boss']){
   const status=await p.evaluate(async name=>{const a=new Audio('assets/audio/'+name+(name.startsWith('music')?'.ogg':'.wav'));return await new Promise(resolve=>{a.onloadedmetadata=()=>resolve({name,duration:a.duration});a.onerror=()=>resolve({name,error:a.error?.code});a.load();});},name);
   assert.ok(status.duration>.1,JSON.stringify(status));
  }
  assert.deepEqual(errors,[]);const report={bossMusicStarts:true,bossRoar:true,pauseFreezesAudio:true,resumeKeepsPosition:true,independentVolume:true,muteWorks:true,allAudioDecodes:true,mobileLayout:true,errors};
  fs.writeFileSync('soundscape-report.json',JSON.stringify(report,null,2));console.log(report);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
