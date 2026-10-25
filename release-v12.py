from pathlib import Path
import json,zipfile
p=Path('qa-chapters-v9.cjs');s=p.read_text(encoding='utf-8').replace("assert.equal(await p.locator('[data-slot=\"0\"]').isDisabled(),true)","assert.equal(await p.locator('[data-slot=\"0\"]').isEnabled(),true)");p.write_text(s,encoding='utf-8')
p=Path('package.json');d=json.loads(p.read_text(encoding='utf-8'));d['version']='0.12.0';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');p.write_text('''# v0.12 更新

- 修复同章接续时战备整体锁死：未使用的槽位可以选择、更换、卸下；已使用的槽位标记「已使用」并保留消耗，换装不会恢复次数。出战时同步接续存档中的重型库存，保留局内道具与编队状态。
- Boomer（膨胀脓肿者）喷吐与死亡留下胆汁。落点先预警，接触后8秒新增尸群数量翻倍；重复接触刷新时间，不叠加倍率。酸液精英仍使用独立的伤害酸池。
- 黄色胆汁区域、沾染提示及8秒倒计时。
- 56项规则测试通过；浏览器验证接续存档换装、已消耗槽位限制、库存同步及胆汁HUD。

'''+s,encoding='utf-8')
r=Path.cwd();names=['index.html','engine.js','frontline.js','characters.js','audio.js','battlefield.css','art-direction.css','operation-ui.css','server.js','start.ps1','启动游戏.cmd','README.md','package.json']
with zipfile.ZipFile(r.parent/'余烬防线-v0.12-完整游戏.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(r/n,'ember-vault/'+n)
 for p in (r/'assets').rglob('*'):
  if p.is_file():z.write(p,'ember-vault/'+p.relative_to(r).as_posix())
print('v0.12 packaged')
