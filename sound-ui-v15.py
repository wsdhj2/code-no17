from pathlib import Path
import numpy as np,wave
sr=22050;rng=np.random.default_rng(1515)
def save(name,x,peak=.7):
 x-=np.mean(x);x=x/max(.001,max(abs(x)))*peak;x[-min(220,len(x)):] *=np.linspace(1,0,min(220,len(x)))
 with wave.open('assets/audio/'+name+'.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((x*32767).astype('<i2').tobytes())
for name,d,decay,freq in [('ui-input',.055,100,1350),('ui-confirm',.2,32,540),('ui-cancel',.14,38,280),('ui-open',.1,45,800),('ui-error',.16,35,180)]:
 t=np.arange(int(sr*d))/sr;n=rng.uniform(-1,1,len(t));lo=np.convolve(n,np.ones(5)/5,'same');x=(n-lo)*np.exp(-t*decay)*.7+np.sin(2*np.pi*freq*t)*np.exp(-t*decay*1.6)*.18
 if name=='ui-confirm':
  delay=int(sr*.055);x[delay:]+=lo[:-delay]*np.exp(-t[:-delay]*45)*.4
 save(name,x,.5)
n=sr*4;t=np.arange(n)/sr;freq=np.fft.rfftfreq(n,1/sr);z=np.fft.rfft(rng.normal(size=n));mid=(1-np.exp(-(freq/500)**4))*np.exp(-(freq/2900)**4);low=np.exp(-(freq/420)**4)*(1-np.exp(-(freq/75)**4));x=np.fft.irfft(z*(mid+.22*low),n);x/=max(abs(x));x*=.98+.02*np.cos(2*np.pi*.5*t);save('laser-sustain-v15',x,.62)
# Restore a periodic seam after normalizing; use a full-cycle waveform without per-loop fades.
y=x/max(abs(x))*.62
with wave.open('assets/audio/laser-sustain-v15.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((y*32767).astype('<i2').tobytes())
# Reuse a separate edited recorded rifle for hostile gunfire, preserving the existing license.
with wave.open('assets/audio/gun-rifle-alt.wav','rb') as w:raw=w.readframes(w.getnframes());params=w.getparams()
with wave.open('assets/audio/enemy-rifle.wav','wb') as w:w.setparams(params);w.writeframes(raw)
p=Path('audio.js');s=p.read_text(encoding='utf-8').replace('laser-sustain-v13.wav','laser-sustain-v15.wav')
pos=s.index(' creature(type)')
s=s[:pos]+" ui(action,step=0){this.unlocked=true;this.play('ui-'+action,action==='input'?.2:.32,action==='input'?1+(step%3)*.035:1);}\n"+s[pos:]
s=s.replace("'air-strafe-cannon':.1", "'air-strafe-cannon':.1,'enemy-rifle':.14,'ui-input':.045")
s=s.replace("creature(type){if(type==='spitter')", "creature(type){if(['robot','gunner','rocketeer','shieldbot','drone'].includes(type))return;if(type==='spitter')")
s=s.replace("chain:['body-burst',.3]", "chain:['body-burst',.3],rocket:['blast-grenade',.5]")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8')
s=s.replace("if(command||aim){clearAim();return;}clearAim();movePointer", "if(command||aim){cancelSupport();return;}mixer.ui('open');clearAim();movePointer")
s=s.replace("$('#supportClose').onclick=clearAim", "$('#supportClose').onclick=cancelSupport")
s=s.replace("mixer.play('radio',.12)", "mixer.ui('input',command.path.length)")
s=s.replace("command=null;$('#supportPanel')?.remove();beginAim(slot)", "mixer.ui('confirm');command=null;$('#supportPanel')?.remove();beginAim(slot)")
s=s.replace("$('#commandHint').textContent='未匹配，重新连线';", "mixer.ui('error');$('#commandHint').textContent='未匹配，重新连线';")
pos=s.index('function clearAim(){');s=s[:pos]+"function cancelSupport(){if(command||aim)mixer.ui('cancel');clearAim();}\n"+s[pos:]
s=s.replace("if(aim||command)clearAim();else pause()", "if(aim||command)cancelSupport();else pause()")
s=s.replace("else toast('已取消投放 · 道具保留',1.2)", "else{mixer.ui('cancel');toast('已取消投放 · 道具保留',1.2);}")
s=s.replace("mixer.play('ui-select',.2)", "mixer.ui('open')").replace("mixer.play('ui-select',.3)", "mixer.ui('confirm')")
s=s.replace("$('#pickerClose').onclick=close", "$('#pickerClose').onclick=()=>{mixer.ui('cancel');close();}")
s=s.replace("if(e.target===sheet)close();", "if(e.target===sheet){mixer.ui('cancel');close();}")
s=s.replace("$('#clearSlot').onclick=()=>{", "$('#clearSlot').onclick=()=>{mixer.ui('cancel');")
s=s.replace("corpses.push({type,x,y,scale,age:0", "corpses.push({type,level:run?.level||0,x,y,scale,age:0")
s=s.replace("if(F.ROBOT_TYPES.includes(c.type)){", "if(c.type==='giant'&&c.level>=5){ctx.save();ctx.globalAlpha=Math.max(0,alpha)*.55;drawAtlas(ctx,'boss',c.level,0,p.x,p.y,100);ctx.restore();}else if(F.ROBOT_TYPES.includes(c.type)){")
p.write_text(s,encoding='utf-8')
