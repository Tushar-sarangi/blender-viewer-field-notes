"""Bake Blender's evaluated mesh animation for the browser viewer.

Run with Blender 5.x:
  blender -b scene.blend --python blender-viewer-bake.py -- --step 1

The output is ``scene.blend.bva.gz``. Keep the editable .blend and this cache
beside one another on a CORS-accessible host. The browser plays these sampled
results; Blender remains responsible for evaluating constraints, rigs, NLA,
modifiers, and simulation caches.
"""

from __future__ import annotations

import argparse
import array
import gzip
import hashlib
import json
import os
import struct
import sys
from typing import Any

import bpy


MAGIC = b"BVA1"
GEOMETRY_TYPES = {"MESH", "CURVE", "SURFACE", "FONT", "META"}


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="output cache path (default: <blend>.bva.gz)")
    parser.add_argument("--start", type=int, help="first frame (default: scene start)")
    parser.add_argument("--end", type=int, help="last frame (default: scene end)")
    parser.add_argument("--step", type=int, default=1, help="sample every N frames")
    parser.add_argument(
        "--no-physics-bake",
        action="store_true",
        help="skip automatic baking of an unbaked rigid-body world cache",
    )
    return parser.parse_args(argv)


def f32_bytes(values: list[float]) -> bytes:
    packed = array.array("f", values)
    if sys.byteorder != "little":
        packed.byteswap()
    return packed.tobytes()


def matrix_column_major(matrix: Any) -> list[float]:
    return [float(matrix[row][column]) for column in range(4) for row in range(4)]


def evaluated_mesh(obj_eval: Any, depsgraph: Any) -> Any:
    try:
        return obj_eval.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
    except TypeError:
        # Blender versions before the preserve_all_data_layers argument.
        return obj_eval.to_mesh()


def mesh_payload(mesh: Any) -> tuple[dict[str, Any], bytes]:
    mesh.calc_loop_triangles()
    positions: list[float] = []
    normals: list[float] = []
    uvs: list[float] = []
    active_uv = mesh.uv_layers.active.data if mesh.uv_layers.active else None
    corner_normals = getattr(mesh, "corner_normals", None)
    groups: list[dict[str, int]] = []
    run_material: int | None = None
    run_start = 0
    vertex_count = 0

    for triangle in mesh.loop_triangles:
        material_index = max(0, int(triangle.material_index))
        if run_material is None:
            run_material = material_index
        elif material_index != run_material:
            groups.append({"start": run_start, "count": vertex_count - run_start, "materialIndex": run_material})
            run_start = vertex_count
            run_material = material_index

        for loop_index, vertex_index in zip(triangle.loops, triangle.vertices):
            co = mesh.vertices[vertex_index].co
            positions.extend((float(co.x), float(co.y), float(co.z)))
            if corner_normals and loop_index < len(corner_normals):
                normal = corner_normals[loop_index].vector
            else:
                normal = mesh.loops[loop_index].normal
            normals.extend((float(normal.x), float(normal.y), float(normal.z)))
            if active_uv:
                uv = active_uv[loop_index].uv
                uvs.extend((float(uv.x), float(uv.y)))
            vertex_count += 1

    if run_material is not None:
        groups.append({"start": run_start, "count": vertex_count - run_start, "materialIndex": run_material})

    # Geometry stores triangle corners directly, so changing topology and
    # split normals remain faithfully representable without a skinning solver.
    parts = [f32_bytes(positions), f32_bytes(normals)]
    if active_uv:
        parts.append(f32_bytes(uvs))
    else:
        parts.append(b"")
    position_bytes, normal_bytes, uv_bytes = parts
    material_names = [material.name if material else "" for material in mesh.materials]
    metadata = {
        "vertexCount": vertex_count,
        "positionLength": len(position_bytes),
        "normalLength": len(normal_bytes),
        "uvLength": len(uv_bytes),
        "groups": groups,
        "materials": material_names,
    }
    return metadata, b"".join(parts)


def bake_rigid_body_cache(scene: Any, frame_start: int, frame_end: int, skip: bool) -> None:
    world = scene.rigidbody_world
    cache = world.point_cache if world else None
    if cache is None or cache.is_baked:
        return
    if skip:
        print("Rigid-body world is not baked; --no-physics-bake leaves its motion unevaluated.")
        return

    cache.frame_start = frame_start
    cache.frame_end = frame_end
    scene.frame_set(frame_start)
    result = bpy.ops.ptcache.bake_all(bake=True)
    if "FINISHED" not in result or not cache.is_baked:
        raise RuntimeError(f"Could not bake rigid-body world cache: {result}")
    print(f"Baked rigid-body world cache for frames {frame_start}–{frame_end}.")


def main() -> None:
    args = parse_args()
    if args.step < 1:
        raise SystemExit("--step must be 1 or greater")
    if not bpy.data.filepath:
        raise SystemExit("Save the Blender file before exporting a browser cache")

    scene = bpy.context.scene
    frame_start = args.start if args.start is not None else scene.frame_start
    frame_end = args.end if args.end is not None else scene.frame_end
    if frame_end < frame_start:
        raise SystemExit("--end must be greater than or equal to --start")
    sample_frames = list(range(frame_start, frame_end + 1, args.step))
    if sample_frames[-1] != frame_end:
        sample_frames.append(frame_end)

    output = os.path.abspath(args.output or (bpy.data.filepath + ".bva.gz"))
    os.makedirs(os.path.dirname(output), exist_ok=True)
    geometry_blob = bytearray()
    geometry_table: dict[str, dict[str, Any]] = {}
    geometry_ids: dict[str, str] = {}
    object_frames: dict[str, list[dict[str, Any]]] = {}
    object_materials: dict[str, list[str]] = {}
    original_frame = scene.frame_current
    bake_rigid_body_cache(scene, frame_start, frame_end, args.no_physics_bake)

    try:
        for frame in sample_frames:
            scene.frame_set(frame)
            bpy.context.view_layer.update()
            depsgraph = bpy.context.evaluated_depsgraph_get()
            for obj in scene.objects:
                if obj.type not in GEOMETRY_TYPES or obj.hide_render:
                    continue
                obj_eval = obj.evaluated_get(depsgraph)
                mesh = evaluated_mesh(obj_eval, depsgraph)
                if mesh is None:
                    continue
                try:
                    geometry, encoded = mesh_payload(mesh)
                finally:
                    obj_eval.to_mesh_clear()
                if not geometry["vertexCount"]:
                    continue

                digest_input = json.dumps(
                    {
                        "vertexCount": geometry["vertexCount"],
                        "positionLength": geometry["positionLength"],
                        "normalLength": geometry["normalLength"],
                        "uvLength": geometry["uvLength"],
                        "groups": geometry["groups"],
                    },
                    separators=(",", ":"),
                ).encode() + encoded
                digest = hashlib.sha256(digest_input).hexdigest()[:24]
                geometry_id = geometry_ids.get(digest)
                if geometry_id is None:
                    geometry_id = f"g{len(geometry_ids):06d}"
                    geometry_ids[digest] = geometry_id
                    offset = len(geometry_blob)
                    geometry.update({"positionOffset": offset, "normalOffset": offset + geometry["positionLength"]})
                    uv_offset = offset + geometry["positionLength"] + geometry["normalLength"]
                    geometry["uvOffset"] = uv_offset if geometry["uvLength"] else None
                    geometry_blob.extend(encoded)
                    geometry_table[geometry_id] = geometry

                object_materials.setdefault(obj.name, geometry["materials"])
                object_frames.setdefault(obj.name, []).append({
                    "frame": frame,
                    "matrix": matrix_column_major(obj_eval.matrix_world),
                    "geometry": geometry_id,
                })

    finally:
        scene.frame_set(original_frame)
        bpy.context.view_layer.update()

    objects = [
        {"name": name, "materials": object_materials[name], "frames": frames}
        for name, frames in sorted(object_frames.items())
    ]
    if not objects:
        raise SystemExit("No visible mesh, curve, surface, text, or metaball geometry was found")

    manifest = {
        "format": "blender-viewer-evaluated-animation",
        "version": 1,
        "scene": scene.name,
        "frameStart": frame_start,
        "frameEnd": frame_end,
        "frameStep": args.step,
        "frameCurrent": scene.frame_current,
        "fps": scene.render.fps / scene.render.fps_base,
        "objects": objects,
        "geometries": geometry_table,
    }
    manifest_bytes = json.dumps(manifest, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    padding = (4 - ((8 + len(manifest_bytes)) % 4)) % 4
    container = MAGIC + struct.pack("<I", len(manifest_bytes)) + manifest_bytes + (b"\0" * padding) + geometry_blob
    with open(output, "wb") as stream:
        stream.write(gzip.compress(container, compresslevel=9, mtime=0))

    print(f"Wrote {output}")
    print(f"{len(objects)} geometry objects · {len(sample_frames)} samples · {len(geometry_table)} unique evaluated meshes")
    print("Non-rigid-body physics caches must be baked in Blender before export for deterministic results.")


if __name__ == "__main__":
    main()
