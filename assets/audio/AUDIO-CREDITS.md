# Sound credits / v0.11

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

Laser sustain v0.13: original band-limited noise texture, generated as a periodic four-second loop. Replaces the repeated lumosaw-derived laser snippets during gameplay.

v0.15: ui-input/ui-confirm/ui-cancel/ui-open/ui-error and laser-sustain-v15 are original designed short textures and a periodic continuous noise loop. enemy-rifle is derived from Free Firearm Sound Library B_16P; mech-servo derives from Residue ventilator. Licensed sources above remain applicable.

v0.16 radio notifications: local Windows SAPI synthesized speech using Microsoft Zira/David/Huihui, processed for radio bandwidth. Original written notification text; no sampled Helldivers or Arknights voice lines. radio-static is original noise synthesis. Voice-source scripts are authoring tools, not required by the offline game.


v0.41 score: score-menu-v41, score-battle-v41, score-boss-v41 and score-victory-v41 are original compositions and locally synthesized stereo ensemble renders. Source: tools/compose-score-v41.py. No third-party music recordings, melodies or soundfonts. WAV masters and OGG game versions.


v0.43 score: five independent original compositions score-menu-v43, score-battle-v43, score-boss-v43, score-victory-v43 and score-defeat-v43. Source: tools/compose-score-v43.py, reusing instrument synthesis from compose-score-v41.py. All local synthesis, no third-party recordings, melodies or soundfont samples. Distinct meters, themes and instrumentation; 32 kHz stereo WAV and OGG.


v0.44 orbital cannon: orbital-designate-v44 and orbital-incoming-v44 are original noise/pressure designs. orbital-impact-v44 derives from the existing credited Residue-based orbital-cannon-impact, mixed with original sub/low-mid pressure synthesis and stereo reflections. No Helldivers recordings are sampled. Source: tools/build-orbital-v44.py.


v0.62 transport cues: dropship-inbound-v62, dropship-fall-v62 and dropship-impact-v62 layer the existing credited aircraft, vehicle, metal and debris recordings. Source: tools/build-dropship-audio-v62.py. No Helldivers recordings sampled.
v0.75 reinforcement arrival radio: original local Microsoft Zira speech, text "Reinforcements have arrived."; filtered to a radio band and played at 1.18x. Source: tools/build-reinforcement-voice-v75.ps1. Triggered once when the reinforcement truck arrives, separate from supply notifications.
