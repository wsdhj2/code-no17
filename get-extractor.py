from urllib.request import urlopen
from pathlib import Path
p=Path('audio-sources/7zr.exe')
if not p.exists():p.write_bytes(urlopen('https://www.7-zip.org/a/7zr.exe',timeout=25).read())
print(p.stat().st_size)
