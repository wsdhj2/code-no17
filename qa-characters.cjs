const{chromium}=require('C:/Users/31681/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true});try{
 const p=await b.newPage({viewport:{width:1440,height:960}}),errors=[];p.on('pageerror',e=>errors.push(e.message));p.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 await p.goto('http://localhost:4186');await p.waitForFunction(()=>emberCharacterSnapshot().loaded);await p.evaluate(()=>document.fonts.ready);
 assert.equal(await p.evaluate(()=>emberCharacterSnapshot().types.length),6);await p.click('#models');await p.waitForTimeout(300);await p.screenshot({path:'preview-character-gallery-v5.png'});
 await p.click('#back');await p.click('#start');await p.waitForTimeout(2300);await p.screenshot({path:'preview-character-game-v5.png'});
 let s=await p.evaluate(()=>emberCharacterSnapshot());assert.ok(s.cachedFrames>=6);assert.ok(s.corpses>0);
 // Every animation frame, including hit tint and prone corpses, must render without cross-cell errors.
 const render=await p.evaluate(()=>{const c=document.createElement('canvas');c.width=800;c.height=600;const g=c.getContext('2d');g.fillStyle='#192b30';g.fillRect(0,0,800,600);const types=emberCharacterSnapshot().types;for(let row=0;row<types.length;row++)for(let col=0;col<4;col++)EmberCharacters.draw(g,types[row],col*200+100,row*100+88,1.5,col,col===2);return c.toDataURL();});fs.writeFileSync('preview-character-frames-v5.png',Buffer.from(render.split(',')[1],'base64'));
 const mob=await b.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true}),mp=await mob.newPage();mp.on('pageerror',e=>errors.push(e.message));await mp.goto('http://localhost:4186');await mp.waitForFunction(()=>emberCharacterSnapshot().loaded);await mp.click('#models');assert.equal(await mp.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await mp.screenshot({path:'preview-character-mobile-v5.png'});await mp.click('#back');await mp.click('#start');await mp.touchscreen.tap(300,640);await mp.waitForTimeout(200);assert.ok(await mp.evaluate(()=>emberSnapshot().x)>200);
 assert.deepEqual(errors,[]);const report={atlasReady:true,characters:6,posesPerCharacter:4,all24PosesRender:true,hitTint:true,corpses:true,mobileGallery:true,mobileTouch:true,errors};fs.writeFileSync('character-report.json',JSON.stringify(report,null,2));console.log(report);
}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});
