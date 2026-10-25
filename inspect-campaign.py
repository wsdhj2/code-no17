from pathlib import Path
from PIL import Image
import json
root=Path('assets')
def box(image,rect):
 x,y,r,b=rect;im=image.crop(rect);alpha=im.getchannel('A').point(lambda n:255 if n>20 else 0);bb=alpha.getbbox()
 if not bb: raise RuntimeError(rect)
 l,t,rr,bb=bb;return dict(x=x+l,y=y+t,w=rr-l,h=bb-t)
boss=Image.open(root/'campaign-bosses-v7b.png');escort=Image.open(root/'escorts-v7.png');print(boss.size,escort.size)
# Deliberately measured atlas cells; keep generated originals untouched.
cols=[(0,480),(480,748),(748,1050),(1050,boss.width)]
rows=[(0,255),(260,530),(535,740),(744,943),(944,boss.height)]
bosses=[[box(boss,(l,t,r,b)) for l,r in cols] for t,b in rows]
ew=escort.width;eh=escort.height
escorts=[[box(escort,(l,t,r,b)) for l,r in [(0,425),(425,860),(860,ew)]] for t,b in [(0,405),(405,790),(790,eh)]]
# Use complete idle figures for portraits where the large illustrated column overlaps rows.
bosses[2][0]=dict(bosses[2][1]);bosses[4][0]=dict(bosses[4][1])
data={'boss':bosses,'escort':escorts}
(root/'campaign-manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'campaign-manifest.js').write_text('window.EmberCampaignManifest='+json.dumps(data)+';',encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace("bossAtlas.src='assets/campaign-bosses-v7.png'","bossAtlas.src='assets/campaign-bosses-v7b.png'");p.write_text(s,encoding='utf-8')
