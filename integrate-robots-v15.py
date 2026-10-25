from pathlib import Path
from PIL import Image
import numpy as np,json,random,urllib.parse
manifest={}
for kind,name,cuts in [('boss','mech-bosses-v15.png',[0,280,566,828,1128,1536]),('robot','robot-enemies-v15.png',[0,294,591,934,1204,1536])]:
 im=Image.open('assets/'+name);arr=np.array(im);rows=[]
 for row in range(5):
  frames=[]
  for col in range(2):
   x0,x1=col*512,(col+1)*512;y0,y1=cuts[row],cuts[row+1];alpha=arr[y0:y1,x0:x1,3];ys,xs=np.where(alpha>180)
   frames.append({'x':int(x0+xs.min()),'y':int(y0+ys.min()),'w':int(xs.max()-xs.min()+1),'h':int(ys.max()-ys.min()+1)})
  rows.append(frames)
 manifest[kind]=rows
Path('assets/robot-manifest-v15.js').write_text('window.EmberRobotManifest='+json.dumps(manifest)+';',encoding='utf-8')
p=Path('index.html');s=p.read_text(encoding='utf-8').replace('<script src="characters.js">','<script src="assets/robot-manifest-v15.js"></script><script src="characters.js">');p.write_text(s,encoding='utf-8')
# Draw a code-native city/industrial campaign map, matching all 26 nodes.
height=145+26*105+10*55+30+125;r=random.Random(1515)
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {height}"><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#6d8899" stroke-opacity=".1"/></pattern></defs><path fill="#17232c" d="M0 0h720v{height}H0z"/><path fill="url(#grid)" d="M0 0h720v{height}H0z"/>']
for i in range(240):
 x=r.randrange(-15,680);y=r.randrange(height);w=r.randrange(25,85);h=r.randrange(30,100);parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{r.choice(["#26343f","#23313b","#2b3d47"])}" stroke="#8ba1ac" stroke-opacity=".12"/>')
for y in range(280,height,330):parts.append(f'<path d="M0 {y}H720" stroke="#0e1b25" stroke-width="22"/><path d="M0 {y}H720" stroke="#7493a0" stroke-opacity=".2"/>')
parts.append(f'<path d="M160 0V800L260 1100V1600L150 1900V{height}" fill="none" stroke="#0b1922" stroke-width="27"/><path d="M0 {height//2}H720" stroke="#8aa8b0" stroke-dasharray="8 12" stroke-opacity=".45"/><text x="35" y="{height//2-15}" fill="#7c9ca8" font-family="monospace" font-size="13">MACHINE QUARANTINE ZONE</text></svg>')
svg=''.join(parts);Path('assets/operation-map-v15.svg').write_text(svg,encoding='utf-8');Path('assets/operation-map-v15.js').write_text('window.EmberOperationMap='+json.dumps('data:image/svg+xml,'+urllib.parse.quote(svg))+';',encoding='utf-8')
p=Path('index.html');s=p.read_text(encoding='utf-8').replace('assets/operation-map-v9.js','assets/operation-map-v15.js');p.write_text(s,encoding='utf-8')
