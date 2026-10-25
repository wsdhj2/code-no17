from pathlib import Path
p=Path('qa-chapters-v9.cjs');s=p.read_text(encoding='utf-8').replace("p.locator('[data-heavy=\"laser\"]')","p.locator('[data-slot=\"0\"]')");p.write_text(s,encoding='utf-8')
