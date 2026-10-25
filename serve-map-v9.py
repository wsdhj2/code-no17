from pathlib import Path
from urllib.parse import quote
import json
svg=Path('assets/operation-map-v9.svg').read_text(encoding='utf-8')
Path('assets/operation-map-v9.js').write_text('window.EmberOperationMap='+json.dumps('data:image/svg+xml;charset=utf-8,'+quote(svg,safe=''))+';',encoding='utf-8')
p=Path('index.html');s=p.read_text(encoding='utf-8').replace('<script src="frontline.js">','<script src="assets/operation-map-v9.js"></script><script src="frontline.js">');p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8').replace('src="assets/operation-map-v9.svg"','src="${window.EmberOperationMap}"').replace('第${gun.unlock+1}关解锁','第${gun.unlock+1}章解锁');p.write_text(s,encoding='utf-8')
