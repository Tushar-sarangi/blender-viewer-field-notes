> Modified by OpenAI Codex (OC) on 2026-10-23: added a Blender 5.x evaluated-animation sidecar for constraints, pose deformation, NLA, animated modifiers, and baked simulations. See [NOTICE](NOTICE) for upstream attribution and [LICENSE](LICENSE) for the complete Apache-2.0 text.

View Blender `.blend` files directly in the browser from a CORS-accessible URL. The viewer parses scene meshes, curves, text, materials, saved cameras, lights, and object transform animation from Blender 5.x files. It provides orbit controls, wireframe mode, camera fitting, and a looping frame timeline.

## Direct object animation

Object location, Euler/quaternion/axis-angle rotation, and scale keyframes from Blender actions play natively. The timeline has play/pause, frame scrubbing, and loop controls. Set `?autoplay=1` on the viewer URL to start playback when the scene is loaded.

## Blender-evaluated animation cache

The browser does not implement Blender's dependency graph or physics solvers. Use Blender itself to sample evaluated scene output into a companion cache while keeping the `.blend` file editable:

```sh
blender -b scene.blend --python blender-viewer-bake.py -- --step 1
```

The exporter writes `scene.blend.bva.gz`. When a `.blend` is loaded, the viewer tries that adjacent filename automatically. For a separately hosted cache, pass its CORS-accessible URL with the viewer's `bake` query parameter. On Blender 5.x, the exporter automatically bakes an unbaked rigid-body world over the requested frame interval. Bake cloth and other non-rigid-body physics caches in Blender first. Use `--no-physics-bake` to skip the rigid-body bake, or `--start`, `--end`, and `--step` to select the sample interval and density.

The cache records each sample's evaluated world transform and triangulated mesh, including split normals, the active UV layer, and material groups. It captures final visible geometry produced by constraints, armature deformation, pose animation, NLA, animated modifiers, and baked physics. The viewer plays those samples with its timeline; it does not run the original simulation in the browser.

## Scope and limits

Without a cache, the viewer supports object transform actions only. It does not evaluate bone controls, shape keys, constraints, animated modifiers, drivers, physics, or NLA itself. Cache playback covers mesh-like scene objects and their geometry/world transforms. It does not animate cameras, lights, material parameters, or expose editable rig controls. The viewer's native parser still omits its own evaluation of unapplied modifiers.

For generic examples that exercise Follow Path/Copy Location constraints, armature pose deformation, a repeated NLA strip, an animated Simple Deform modifier, and rigid-body dominoes, see [`examples/build_evaluated_demos.py`](examples/build_evaluated_demos.py).
