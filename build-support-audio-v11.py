from pathlib import Path
import numpy as np,wave,json
sr=22050;rng=np.random.default_rng(1137);root=Path('assets/audio')
def save(name,x):
 x=np.tanh(x);x=x/max(.001,np.max(np.abs(x)))*.86
 with wave.open(str(root/(name+'.wav')),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((x*32767).astype('<i2').tobytes())
def sig(d):
 t=np.arange(int(sr*d))/sr;n=rng.uniform(-1,1,len(t));lo=np.convolve(n,np.ones(35)/35,'same');return t,n,lo
# Jet turbine, broadband pass and a Doppler fall. No explosion in approach cue.
t,n,lo=sig(1.65);env=np.sin(np.pi*t/1.65)**1.7;phase=2*np.pi*np.cumsum(780-460*t/1.65)/sr
save('airstrike-flyby',(lo*4+n*.16+np.sin(phase)*.18+np.sin(phase*2.03)*.07)*env)
t,n,lo=sig(1.2);phase=2*np.pi*(230*t+480*t*t);env=np.minimum(t/.12,1)*np.maximum(0,1-t/1.2)**.4
save('orbital-charge',(np.sin(phase)*.28+np.sin(phase*.503)*.2+lo*.8)*env)
# Cannon impulse: sharp metallic discharge followed by descending pressure wave and debris.
t,n,lo=sig(1.8);x=(n*.8*np.exp(-t*70)+lo*7*np.exp(-t*3.3)+np.sin(2*np.pi*(52*t+2*(1-np.exp(-t*30))))*np.exp(-t*4))
for delay,gain in [(.12,.3),(.27,.18),(.49,.1)]:
 at=int(delay*sr);x[at:]+=lo[:-at]*gain*3*np.exp(-t[:-at]*4)
save('orbital-cannon-impact',x)
t,n,lo=sig(.8);phase=2*np.pi*(110*t+130*t*t);env=np.minimum(t/.035,1)*np.minimum((.8-t)/.08,1)
save('orbital-beam-loop',(np.sin(phase)*.24+np.sin(phase*3)*.06+lo*.5)*env)
t,n,lo=sig(.95);save('airstrike-impact',(lo*5*np.exp(-t*7)+n*.6*np.exp(-t*55)+np.sin(2*np.pi*(76*t-23*t*t))*np.exp(-t*8)))
t,n,lo=sig(.18);save('air-strafe-cannon',(n*.9*np.exp(-t*80)+lo*3*np.exp(-t*28)+np.sin(2*np.pi*145*t)*np.exp(-t*30)))
p=Path('audio.js');s=p.read_text(encoding='utf-8').replace("'boss-impact':.2", "'boss-impact':.2,'air-strafe-cannon':.1,'orbital-beam-loop':.6")
s=s.replace("strafe:['gun-smg',.3]", "strafe:['air-strafe-cannon',.4]").replace("orbitalBomb:['blast-orbital',.8]", "orbitalBomb:['orbital-cannon-impact',.82]").replace("bomb:['blast-bomb',.65]", "bomb:['airstrike-impact',.7]")
pos=s.index(' arrival(type)')
s=s[:pos]+" approach(type){const name=({bomb:'airstrike-flyby',strafe:'airstrike-flyby',orbitalBomb:'orbital-charge',laser:'orbital-charge',mgTank:'airstrike-flyby',grenadeTank:'airstrike-flyby'})[type];if(name)this.play(name,.45);}\n"+s[pos:]
s=s.replace("laser:'laser-arrive'", "laser:'laser-arrive',strafe:'airstrike-flyby'")
p.write_text(s,encoding='utf-8')
