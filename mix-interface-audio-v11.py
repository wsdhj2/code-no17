from pathlib import Path
p=Path('audio.js');s=p.read_text(encoding='utf-8').replace('/* Original sample-based soundscape.', '/* Layered licensed field recordings and designed effects; see AUDIO-CREDITS.md.')
s=s.replace("this.cooldowns={};", "this.cooldowns={};this.duckUntil=0;this.variant=0;")
s=s.replace("['rifle-1','rifle-2','rifle-3','heavy','impact','armor','shield','explosion','infected-giant']", "['gun-pistol','gun-pistol-alt','gun-smg','gun-smg-alt','gun-rifle','gun-rifle-alt','gun-shotgun','gun-shotgun-alt','airstrike-flyby','airstrike-impact','orbital-cannon-impact','orbital-charge','orbital-beam-loop']")
s=s.replace("this.play('radio',.4)", "this.play('call-confirm',.25)")
s=s.replace("this.play(...sample);if(army>16", "const clip=type!=='laserCannon'&&this.variant++%2?sample[0]+'-alt':sample[0];this.play(clip,sample[1],.98+Math.random()*.04);if(army>16")
s=s.replace("this.play(sample[0],sample[1]*.3,sample[2]*1.03)", "this.play(clip,sample[1]*.18,1.04)")
s=s.replace("effectSound(source){const sample=", "effectSound(source){if(['bomb','orbitalBomb','boss'].includes(source))this.duckUntil=this.clock+1.1;const sample=")
s=s.replace("name===mode?this.levels.music*.65:0", "name===mode?this.levels.music*(this.clock<this.duckUntil?.25:.65):0")
s=s.replace("'air-strafe-cannon':.1", "'air-strafe-cannon':.1,'tank-machinegun':.1,'spitter-cast':.5,'empty-magazine':.3")
p.write_text(s,encoding='utf-8')
p=Path('frontline.js');s=p.read_text(encoding='utf-8')
s=s.replace("e.item==='mgTank'?'gun-smg':'grenade-launch'", "e.item==='mgTank'?'tank-machinegun':'grenade-launch'")
s=s.replace("if(e.type==='tankShot')", "if(e.type==='vehicleEmpty')mixer.play('empty-magazine',.3);if(e.type==='spit')mixer.play('spitter-cast',.45);if(e.type==='tankShot')")
s=s.replace('<span class="armory-serial">${', '<button id="weaponAudition" class="weapon-audition" aria-label="试听枪声">◖ 试听</button><span class="armory-serial">${')
s=s.replace("$('#deployStart').onclick=", "$('#weaponAudition').onclick=()=>{mixer.unlocked=true;mixer.lastVolley=-10;mixer.weaponVolley(b.weapon,8);};$('#deployStart').onclick=")
s=s.replace("function chooseLoadout(slot){const", "function chooseLoadout(slot){mixer.unlocked=true;mixer.play('ui-select',.2);const")
s=s.replace("b.slots[slot]=el.dataset.pick;", "mixer.play('ui-select',.3);b.slots[slot]=el.dataset.pick;")
p.write_text(s,encoding='utf-8')
p=Path('engine.js');s=p.read_text(encoding='utf-8').replace("e.ammo--;e.tick=", "e.ammo--;if(e.ammo===0)this.emit('vehicleEmpty',{item:e.type});e.tick=");p.write_text(s,encoding='utf-8')
# License and modification records ship with the game.
Path('assets/audio/AUDIO-CREDITS.md').write_text('''# Sound credits / v0.11

## The Free Firearm Sound Library — CC0 1.0
Recorded by Ben Jaszczak, Brian Nelson, Kevin Heras and Matthew Nanney.
https://opengameart.org/content/the-free-firearm-sound-library
https://creativecommons.org/publicdomain/zero/1.0/

Source files: 1911 A_42P/A_34P; Carl Gustav M45 G_31P/G_20P; Springfield 1917 B_24P/B_16P; Charles Daly H_21P/H_16P; AK-47 C_28P/C_31P.
Game derivatives: gun-pistol and alternate, gun-smg and alternate, gun-rifle and alternate, gun-shotgun and alternate, air-strafe-cannon, tank-machinegun. Trimmed to first shot, downmixed/resampled, level normalized with short fades. Source archives remain in the local authoring folder.

## Residue-sfx — FacadeGaikan — CC0 1.0
https://opengameart.org/content/residue-sfx
https://creativecommons.org/publicdomain/zero/1.0/
Sources: boom, lumosaw, emag, hurker, spit, zipper, ammopickup, quietship, emptyclip, ventilator.
Derived, trimmed and mixed into airstrike-impact, blast-grenade, orbital-cannon-impact, orbital-charge, orbital-beam-loop, laser-arrive, emp-pulse, spitter-cast, infected-bloater, metal-break, pickup-gear, lure-pulse, empty-magazine, ui-select, call-confirm, upgrade, rescue, gun-laser, shield-hit and vehicle-engine.

## Jet Engine Takeoff — dklon — CC BY 3.0
https://opengameart.org/content/jet-engine-takeoff
https://creativecommons.org/licenses/by/3.0/
Source: engine_takeoff.wav. Game derivative: airstrike-flyby, cropped, resampled and level adjusted.
Credit: Jet Engine Takeoff by dklon, licensed CC BY 3.0, via OpenGameArt.org.

Other music, ambience and legacy effects are original synthesized assets for Ember Front. Licensed recordings are not claimed as original recordings by this project.
''',encoding='utf-8')
