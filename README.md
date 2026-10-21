# Frame / Field — Blender Viewer Showcase

A standalone GitHub Pages bundle for the Blender 5.x viewer work in the private [Tushar-sarangi/tools](https://github.com/Tushar-sarangi/tools) repository.

## Contents

- `index.html`: cinematic landing page with two scene cards and an embedded orbitable viewer
- `blender-viewer.html`: the fork's browser viewer, including direct object-action timeline playback and looping
- `assets/*.blend`: two editable Blender 5.0 A.N.T. Landscape scenes
- `assets/*-loop.gif` and `assets/*-poster.png`: motion and still previews
- `LICENSE`, `NOTICE`, and `blender-viewer.docs.md`: upstream license, attribution, modifications, and viewer limitations

The page loads its `.blend` files from its own Pages origin. Visitors do not need access to the private source repository. This is a deliberately small public showcase bundle; it does not copy the rest of the `tools` repository. No `CNAME` is included, so it cannot claim the upstream `tools.simonwillison.net` domain.

## Publish with GitHub Pages

For a GitHub Free account, the Pages source repository must be public. Create a separate public repository for this bundle, upload its contents, then choose **Settings → Pages → Deploy from a branch → main → /(root)**. The generated project URL follows `https://<owner>.github.io/<repository>/`.

Public Pages visitors can access the bundled viewer source, Blender scene files, preview GIFs, and posters. Keep the original `tools` repository private.

## Attribution

The source viewer derives from Simon Willison's `simonw/tools`, licensed under Apache License 2.0. The terrain scenes use generated meshes from the official A.N.T. Landscape extension (0.2.0), credited in `NOTICE`. The add-on source is not included.