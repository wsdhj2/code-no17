from pathlib import Path
import numpy as np,wave
rng=np.random.default_rng(1601);sr=22050
for p in Path('voice-sources').glob('*.wav'):
 with wave.open(str(p)) as f:
  data=f.readframes(f.getnframes());rate=f.getframerate();channels=f.getnchannels()
 if not data:continue
 x=np.frombuffer(data,dtype='<i2').astype(float)/32768
 if channels>1:x=x.reshape(-1,channels).mean(axis=1)
 if rate!=sr:x=np.interp(np.arange(int(len(x)*sr/rate))*rate/sr,np.arange(len(x)),x)
 # Communication bandwidth with a little saturation and a soft squelch, preserving intelligibility.
 freq=np.fft.rfftfreq(len(x),1/sr);shape=(1-np.exp(-(freq/220)**4))*np.exp(-(freq/3400)**6);x=np.fft.irfft(np.fft.rfft(x)*shape,n=len(x));x=np.tanh(x*1.6);x=x/max(.01,max(abs(x)))*.75
 pad=int(sr*.045);noise=rng.normal(0,.025,pad)*np.sin(np.linspace(0,np.pi,pad));x=np.concatenate([noise,x,noise*.65])
 with wave.open('assets/audio/voice-'+p.name,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(x,-1,1)*32767).astype('<i2').tobytes())
t=np.arange(int(sr*.85))/sr;n=rng.normal(size=len(t));n=np.convolve(n,np.ones(4)/4,'same');n*=.12*(.35+.65*np.sin(t*47)**2)*np.minimum(t/.025,1)*np.maximum(0,1-t/.85)
with wave.open('assets/audio/radio-static.wav','wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((n*32767).astype('<i2').tobytes())
print('Radio notifications rendered')
