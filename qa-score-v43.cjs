const {chromium}=require('C:/Users/31681/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');const a=require('node:assert/strict');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true});try{
const p=await b.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),errors=[];
p.on('pageerror',e=>errors.push(e.message));
await p.addInitScript(()=>localStorage.setItem('ember-front-record',JSON.stringify({campaignVersion:24,storySkipVersion:25,prologueCompleted:true,skipStory:true,difficulty:'easy'})));
await p.route('**/frontline.js*',async r=>{const v=await r.fetch();await r.fulfill({response:v,body:(await v.text()).replace('window.emberSnapshot=','window.musicQA={getRun:()=>run};window.emberSnapshot=')});});
await p.goto('http://localhost:4186');await p.click('#settings');
a.equal(await p.locator('[data-score]').count(),5);const sources=[];
for(const mode of ['menu','patrol','boss','victory','defeat']){
 await p.click(`[data-score="${mode}"]`);
 await p.waitForFunction(m=>{const s=emberAudioSnapshot();return s.musicMode===m&&!s.tracks[m].paused&&s.tracks[m].time>.15},mode);
 const s=await p.evaluate(()=>emberAudioSnapshot());a.equal(s.preview,mode);a.equal(s.tracks[mode].error,null);a.ok(s.tracks[mode].src.includes('-v43.ogg'));sources.push(s.tracks[mode].src);
 a.equal(await p.locator(`[data-score="${mode}"]`).getAttribute('aria-pressed'),'true');
}
a.equal(new Set(sources).size,5);
await p.screenshot({path:'preview-music-v43-390.png'});
await p.click('[data-score="defeat"]');a.equal(await p.evaluate(()=>emberAudioSnapshot().preview),null);
await p.click('#settingsBack');await p.click('#start');await p.click('#missionDeploy');await p.click('#prepNext');await p.click('#deployStart');
await p.evaluate(()=>{const r=musicQA.getRun();r.entities=[];r.nextWave=Infinity;});
await p.waitForFunction(()=>emberAudioSnapshot().mode==='patrol'&&emberAudioSnapshot().tracks.patrol.time>.15);
await p.evaluate(()=>musicQA.getRun().bossSpawned=true);
await p.waitForFunction(()=>emberAudioSnapshot().mode==='boss'&&emberAudioSnapshot().tracks.boss.time>.15);
await p.waitForTimeout(1200);const normal=await p.evaluate(()=>emberAudioSnapshot().tracks.boss.volume);
await p.evaluate(()=>EmberSound.dialogue=true);await p.waitForTimeout(800);a.ok((await p.evaluate(()=>emberAudioSnapshot().tracks.boss.volume))<normal*.5);
await p.evaluate(()=>{EmberSound.dialogue=false;musicQA.getRun().pause();});await p.waitForFunction(()=>emberAudioSnapshot().mode==='paused');
await p.evaluate(()=>{EmberSound.previewScore('patrol');EmberSound.scorePreview.until=EmberSound.clock+.25;});await p.waitForTimeout(2400);
a.equal(await p.evaluate(()=>emberAudioSnapshot().preview),null);a.ok(await p.evaluate(()=>Object.values(emberAudioSnapshot().tracks).every(t=>t.paused)));
await p.evaluate(()=>{EmberSound.dialogue=false;musicQA.getRun().state='cleared';});
await p.waitForFunction(()=>emberAudioSnapshot().mode==='victory'&&emberAudioSnapshot().tracks.victory.time>.15);
a.equal(await p.evaluate(()=>emberAudioSnapshot().tracks.victory.loop),false);
await p.evaluate(()=>EmberSound.tracks.victory.pause());await p.waitForTimeout(350);a.equal(await p.evaluate(()=>EmberSound.tracks.victory.paused),true);
await p.evaluate(()=>musicQA.getRun().state='lost');
await p.waitForFunction(()=>emberAudioSnapshot().mode==='defeat'&&emberAudioSnapshot().tracks.defeat.time>.15);
a.equal(await p.evaluate(()=>emberAudioSnapshot().tracks.defeat.loop),false);
if(!process.argv.includes('--quick')){await p.waitForTimeout(33300);a.equal(await p.evaluate(()=>EmberSound.tracks.defeat.ended),true);await p.waitForTimeout(700);a.equal(await p.evaluate(()=>EmberSound.tracks.defeat.ended),true);}
a.deepEqual(errors,[]);console.log('PASS five distinct preview files; all five scene routes; voice ducking; paused preview expiry; non-looping result cues'+(process.argv.includes('--quick')?'':'; natural defeat ending without restart'));
}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});
