"""Original sound design and score for Ember Front. No third-party recordings."""
from pathlib import Path
import wave, json, subprocess
import numpy as np

SR = 22050
ROOT = Path(__file__).parent / 'assets' / 'audio'
ROOT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(271023)

def noise(n): return rng.uniform(-1, 1, n)
def lowpass(x, width):
    # Moving average FIR, shape preserving and deterministic.
    return np.convolve(x, np.ones(width) / width, mode='same')
def save(name, x, peak=.86):
    x = np.nan_to_num(x)
    maximum = max(float(np.max(np.abs(x))), .001)
    x = x / maximum * peak
    with wave.open(str(ROOT / (name + '.wav')), 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
    return {'name': name, 'duration': len(x)/SR, 'peak': peak}
def add(track, sample, seconds, gain=1):
    pos=int(seconds*SR); size=min(len(sample),len(track)-pos)
    if size>0: track[pos:pos+size] += sample[:size]*gain
def gun(seed, heavy=False):
    rr=np.random.default_rng(seed); t=np.arange(int(SR*.34))/SR
    n=rr.uniform(-1,1,len(t)); crack=(n-lowpass(n,8))*np.exp(-t*110)*1.3
    body=lowpass(n,13)*np.exp(-t*28)*3
    thump=np.sin(2*np.pi*(145*t-110*t*t))*np.exp(-t*35)*.8
    mechanic=(np.sin(2*np.pi*2200*t)+.5*np.sin(2*np.pi*3100*t))*np.exp(-np.maximum(0,t-.035)*70)*(t>.035)*.08
    x=crack+body+thump+mechanic
    if heavy: x+=np.sin(2*np.pi*66*t)*np.exp(-t*12)*.8
    for delay,gain in [(0.045,.19),(.09,.1),(.17,.05)]:
        at=int(delay*SR); x[at:]+=body[:-at]*gain
    return np.tanh(x*1.7)

report=[]
for i in range(3): report.append(save('rifle-'+str(i+1),gun(40+i),.83))
report.append(save('heavy',gun(51,True),.85))
for name,material in [('impact',0),('armor',1),('shield',2),('debris',3)]:
    t=np.arange(int(SR*.25))/SR; n=noise(len(t)); x=lowpass(n,3+material*3)*np.exp(-t*(35 if material==0 else 22))
    if material: x+=sum(np.sin(2*np.pi*f*t)*np.exp(-t*30)*.12 for f in [410+material*350,1100+material*170,2310])
    report.append(save(name,x,.6))
t=np.arange(int(SR*1.5))/SR;n=noise(len(t));x=lowpass(n,22)*np.exp(-t*3)*3+np.sin(2*np.pi*(48*t+5*np.sin(t*9)))*np.exp(-t*5)
x+=(n-lowpass(n,7))*np.exp(-t*38)*.6
report.append(save('explosion',np.tanh(x*2),.94))

# Formant-shaped, nonverbal synthetic creature voices, not recorded actor voices.
for kind,freq,length in [('walker',83,.8),('runner',165,.62),('armored',68,.85),('bloater',51,1.1),('giant',37,1.7)]:
    t=np.arange(int(SR*length))/SR
    f=freq*(1+.15*np.sin(t*11))*(1-.3*t/length)
    phase=2*np.pi*np.cumsum(f)/SR
    voice=sum(np.sin(phase*k)/k for k in range(1,13))
    breath=lowpass(noise(len(t)),5)*2
    envelope=np.minimum(t/.05,1)*np.maximum(0,1-t/length)**.7
    voice=np.tanh(voice*2)*(0.5+.5*np.sin(t*23)**2)+breath*.35
    if kind=='bloater': voice+=np.sin(2*np.pi*31*t)*(.6+.4*np.sin(t*35))
    if kind=='giant': voice+=lowpass(noise(len(t)),90)*8
    report.append(save('infected-'+kind,voice*envelope,.75))
t=np.arange(int(SR*.35))/SR
hurt=(np.sin(2*np.pi*(115*t-50*t*t))+.5*lowpass(noise(len(t)),8))*np.minimum(t/.015,1)*np.exp(-t*11)
report.append(save('squad-hurt',hurt,.65))
for name,notes in [('rescue',[587,740,880]),('upgrade',[440,660,880]),('radio',[1150,950]),('victory',[293.66,349.23,440,587.33]),('defeat',[220,174.61,146.83])]:
    x=np.zeros(int(SR*(len(notes)*.14+.45)))
    for i,f in enumerate(notes):
        t=np.arange(int(.4*SR))/SR; sample=(np.sin(2*np.pi*f*t)+np.sin(2*np.pi*f*2*t)*.2)*np.exp(-t*12)
        add(x,sample,i*.14,.45)
    report.append(save(name,x,.6))

def note(freq,seconds,kind='bass'):
    t=np.arange(int(seconds*SR))/SR
    if kind=='bass': x=np.tanh((np.sin(2*np.pi*freq*t)+.35*np.sin(2*np.pi*freq*2*t))*2)*np.exp(-t*3)
    elif kind=='string': x=sum(np.sin(2*np.pi*freq*k*t)/k for k in range(1,6))*np.minimum(t/.06,1)*np.exp(-t*2)
    else: x=np.sin(2*np.pi*freq*t)*np.exp(-t*8)
    return x*np.minimum((seconds-t)/.025,1)

def kick():
    t=np.arange(int(.4*SR))/SR
    return np.sin(2*np.pi*(43*t+5*(1-np.exp(-t*35))))*np.exp(-t*13)+noise(len(t))*np.exp(-t*110)*.2
def snare():
    t=np.arange(int(.25*SR))/SR;n=noise(len(t));return(n-lowpass(n,9))*np.exp(-t*20)+np.sin(2*np.pi*170*t)*np.exp(-t*25)*.2
def hat():
    t=np.arange(int(.08*SR))/SR;n=noise(len(t));return(n-lowpass(n,4))*np.exp(-t*70)

# 16 bars / D minor progression. Exact bar boundary loops, sparse patrol vs driving boss.
for name,bpm,boss in [('patrol',88,False),('boss',116,True)]:
    beat=60/bpm; bars=16; duration=bars*4*beat; x=np.zeros(round(duration*SR)); roots=[73.416,58.27,65.406,55]
    for bar in range(bars):
        root=roots[(bar//2)%4];base=bar*4*beat
        for step in range(8):
            freq=root*(2 if step%4==3 else 1)
            add(x,note(freq,.42*beat),base+step*.5*beat,.23 if boss else .12)
            if boss:
                interval=[0,7,12,3,0,7,10,7][step];f=root*2*2**(interval/12)
                add(x,note(f,.9*beat,'string'),base+step*.5*beat,.075)
        for b in ([0,1.5,2,3.25] if boss else [0,2]):add(x,kick(),base+b*beat,.38 if boss else .2)
        for b in [1,3]:add(x,snare(),base+b*beat,.2 if boss else .06)
        for b in range(8):add(x,hat(),base+b*.5*beat,.045 if boss else .02)
        # Long minor harmony, distant signal rather than a copied recognizable melody.
        for ratio in [1,2**(3/12),2**(7/12)]:add(x,note(root*4*ratio,3.8*beat,'string'),base,.017 if boss else .025)
    # Circular stereo-style room reflections folded into the mono loop.
    x=np.tanh(x*1.3);x+=np.roll(x,int(.17*SR))*.11+np.roll(x,int(.31*SR))*.06
    report.append(save('music-'+name,x,.7))
t=np.arange(int(SR*18))/SR
wind=lowpass(noise(len(t)),100)*4*(.4+.6*np.sin(t*.3)**2)
wind+=np.sin(2*np.pi*48*t)*.02+lowpass(noise(len(t)),6)*.025
report.append(save('ambience',wind,.45))
ff=Path(r'C:\Users\31681\Desktop\学习\小程序\work\video-inspect-deps\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe')
for name in ['music-patrol','music-boss','ambience']:
    if ff.exists():subprocess.run([str(ff),'-y','-loglevel','error','-i',str(ROOT/(name+'.wav')),'-c:a','libvorbis','-q:a','4',str(ROOT/(name+'.ogg'))],check=True)
(ROOT/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Built',len(report),'original audio assets')
