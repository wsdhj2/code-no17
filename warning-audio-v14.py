from pathlib import Path
import numpy as np,wave
sr=22050;t=np.arange(int(sr*1.45))/sr;r=np.random.default_rng(1401);phase=2*np.pi*(115*t+21*t*t);noise=np.convolve(r.normal(size=len(t)),np.ones(18)/18,'same');x=(np.sin(phase)*.4+np.sin(phase*2)*.18+np.sin(phase*3)*.1+noise*.2)*np.sin(np.pi*t/1.45)**.8
with wave.open('assets/audio/boss-warning.wav','wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((x*.8*32767).astype('<i2').tobytes())
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace('function effect(e){supportAircraft(e);','function effect(e){')
s=s.replace("for(const e of run.effects)if(['laser','squadBeam'].includes(e.type))effect(e);", "for(const e of run.effects)if(['laser','squadBeam'].includes(e.type))effect(e);for(const e of run.effects)supportAircraft(e);")
p.write_text(s,encoding='utf-8')
