from urllib.request import urlopen,Request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import zipfile
root=Path('audio-sources');root.mkdir(exist_ok=True)
urls={'firearms.7z':'https://opengameart.org/sites/default/files/Prepared%20SFX%20Library.7z','residue.zip':'https://opengameart.org/sites/default/files/residue-sfx.zip','engine_takeoff.wav':'https://opengameart.org/sites/default/files/engine_takeoff.wav'}
def download(pair):
 name,url=pair;p=root/name
 if not p.exists():
  with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r,p.open('wb') as f:
   while True:
    b=r.read(1024*1024)
    if not b:break
    f.write(b)
 return name,p.stat().st_size
with ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(download,urls.items()):print(result,flush=True)
with zipfile.ZipFile(root/'residue.zip') as z:print(z.namelist())
