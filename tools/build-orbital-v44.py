"""Layered orbital cannon cue. Derives from the existing credited explosion texture.
Adds original sub/low-mid pressure, falling shell noise, charge and stereo reflections.
"""
from pathlib import Path
import json, subprocess, wave
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/audio'
FF=ROOT.parent.parent/'work/video-inspect-deps/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
SR=32000;RNG=np.random.default_rng(1744);report=[]
def read(name):
    return np.frombuffer(subprocess.check_output([str(FF),'-v','error','-i',str(OUT/name),'-f','f32le','-ar',str(SR),'-ac','1','-']),dtype='<f4').copy()
def smooth(x,n):return np.convolve(x,np.ones(n)/n,mode='same')
def save(name,x,peak=.93):
    if x.ndim==1:x=np.column_stack([x,x])
    x-=x.mean(axis=0);x*=peak/max(.001,np.max(np.abs(x)))
    n=int(.003*SR);x[:n]*=np.linspace(0,1,n)[:,None];x[-int(.18*SR):]*=np.linspace(1,0,int(.18*SR))[:,None]
    with wave.open(str(OUT/(name+'.wav')),'wb')as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
    report.append({'file':name+'.wav','seconds':len(x)/SR,'peak':round(float(np.max(np.abs(x))),4),'rms':round(float(np.sqrt(np.mean(x*x))),4)})

t=np.arange(int(.48*SR))/SR;n=RNG.normal(0,1,len(t))
x=smooth(n,29)*np.exp(-t*13)*.7+(np.sin(2*np.pi*145*t)+.3*np.sin(2*np.pi*290*t))*np.exp(-t*15)*.2
save('orbital-designate-v44',x,.66)
t=np.arange(int(.75*SR))/SR;n=RNG.normal(0,1,len(t));rise=(t/.75)**1.2
x=(smooth(n,15)-smooth(n,140))*rise*2
x+=np.sin(2*np.pi*(900*t-480*t*t))*.18*rise
x+=np.sin(2*np.pi*(65*t+30*t*t))*.3*rise
save('orbital-incoming-v44',x,.83)
t=np.arange(int(6.4*SR))/SR;n=RNG.normal(0,1,len(t));mono=np.zeros(len(t))
source=read('orbital-cannon-impact.wav');mono[:len(source)]+=source*.94
low=smooth(n,160);low/=max(.001,np.std(low));mid=smooth(n,32);mid/=max(.001,np.std(mid))
mono+=low*.33*np.exp(-t*.85)*(1-np.exp(-t*45))
mono+=mid*.17*np.exp(-t*2.8)*(1-np.exp(-t*100))
mono+=np.sin(2*np.pi*(39*t+2.8*(1-np.exp(-t*18))))*.43*np.exp(-t*1.8)
mono+=np.sin(2*np.pi*93*t)*.2*np.exp(-t*3.7)+np.sin(2*np.pi*177*t)*.13*np.exp(-t*6)
mono+=(n-smooth(n,7))*.15*np.exp(-t*38)
mono=np.tanh(mono*1.3);stereo=np.column_stack([mono,mono])
for seconds,gain in [(.079,.23),(.19,.19),(.36,.15),(.69,.1),(1.17,.07)]:
    d=int(seconds*SR);stereo[d:,0]+=mono[:-d]*gain
    d+=int(.013*SR);stereo[d:,1]+=mono[:-d]*gain
save('orbital-impact-v44',stereo)
(OUT/'orbital-v44-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
