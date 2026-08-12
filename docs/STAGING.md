# Single staging gate

Reuse the disposable Minecraft/BlueMap server and PVC. Install the exact All
the Mons 1.2.0 Chipped/Athena pair and only the candidate add-on in BlueMap's
packs directory. Use a bounded map named `chipped_staging`.

Before startup apply the shared low-cost test settings:

```ini
advance_time=false
advance_weather=false
random_tick_speed=0
spread_vines=false
spawn_mobs=false
spawn_monsters=false
spawn_patrols=false
spawn_phantoms=false
spawn_wandering_traders=false
spawn_wardens=false
spawner_blocks_work=false
pvp=false
player_movement_check=false
freeze_damage=false
fire_damage=false
fall_damage=false
drowning_damage=false
raids=false
global_sound_events=false
```

Run one enabled lifecycle:

1. Install the generated datapack, start once, run
   `function chipped_gallery:build`, then `function chipped_gallery:verify`.
   Require the generated routed-block registry/placement census and zero
   failures.
2. Save and restart once; rerun only the verifier and require the same result.
3. Require exact dual-artifact/schema activation with no adapter, resource, or
   render failure. Purge/render only the bounded gallery map.
4. Require nonempty rendered models for every census block and inspect the
   structural anchors: transparent CTM/pillar/giant/limited/panes, adjacent
   carpets, face-local seams, axes, mural phase, and pane topology.
5. Open the exact external `#chipped_staging` link in the agent browser for a
   quick blank/black/missing/gross-breakage check before presenting it to the
   owner.

Record results only after they occur. This implementation candidate has no
staging or owner-acceptance claim yet.
