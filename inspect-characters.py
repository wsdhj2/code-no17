"""Read-only atlas inspection; writes crop/anchor metadata, never edits image pixels."""
from pathlib import Path
from PIL import Image
import json

root=Path(__file__).parent
image=Image.open(root/'assets/characters-v5.png')
alpha=image.getchannel('A')
xs=[0,256,512,744,1024]
ys=[0,300,528,744,974,1210,1536]
names=['soldier','walker','runner','armored','bloater','giant']
heights=[48,41,43,45,49,49]
nominal=[245,210,205,225,235,285]
manifest={'image':'assets/characters-v5.png','width':image.width,'height':image.height,'characters':{}}
for row,name in enumerate(names):
    frames=[]
    for col in range(4):
        box=(xs[col],ys[row],xs[col+1],ys[row+1])
        mask=alpha.crop(box).point(lambda p:255 if p>50 else 0)
        bounds=mask.getbbox()
        if not bounds:raise RuntimeError('Empty frame '+name+' '+str(col))
        x0,y0,x1,y1=bounds
        frames.append({'x':box[0]+x0,'y':box[1]+y0,'w':x1-x0,'h':y1-y0,'center':(xs[col]+xs[col+1])/2})
    baseline=max(f['y']+f['h'] for f in frames[:3])
    manifest['characters'][name]={'base':baseline,'height':heights[row],'nominal':nominal[row],'frames':frames}
    print(name,'baseline',baseline,'frames',[(f['w'],f['h']) for f in frames])
(root/'assets/characters-v5-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(root/'assets/characters-v5-manifest.js').write_text('window.EmberSpriteManifest='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8')
