from pathlib import Path
import numpy as np,wave
R=Path('assets/audio');sr=22050;rng=np.random.default_rng(1010)
def save(name,x):
 x=x/max(.01,np.max(np.abs(x)))*.82
 with wave.open(str(R/(name+'.wav')),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((x*32767).astype('<i2').tobytes())
def clip(name,d,freq,decay,noise=.3):
 t=np.arange(int(sr*d))/sr;n=rng.uniform(-1,1,len(t));lo=np.convolve(n,np.ones(11)/11,'same');x=(np.sin(2*np.pi*(freq*t-25*t*t))*.5+lo*noise)*np.exp(-t*decay)+(n-lo)*np.exp(-t*130)*noise
 save(name,x)
for args in [('gun-pistol',.22,210,30,1.2),('gun-smg',.11,310,48,1),('gun-rifle',.38,135,20,1.6),('gun-shotgun',.45,100,16,2),('gun-laser',.16,760,13,.03),('grenade-launch',.24,95,19,.3),('blast-grenade',.48,64,11,1.5),('blast-orbital',1.8,34,2.8,1.8),('blast-bomb',.95,48,5,1.6),('metal-break',.3,1450,17,.5),('shield-hit',.17,940,25,.03),('emp-pulse',.65,420,7,.05),('drop-land',.4,70,15,.6),('call-confirm',.2,1230,18,.02),('laser-arrive',.8,320,4,.02),('lure-pulse',.35,880,15,.02),('body-burst',.32,80,18,.8),('boss-impact',.65,54,7,1.1)]:clip(*args)
p=Path('audio.js');s=p.read_text(encoding='utf-8');s=s.replace("this.pool=new Map();", "this.pool=new Map();this.cooldowns={};")
s=s.replace("let list=this.pool.get(name);", "const gap=({'gun-smg':.075,'blast-grenade':.18,'shield-hit':.2,'gun-laser':.16,'impact':.1,'boss-impact':.2})[name]||0;if(gap&&this.clock-(this.cooldowns[name]??-10)<gap)return;this.cooldowns[name]=this.clock;let list=this.pool.get(name);")
a=s.index("const sample=({pistol:");z=s.index(";this.play(...sample)",a)
s=s[:a]+"const sample=({pistol:['gun-pistol',.44,1],smg:['gun-smg',.28,1],rifle:['gun-rifle',.6,1],shotgun:['gun-shotgun',.55,1],laserCannon:['gun-laser',.22,1]})[type]||['gun-pistol',.4,1]"+s[z:]
pos=s.index(' creature(type)')
s=s[:pos]+''' effectSound(source){const sample=({strafe:['gun-smg',.3],grenade:['blast-grenade',.4],orbitalBomb:['blast-orbital',.8],bomb:['blast-bomb',.65],boss:['boss-impact',.55],enemy:['body-burst',.4],chain:['body-burst',.3]})[source]||['blast-grenade',.3];this.play(...sample);}
 arrival(type){const sample=({laser:'laser-arrive',energyShield:'emp-pulse',emp:'emp-pulse',barricade:'drop-land',mgTank:'drop-land',grenadeTank:'drop-land',lure:'lure-pulse'})[type];if(sample)this.play(sample,.4);}
'''+s[pos:];p.write_text(s,encoding='utf-8')
