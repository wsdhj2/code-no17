"""Original military science-fiction score, rendered locally without external samples.
Deterministic ensemble synthesis: detuned bowed strings, breathy brass,
formant choir, timpani, field snare and metallic cymbals. Not an OST recreation.
"""
from pathlib import Path
from functools import lru_cache
import json, subprocess, wave
import numpy as np
def lfilter(b,a,x):
    if len(a)==1:return np.convolve(x,b,mode='full')[:len(x)]
    kernel=b[0]*(-a[1])**np.arange(96)
    return np.convolve(x,kernel,mode='full')[:len(x)]

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/audio'
FF=ROOT.parent.parent/'work/video-inspect-deps/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SR=32000
RNG=np.random.default_rng(1741)

@lru_cache(maxsize=2048)
def voice(kind,note,duration):
    n=int(duration*SR);t=np.arange(n)/SR;f=440*2**((note-69)/12)
    y=np.zeros(n);attack=.045;release=.15
    if kind in ('horn','strings','choir','bass'):
        attack={'horn':.065,'strings':.11,'choir':.25,'bass':.015}[kind]
        release={'horn':.18,'strings':.25,'choir':.4,'bass':.09}[kind]
        # Multiple independently detuned desks, rather than a bare oscillator.
        for detune,phase in [(-.003,0),(.0015,1.2),(.004,2.7)]:
            fundamental=2*np.pi*f*(1+detune)*t+.004*f*np.sin(2*np.pi*4.7*t)/4.7
            for h in range(1,min(21,int(SR/2/f))):
                weight=(1/h**1.25)*np.exp(-h*f/(2500 if kind=='strings' else 1700))
                if kind=='horn':weight*=1+.6*np.exp(-((h*f-800)/500)**2)
                if kind=='choir':weight=(np.exp(-((h*f-650)/220)**2)+.55*np.exp(-((h*f-1150)/260)**2)+.2*np.exp(-((h*f-2600)/400)**2))/h**.7
                if kind=='bass':weight=1/h**2.2
                y+=np.sin(h*fundamental+phase)*weight/3
        if kind=='horn':y+=lfilter([.1],[1,-.9],RNG.normal(0,.025,n))
    elif kind=='snare':
        y=lfilter([1,-.85],[1],RNG.normal(0,.6,n))*np.exp(-t*18)
        y+=.4*np.sin(2*np.pi*185*t)*np.exp(-t*24);attack=.001;release=.015
    elif kind=='timpani':
        for ratio,gain in [(1,1),(1.5,.4),(2.04,.2)]:y+=gain*np.sin(2*np.pi*f*ratio*t+3*(1-np.exp(-t*12)))*np.exp(-t*4.5)
        y+=RNG.normal(0,.12,n)*np.exp(-t*50);attack=.002;release=.05
    elif kind=='cymbal':
        y=lfilter([1,-.98],[1],RNG.normal(0,.14,n))*np.exp(-t*2.3)
        for ratio in [1,1.414,1.932,2.542]:y+=.035*np.sin(2*np.pi*1780*ratio*t)*np.exp(-t*2)
        attack=.002;release=.06
    envelope=np.minimum(1,t/attack)*np.minimum(1,np.maximum(0,duration-t)/release)
    y=y*envelope
    return (y/max(1,np.max(np.abs(y)))).astype(np.float32)

def compose(name,bpm,bars,style):
    beat=60/bpm;length=bars*4*beat;tail=2.5
    mix=np.zeros((int((length+tail)*SR),2),np.float32)
    def put(kind,note,start,beats,gain,pan=0):
        sample=voice(kind,note,round(beats*beat,4));at=int(start*beat*SR)
        n=min(len(sample),len(mix)-at)
        if n<=0:return
        mix[at:at+n,0]+=sample[:n]*gain*np.sqrt((1-pan)/2)
        mix[at:at+n,1]+=sample[:n]*gain*np.sqrt((1+pan)/2)
    progression=[(38,50,53,57),(34,46,50,53),(41,53,57,60),(36,48,52,55)]
    if style=='victory':progression=[(38,50,54,57),(34,46,50,53),(43,55,59,62),(38,50,54,57)]
    # Original eight-bar theme with an answering phrase, varied by orchestration.
    motif=[[(62,1.5),(69,.5),(65,1),(64,1)],[(62,2),(57,1),(60,1)],[(65,1),(69,1),(72,1.5),(69,.5)],[(67,2),(64,1),(60,1)],[(62,1),(65,1),(69,2)],[(70,1.5),(69,.5),(65,1),(62,1)],[(67,1),(69,1),(64,1),(60,1)],[(61,2),(57,2)]]
    for bar in range(bars):
        root,*chord=progression[bar%4];base=bar*4
        swell=.72+.28*np.sin(np.pi*((bar%8)+1)/9)
        put('bass',root,base,3.95,.34)
        for j,note in enumerate(chord):
            put('strings',note+12,base,4.15,.15*swell,[-.55,.2,.6][j])
            if style!='battle' or bar>=8:put('choir',note+12,base,4.25,.16 if style=='menu' else .12,[-.35,0,.35][j])
        if style in ('battle','boss'):
            for step in range(8):
                note=chord[[0,1,2,1][step%4]]+12
                put('strings',note,base+step*.5,.42,.26 if style=='boss' else .21,-.5 if step%2 else .5)
                if step%2==0:put('bass',root,base+step*.5,.4,.12)
        phrase=motif[bar%8];pos=base
        for note,dur in phrase:
            if style=='victory' and note in (65,60,61):note+={65:1,60:2,61:1}[note]
            if style!='battle' or bar%16>=4:
                put('horn',note-12,pos,max(.2,dur-.06),.34*swell)
                if style in ('boss','victory') or bar>=16:put('horn',note,pos,max(.2,dur-.06),.19,-.12)
            pos+=dur
        # March rhythm changes between phrases, with rolls into section boundaries.
        for b in (0,2):put('timpani',root,base+b,.9,.58 if style!='menu' else .28,-.15)
        for b in (1,3):put('snare',60,base+b,.32,.24 if style!='menu' else .1,.22)
        if style in ('battle','boss'):
            for b in (1.5,2.75,3.5):put('snare',60,base+b,.2,.1,.22)
        if bar%4==3:
            for step in range(4):put('snare',60,base+3+step*.25,.18,.08+step*.025,.22)
        if bar%4==0:put('cymbal',60,base,3.2,.36 if style!='menu' else .16,.3)
    # Stereo early reflections and long hall tails, wrapping on loopable cues.
    dry=mix.copy()
    for seconds,gain in [(.041,.16),(.079,.12),(.137,.09),(.233,.075),(.389,.06),(.61,.045),(.93,.03), (1.37,.02)]:
        delay=int(seconds*SR);mix[delay:]+=dry[:-delay,::-1]*gain
    loop=style!='victory'
    end=int(length*SR)
    if loop:
        mix[:len(mix)-end]+=mix[end:];mix=mix[:end]
        # Join without a hard transient; the musical bar grid remains exact.
        n=int(.008*SR);mix[:n]*=np.linspace(0,1,n)[:,None];mix[-n:]*=np.linspace(1,0,n)[:,None]
    else:
        mix[-int(SR*1.5):]*=np.linspace(1,0,int(SR*1.5))[:,None]
    mix-=mix.mean(axis=0);rms=np.sqrt(np.mean(mix**2));mix*=.17/max(rms,.001)
    mix=np.tanh(mix*1.1)/1.1;mix*=min(1,.89/max(np.max(np.abs(mix)),.001))
    path=OUT/(name+'.wav')
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((mix*32767).astype('<i2').tobytes())
    subprocess.run([str(FF),'-v','error','-y','-i',str(path),'-c:a','libvorbis','-q:a','4',str(path.with_suffix('.ogg'))],check=True)
    result={'file':name,'bpm':bpm,'bars':bars,'seconds':round(len(mix)/SR,3),'loop':loop,'peak':round(float(np.max(np.abs(mix))),4),'rms':round(float(np.sqrt(np.mean(mix**2))),4)}
    print(json.dumps(result),flush=True);return result

if __name__=='__main__':
    report=[compose('score-menu-v41',84,24,'menu'),compose('score-battle-v41',124,32,'battle'),compose('score-boss-v41',140,24,'boss'),compose('score-victory-v41',104,8,'victory')]
    (OUT/'score-v41-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
