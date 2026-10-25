from pathlib import Path
p=Path('audio.js');s=p.read_text(encoding='utf-8')
s=s.replace("const root='assets/audio/';", "const root='assets/audio/';\nconst VOICE_LINES={airstrike:'Air strike incoming.',orbital:'Orbital strike incoming.',supply:'Supply inbound.',armor:'Armored support inbound.',shield:'Shield deployment confirmed.',emp:'EMP strike confirmed.',linked:'Command link established.',warning:'Heavy hostile approaching.',objective:'Objective complete. Proceed to extraction.',unknown:'还有活人吗？收到请回答。'};")
s=s.replace("this.previewUntil=0;", "this.previewUntil=0;",1)
s=s.replace("this.levels={sfx:.65,music:.38,ambience:.3};", "this.levels={sfx:.65,music:.38,ambience:.3,voice:.85};this.voiceQueue=[];this.voiceHistory={};this.voiceCue=null;this.dialogue=false;this.speech=new Audio();this.speech.preload='auto';this.speech.onended=()=>{this.voiceCue=null;this.nextVoice();};this.speech.onerror=()=>{this.voiceCue=null;this.nextVoice();};")
pos=s.index(' stopLaser(){')
s=s[:pos]+''' speak(cue){if(!VOICE_LINES[cue]||!this.enabled||!this.unlocked)return;if(this.clock-(this.voiceHistory[cue]??-99)<3||this.voiceQueue.includes(cue)||this.voiceCue===cue)return;this.voiceHistory[cue]=this.clock;if(this.voiceQueue.length>=3)this.voiceQueue.shift();this.voiceQueue.push(cue);if(!this.voiceCue)this.nextVoice();}
 nextVoice(){if(!this.enabled){this.stopSpeech();return;}const cue=this.voiceQueue.shift();const notice=document.querySelector('#radioNotice');if(!cue){if(notice)notice.hidden=true;return;}this.voiceCue=cue;this.speech.src=root+'voice-'+cue+'.wav';this.speech.volume=this.levels.voice;this.speech.play().catch(()=>{this.voiceCue=null;if(notice)notice.hidden=true;});this.counts['voice-'+cue]=(this.counts['voice-'+cue]||0)+1;let el=notice;if(!el){el=document.createElement('aside');el.id='radioNotice';el.innerHTML='<small>林澈 / 指挥部频道</small><b></b>';document.querySelector('#frame')?.append(el);}el.querySelector('b').textContent=VOICE_LINES[cue];el.hidden=this.dialogue;}
 stopSpeech(){this.voiceQueue=[];this.voiceCue=null;this.speech.pause();try{this.speech.currentTime=0;}catch{}const el=document.querySelector('#radioNotice');if(el)el.hidden=true;}
'''+s[pos:]
s=s.replace("beginRun(){this.stopLaser();", "beginRun(){this.stopSpeech();this.voiceHistory={};this.stopLaser();")
s=s.replace("if(!this.enabled){this.stopLaser();", "if(!this.enabled){this.stopSpeech();this.stopLaser();")
s=s.replace("if(mode==='paused'){", "if(mode==='paused'){if(!this.dialogue)this.stopSpeech();")
s=s.replace("this.clock+=dt;this.setMode(mode);", "this.clock+=dt;this.setMode(mode);if(this.voiceCue&&!this.speech.paused){this.speech.volume=this.levels.voice;this.duckUntil=this.clock+.1;}const caption=document.querySelector('#radioNotice');if(caption&&this.dialogue)caption.hidden=true;")
s=s.replace("['ambience','环境氛围']", "['ambience','环境氛围'],['voice','无线电语音']")
s=s.replace("laser:{paused:", "voice:{cue:this.voiceCue,queue:[...this.voiceQueue],paused:this.speech.paused,error:this.speech.error?.code??null},laser:{paused:")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace("function clearStoryUI(){prologue=null;", "function clearStoryUI(){mixer.dialogue=false;mixer.stopSpeech();prologue=null;")
s=s.replace("run.pause();mixer.setMode('paused');", "run.pause();mixer.dialogue=true;mixer.setMode('paused');")
s=s.replace("function closeComms(){mixer.stopSpeech();", "function closeComms(){mixer.dialogue=false;mixer.stopSpeech();")
p.write_text(s,encoding='utf-8')
