"""Layer existing licensed game recordings into transport-specific cues."""
from pathlib import Path
import wave
import numpy as np
root=Path('assets/audio');sr=24000
def read(name,rate=1):
    with wave.open(str(root/(name+'.wav')),'rb') as w:
        width=w.getsampwidth();channels=w.getnchannels();source=w.getframerate();raw=w.readframes(w.getnframes())
    assert width==2
    data=np.frombuffer(raw,dtype='<i2').astype(float).reshape(-1,channels).mean(axis=1)/32768
    return np.interp(np.arange(int(len(data)*sr/source/rate))*source*rate/sr,np.arange(len(data)),data)
def mix(seconds,layers,name):
    out=np.zeros(int(seconds*sr))
    for sample,start,gain,pitch in layers:
        d=read(sample,pitch);at=int(start*sr);n=min(len(d),len(out)-at)
        if n>0:out[at:at+n]+=d[:n]*gain
    fade=min(int(sr*.12),len(out)//2);out[:fade]*=np.linspace(0,1,fade);out[-fade:]*=np.linspace(1,0,fade)
    out=np.tanh(out*1.4)*.82
    with wave.open(str(root/(name+'.wav')),'wb') as w:w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes((out*32767).astype('<i2').tobytes())
mix(6,[('airstrike-flyby',0,.45,.65),('vehicle-engine',.2,.9,.8),('vehicle-engine',2,.6,.82),('vehicle-engine',3.7,.5,.85)],'dropship-inbound-v62')
mix(1.2,[('metal-break',0,.7,.65),('airstrike-flyby',0,.5,1.7),('debris',.3,.5,1)],'dropship-fall-v62')
mix(3.4,[('airstrike-impact',0,.75,.75),('metal-break',.08,.65,.8),('debris',.2,.75,.7),('explosion',0,.4,.65)],'dropship-impact-v62')
print('Created transport inbound, damage/fall and debris impact cues')
