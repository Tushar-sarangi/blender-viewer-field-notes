> Modified by OpenAI Codex (OC) on 2026-10-21: added Blender 5.x object-action playback and looping timeline controls. See [NOTICE](NOTICE) for upstream attribution and [LICENSE](LICENSE) for the full Apache-2.0 text.

View Blender .blend files directly in your browser by pasting a URL to a CORS-accessible file or GitHub repository link. The viewer renders mesh geometry, curves, and text with materials, lighting, and optional saved camera positions from Blender 5.x files, providing interactive orbit controls, wireframe mode, and model fitting capabilities.

Object location, Euler/quaternion/axis-angle rotation, and scale keyframes play directly from Blender 5.x animation actions. The viewer includes play/pause, frame scrubbing, and looping across the scene frame range. This first pass does not evaluate armature/pose animation, shape keys, animated modifiers, drivers, or NLA blending; those channels remain at their saved pose.

