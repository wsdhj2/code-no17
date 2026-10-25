from urllib.request import urlopen,Request
import re,json
from pathlib import Path
pages=['the-free-firearm-sound-library','residue-sfx','jet-engine-takeoff']
for slug in pages:
 html=urlopen(Request('https://opengameart.org/content/'+slug,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode()
 links=re.findall(r'href="([^"]+/sites/default/files/[^"]+)"',html)
 print(slug, list(dict.fromkeys(links)))
