from pathlib import Path
import numpy as np,wave
with wave.open('assets/audio/vehicle-engine.wav','rb') as f:sr=f.getframerate();x=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
x=x[:int(sr*.65)];x=np.convolve(x,np.ones(9)/9,'same');x*=np.minimum(np.arange(len(x))/(sr*.03),1)*np.minimum((len(x)-np.arange(len(x)))/(sr*.08),1)
with wave.open('assets/audio/mech-servo.wav','wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((x/max(.01,max(abs(x)))*.65*32767).astype('<i2').tobytes())
p=Path('audio.js');s=p.read_text(encoding='utf-8').replace("creature(type){if(['robot'", "creature(type){if(this.mechanical&&type==='giant'){if(this.clock-this.lastCreature>5){this.lastCreature=this.clock;this.play('mech-servo',.45);}return;}if(['robot'")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace("checkpoint=null){mixer.beginRun();", "checkpoint=null){mixer.mechanical=level>=5;mixer.beginRun();")
s=s.replace("F.LEVELS[m.chapter].boss:'清理尸群，沿撤离路线继续推进。'", "F.LEVELS[m.chapter].boss:m.chapter>=5?'突破机械警戒，沿撤离路线推进。':'清理尸群，沿撤离路线继续推进。'")
p.write_text(s,encoding='utf-8')
p=Path('tests/frontline.test.cjs');s=p.read_text(encoding='utf-8')+'''\ntest('old chapter IDs retain their identity and chapter six begins after the former ending',()=>{assert.equal(F.STAGES[12].chapter,4);assert.equal(F.STAGES[12].name,'撤离行动');assert.equal(F.STAGES[13].chapter,5);assert.equal(F.STAGES.at(-1).chapter,9);const r=new F.Run({level:9,weapon:'laserCannon'});assert.equal(r.level,9);assert.equal(r.weapon,'laserCannon');});\n''';p.write_text(s,encoding='utf-8')
p=Path('qa-support.cjs');s=p.read_text(encoding='utf-8');s=s.replace("assert.deepEqual(errors,[]);await p.screenshot", "await p.click('#supportOpen');await p.click('#supportOpen');const audio=await p.evaluate(()=>emberAudioSnapshot());assert.ok(audio.counts['ui-input']>0);assert.ok(audio.counts['ui-confirm']>0);assert.ok(audio.counts['ui-cancel']>0);assert.deepEqual(errors,[]);await p.screenshot");p.write_text(s,encoding='utf-8')
