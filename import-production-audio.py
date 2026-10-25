from pathlib import Path
import subprocess,numpy as np,wave,json
ff=Path(r'C:\Users\31681\Desktop\学习\小程序\work\video-inspect-deps\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe');sr=22050;out=Path('assets/audio');lib=Path('audio-sources/firearms/Prepared SFX Library');res=Path('audio-sources/residue/residue-sfx');report=[]
def read(p):return np.frombuffer(subprocess.check_output([str(ff),'-v','error','-i',str(p),'-f','f32le','-ac','1','-ar',str(sr),'-']),dtype='<f4').copy()
def save(name,x,peak=.86):
 x=np.nan_to_num(x);x-=np.mean(x);n=min(int(.012*sr),len(x)//4);x[:n]*=np.linspace(0,1,n);x[-n:]*=np.linspace(1,0,n);x=x/max(.001,np.max(np.abs(x)))*peak
 with wave.open(str(out/(name+'.wav')),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
 report.append({'file':name+'.wav','seconds':round(len(x)/sr,3)})
def shot(p,duration):
 x=read(p);win=110;levels=np.array([np.sqrt(np.mean(x[i:i+win]**2)) for i in range(0,len(x),win)]);indices=np.where(levels>max(levels)*.22)[0];start=max(0,indices[0]*win-int(.008*sr));return x[start:start+int(duration*sr)]
for name,folder,files,length in [('gun-pistol','1911',['A_42P.wav','A_34P.wav'],.48),('gun-smg','Carl Gustav M45',['G_31P.wav','G_20P.wav'],.23),('gun-rifle','1917',['B_24P.wav','B_16P.wav'],.75),('gun-shotgun','CD',['H_21P.wav','H_16P.wav'],.7)]:
 for i,file in enumerate(files):save(name+('-alt' if i else ''),shot(lib/folder/file,length))
jet=read(Path('audio-sources/engine_takeoff.wav'));jet=jet[:int(sr*3)];save('airstrike-flyby',jet)
boom=read(res/'boom.ogg');save('airstrike-impact',boom[:int(sr*1.6)])
save('blast-grenade',boom[:int(sr*.6)])
# Orbital impact layers the explosion with a stretched low tail and delayed pressure reflections.
low=np.interp(np.arange(int(len(boom)*1.5))/1.5,np.arange(len(boom)),boom);mix=np.zeros(int(sr*2.6));n=min(len(low),len(mix));mix[:n]+=low[:n]*.8;n=min(len(boom),len(mix));mix[:n]+=boom[:n]*.6
for delay,gain in [(.14,.27),(.32,.14)]:
 at=int(delay*sr);n=min(len(low),len(mix)-at);mix[at:at+n]+=low[:n]*gain
save('orbital-cannon-impact',mix)
save('air-strafe-cannon',shot(lib/'AK-47'/'C_28P.wav',.26))
save('tank-machinegun',shot(lib/'AK-47'/'C_31P.wav',.27))
# Texture-based energy and creature layers retain broadband material, not a sine-wave notification.
for name,file,seconds in [('orbital-beam-loop','lumosaw.wav',.8),('laser-arrive','emag.wav',.9),('emp-pulse','emag.wav',.6),('spitter-cast','spit.wav',.65),('infected-bloater','hurker.wav',.8),('metal-break','zipper.wav',.45),('pickup-gear','ammopickup.wav',.4),('lure-pulse','quietship.wav',.7),('empty-magazine','emptyclip.wav',.4)]:
 x=read(res/file);save(name,x[:int(sr*seconds)])
# Charge built from reversed explosion texture plus rising engine, not two pure-tone beeps.
x=boom[:int(sr*1.1)][::-1].copy();x*=np.linspace(.03,.65,len(x));save('orbital-charge',x)
# Short mechanical UI click taken from an existing material sample, never a melodic notification.
x=read(out/'metal-break.wav');save('ui-select',x[:int(sr*.065)],.45);save('call-confirm',x[:int(sr*.11)],.55)
save('upgrade',read(out/'pickup-gear.wav'),.65);save('rescue',read(out/'pickup-gear.wav'),.6)
(out/'production-audio-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('Imported and mixed',len(report),'production clips')

for name,file,d in [('gun-laser','lumosaw.wav',.17),('shield-hit','emag.wav',.18),('shield','emag.wav',.26),('vehicle-engine','ventilator.wav',1.6)]:save(name,read(res/file)[:int(sr*d)])
