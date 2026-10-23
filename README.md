# Frame / Field — Blender Viewer Showcase

**Open the live orbitable viewer:** [Frame / Field](https://tushar-sarangi.github.io/blender-viewer-field-notes/?v=evaluated-cache-v1)

The landing page embeds the viewer at figure scale. Choose a scene, drag to orbit, scroll to zoom, and use Play, Loop, and the frame scrubber.

## Examples

- **Lantern Ridge** — a stop-motion courier crosses a procedural A.N.T. Landscape range. [View](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=lantern) · [Download `.blend`](assets/lantern-ridge.blend)
- **Paper Moon** — a signal probe moves through a layered dusk landscape. [View](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=moon) · [Download `.blend`](assets/paper-moon-signal.blend)
- **First Lift** — the default cube rises along Z, returns, and loops on object-action keys. [View](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=cube) · [Download `.blend`](assets/default-cube.blend)
- **Constraint Arc** — Follow Path and Copy Location constraints move a signal and beacon around an orbit. [View](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=constraint) · [Download `.blend`](assets/constraint-arc.blend)
- **Motion Mechanics** — armature pose animation repeats in NLA beside an animated Simple Deform modifier and a rigid-body domino / marble study. [View](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=mechanics) · [Download `.blend`](assets/motion-mechanics.blend)

The two advanced examples include adjacent `.bva.gz` files. These contain sampled geometry and world transforms produced by Blender's evaluated dependency graph, allowing the browser viewer to display constraints, rig deformation, NLA, animated modifiers, and physics results. Blender performs the evaluation; the browser replays the samples. The `.blend` files remain the editable source scenes.

## Rebuild an evaluated cache

With Blender 5.x installed, run the exporter for a saved scene:

```sh
blender -b scene.blend --python blender-viewer-bake.py -- --step 1
```

The exporter writes `scene.blend.bva.gz`. It automatically bakes an unbaked rigid-body world; bake cloth and other non-rigid-body caches in Blender first. Adjust the interval with `--start`, `--end`, and `--step`. The viewer looks for the sidecar beside the `.blend` file or accepts an explicit `bake` URL parameter.

To recreate the two generic advanced sample scenes and previews:

```sh
blender --background --python examples/build_evaluated_demos.py -- --output-dir assets
blender -b assets/constraint-arc.blend --python blender-viewer-bake.py -- --step 2
blender -b assets/motion-mechanics.blend --python blender-viewer-bake.py -- --step 2
```

This standalone Pages bundle includes the viewer, editable scenes, caches, preview art, and licensing files, so it does not depend on access to the private source fork. Full attribution and the Apache License 2.0 text are in [NOTICE](NOTICE) and [LICENSE](LICENSE). Terrain meshes were generated with A.N.T. Landscape 0.2.0; its extension source is not included.
