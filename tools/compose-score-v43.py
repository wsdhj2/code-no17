"""Five independent original game cues. Different meters, motifs and lead instruments.
Local ensemble synthesis; no copied melodies, OST recordings or remote dependencies.
"""
import importlib.util, json, subprocess, wave
from pathlib import Path
from functools import lru_cache
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ensemble',Path(__file__).with_name('compose-score-v41.py'))
ensemble=importlib.util.module_from_spec(spec);spec.loader.exec_module(ensemble)
SR=32000;OUT=ROOT/'assets/audio';RNG=np.random.default_rng(4317)

@lru_cache(maxsize=2048)
def note(kind,midi,duration):
    if kind in ['horn','strings','choir','snare','timpani','cymbal','bass']:
        return ensemble.voice(kind,midi,duration)
    t=np.arange(int(duration*SR))/SR;f=440*2**((midi-69)/12);y=np.zeros(len(t));attack=.008
    if kind=='piano':
        for h in range(1,min(16,int(SR/2/f))):
            for detune in [-.0008,.0006]:
                y+=np.sin(2*np.pi*f*h*(1+detune)*np.sqrt(1+.00005*h*h)*t)*np.exp(-t*(.7+h*.27))/(h**1.65)*.5
        y+=RNG.normal(0,.018,len(t))*np.exp(-t*120)
    elif kind=='pad':
        attack=.45
        for detune in [-.004,0,.003]:
            for h in [1,2,3,5]:y+=np.sin(2*np.pi*f*h*(1+detune)*t+.35*np.sin(2*np.pi*.17*t))/(h**2)*.23
        y*=.72+.18*np.sin(2*np.pi*.21*t)
    elif kind=='bell':
        for ratio,gain,decay in [(1,.65,.8),(2.01,.22,1.4),(2.77,.08,2),(4.03,.04,3)]:
            y+=gain*np.sin(2*np.pi*f*ratio*t)*np.exp(-t*decay)
    elif kind=='distbass':
        for h in range(1,min(15,int(SR/2/f))):y+=np.sin(2*np.pi*f*h*t)/(h**1.1)
        y=np.tanh(y*3)*np.exp(-t*3.3)
        y=np.convolve(y,np.ones(15)/15,mode='same')
        y+=.25*np.sin(2*np.pi*f*t)*np.exp(-t*3)
    elif kind=='kick':
        y=np.sin(2*np.pi*(44*t+5*(1-np.exp(-t*22))))*np.exp(-t*10)
        y+=RNG.normal(0,.14,len(t))*np.exp(-t*90);attack=.001
    elif kind=='hat':
        n=RNG.normal(0,.25,len(t));y=(n-np.roll(n,1))*np.exp(-t*55);attack=.001
    elif kind=='metal':
        for ratio in [1,1.413,2.613,3.87]:y+=.18*np.sin(2*np.pi*338*ratio*t)*np.exp(-t*6)
        y+=RNG.normal(0,.1,len(t))*np.exp(-t*25);attack=.001
    envelope=np.minimum(1,t/attack)*np.minimum(1,np.maximum(0,duration-t)/.06)
    return (y*envelope/max(1,np.max(np.abs(y)))).astype(np.float32)

def render(mode,bpm,bars,meter):
    beat=60/bpm;length=bars*meter*beat;tail=3.2
    mix=np.zeros((int((length+tail)*SR),2),np.float32)
    def put(kind,midi,start,dur,gain,pan=0):
        sample=note(kind,midi,round(dur*beat,4));at=int(start*beat*SR)
        n=min(len(sample),len(mix)-at)
        if n>0:
            mix[at:at+n,0]+=sample[:n]*gain*np.sqrt((1-pan)/2)
            mix[at:at+n,1]+=sample[:n]*gain*np.sqrt((1+pan)/2)
    for bar in range(bars):
        base=bar*meter
        if mode=='menu':
            root,chord=[(45,[57,60,64,71]),(41,[53,57,60,67]),(48,[60,64,67,74]),(43,[55,59,62,69])][(bar//2)%4]
            if bar%2==0:
                put('bass',root,base,5.95,.12)
                for j,n in enumerate(chord):put('pad',n,base,6.2,.16,[-.6,-.2,.2,.6][j])
            # Sparse three-beat piano phrases; deliberately no march, brass or snare.
            phrase=[[(76,0),(71,1.5)],[(72,.5)],[(69,0),(64,2)],[(67,1)],[(79,0),(76,1.5)],[(74,.5)],[(71,0),(67,2)],[(69,1)]][bar%8]
            for n,pos in phrase:put('piano',n,base+pos,2.7,.32,-.2)
            if bar%4==3:put('bell',chord[-1]+12,base+2,3,.09,.6)
            if bar>=16 and bar%2==0:put('choir',chord[1],base,6,.09,.3)
        elif mode=='battle':
            root,chord=[(40,[52,55,59]),(43,[55,59,62]),(36,[48,52,55]),(38,[50,54,57])][(bar//2)%4]
            sequence=[0,0,2,1,0,2,1,2]
            for i in range(8):
                put('strings',chord[sequence[i]]+12,base+i*.5,.36,.3,-.5 if i%2 else .5)
                put('bass',root+(12 if i%4==3 else 0),base+i*.5,.38,.25)
                put('hat',60,base+i*.5,.15,.1,.4)
            for pos in [0,1.5,2,2.75]:put('kick',36,base+pos,.6,.62)
            for pos in [1,3]:put('snare',60,base+pos,.35,.24,-.2)
            # Short answering strings, not the old shared horn theme.
            if bar%8>=4:
                melody=[[71,69,67,64],[67,66,64,62],[72,71,67,64],[66,69,67,62]][bar%4]
                for i,n in enumerate(melody):put('strings',n,base+i,.8,.22,.15)
            if bar%4==0:put('cymbal',60,base,3,.19,.35)
            if bar%8==7:
                for i in range(4):put('snare',60,base+3+i*.25,.18,.09+i*.025,-.2)
        elif mode=='boss':
            # Five-beat asymmetric industrial riff, low register and half-time impacts.
            root=[37,37,36,42,37,43,36,37][bar%8]
            riff=[0,0,12,1,0,7,6,0,-1,0]
            for i,offset in enumerate(riff):
                put('distbass',root+offset,base+i*.5,.42,.55,-.1)
                if i%2==0:put('strings',root+24+offset,base+i*.5,.35,.18,.55)
            for pos in [0,1.5,3,4.25]:put('kick',36,base+pos,.8,.8)
            for pos in [2,4]:put('snare',60,base+pos,.45,.33,.2)
            for pos in [.75,2.75,4.5]:put('metal',60,base+pos,.45,.22,-.55)
            if bar%2==0:
                for n in [root+24,root+25,root+31]:put('choir',n,base,5.2,.19,.3)
                put('horn',root+12,base,1.3,.45,-.25)
                put('timpani',root,base,2,.7)
            if bar%4==0:put('cymbal',60,base,4,.4,.5)
        elif mode=='victory':
            root,chord=[(43,[55,59,62]),(48,[60,64,67]),(50,[62,66,69]),(43,[55,59,62])][min(3,bar//3)]
            for j,n in enumerate(chord):
                put('strings',n,base,4.2,.19,[-.5,0,.5][j]);put('choir',n+12,base,4.2,.18,.2)
            put('bass',root,base,4,.28)
            fanfare=[[(67,1),(74,.5),(79,1.5),(78,1)],[(76,1.5),(74,.5),(71,2)],[(74,2),(79,2)],[(72,1),(76,1),(79,2)],[(81,1.5),(79,.5),(76,2)],[(79,2),(76,1),(72,1)],[(74,1),(78,1),(81,2)],[(83,1.5),(81,.5),(78,2)],[(81,1),(78,1),(74,2)],[(79,2),(74,1),(71,1)],[(67,4)],[(67,4)]][bar]
            pos=base
            for n,d in fanfare:
                put('horn',n-12,pos,d-.04,.46);put('horn',n,pos,d-.04,.17,-.2);pos+=d
            if bar<10:
                put('timpani',root,base,1.6,.4)
                if bar%3==0:put('cymbal',60,base,3,.23,.5)
                for pos in [1,3]:put('snare',60,base+pos,.3,.11,-.35)
            if bar==11:
                for n in chord:put('horn',n,base,5,.25)
        else:
            # Quiet three-beat lament; no drums or heroic fanfare.
            root,chord=[(40,[52,55,59]),(36,[48,52,55]),(45,[57,60,64]),(40,[52,55,59])][bar//2]
            for j,n in enumerate(chord):put('strings',n,base,3.3,.12,[-.5,0,.5][j])
            melody=[64,62,60,59,57,55,54,52][bar]
            put('piano',melody,base+.15,3.1,.42,-.15)
            put('piano',root,base,3.5,.23,.2)
            if bar in [0,4]:put('pad',root+12,base,6.2,.12,.4)
            if bar==7:put('piano',59,base+1,3.6,.12,-.15)
    dry=mix.copy()
    reflections=[(.061,.19),(.131,.13),(.271,.1),(.449,.075),(.739,.055),(1.103,.035),(1.673,.024)]
    for seconds,gain in reflections:
        d=int(seconds*SR);mix[d:]+=dry[:-d,::-1]*gain
    loop=mode in ['menu','battle','boss'];end=int(length*SR)
    if loop:
        mix[:len(mix)-end]+=mix[end:];mix=mix[:end]
        n=int(.008*SR);mix[:n]*=np.linspace(0,1,n)[:,None];mix[-n:]*=np.linspace(1,0,n)[:,None]
    else:mix[-int(2.5*SR):]*=np.linspace(1,0,int(2.5*SR))[:,None]
    mix-=mix.mean(axis=0);target={'menu':.12,'battle':.18,'boss':.2,'victory':.17,'defeat':.1}[mode]
    mix*=target/max(.001,np.sqrt(np.mean(mix**2)));mix=np.tanh(mix*1.05)/1.05
    mix*=min(1,.89/max(.001,np.max(np.abs(mix))))
    name='score-'+mode+'-v43';path=OUT/(name+'.wav')
    with wave.open(str(path),'wb')as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((mix*32767).astype('<i2').tobytes())
    subprocess.run([str(ensemble.FF),'-v','error','-y','-i',str(path),'-c:a','libvorbis','-q:a','4',str(path.with_suffix('.ogg'))],check=True)
    result={'name':name,'bpm':bpm,'meter':meter,'bars':bars,'seconds':round(len(mix)/SR,3),'loop':loop,'rms':round(float(np.sqrt(np.mean(mix**2))),4),'peak':round(float(np.max(np.abs(mix))),4)}
    print(json.dumps(result),flush=True);return result

if __name__=='__main__':
    report=[render('menu',68,24,3),render('battle',128,32,4),render('boss',142,24,5),render('victory',112,12,4),render('defeat',52,8,3)]
    (OUT/'score-v43-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
