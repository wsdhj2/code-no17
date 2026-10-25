import zipfile
from pathlib import Path
p=Path('audio-sources')
with zipfile.ZipFile(p/'residue.zip') as z:
 print('\n'.join(z.namelist()));z.extractall(p/'residue')
