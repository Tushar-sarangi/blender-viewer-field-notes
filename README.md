# Frame / Field — Blender Viewer Showcase

**Open the live browser viewer:** [tushar-sarangi.github.io/blender-viewer-field-notes](https://tushar-sarangi.github.io/blender-viewer-field-notes/?v=lift-camera-v3)

Jump straight to the animated default cube: [First Lift](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=cube&v=lift-camera-v3).

The landing page embeds the orbitable viewer at figure scale. Choose one of three scenes, then drag to orbit, scroll to zoom, and use the viewer's Play, Loop, and timeline controls.

## Examples

- **Lantern Ridge** — an amber-lit courier crosses an A.N.T. Landscape mountain range. [Open in the live viewer](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=lantern&v=lift-camera-v3) · [Download the editable scene](assets/lantern-ridge.blend)
- **Paper Moon** — a signal probe moves over a layered dusk landscape. [Open in the live viewer](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=moon&v=lift-camera-v3) · [Download the editable scene](assets/paper-moon-signal.blend)
- **First Lift** — the Blender default cube rises on Z, returns to its start, and loops with stepped object-action keys. [Open in the live viewer](https://tushar-sarangi.github.io/blender-viewer-field-notes/?scene=cube&v=lift-camera-v3) · [Download the editable scene](assets/default-cube.blend)

![First Lift looping preview, rendered from the same Blender scene](assets/default-cube-loop.gif?v=lift-camera-v3)

First Lift's camera is centered and widened to keep the cube's complete vertical motion in frame. The looping preview is rendered from that same camera and `.blend` file.

The viewer and scenes are bundled on this Pages origin, so visitors do not need access to the private source repository. See [blender-viewer.docs.md](blender-viewer.docs.md) for supported animation data and limitations.

## Attribution and license

The browser viewer derives from Simon Willison's [`simonw/tools`](https://github.com/simonw/tools) and is distributed under Apache License 2.0. The full license text is in [LICENSE](LICENSE); [NOTICE](NOTICE) records attribution and significant changes, including the OC initials in the Blender sample. The terrain meshes were generated with A.N.T. Landscape 0.2.0; its attribution is also in `NOTICE`. The extension source is not included.

