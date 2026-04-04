# Demo Module

This page documents the packaged demo entrypoints in aiden3drenderer.Demo.silly_skull.

## Why this module exists

The Demo module is the distribution-facing showcase for the renderer stack. It is wired to console entrypoints in setup.py so users can run an installed demo without writing code.

## Entry points (from packaging)

- aiden3d-demo -> aiden3drenderer.Demo.silly_skull:demo
- inverted-aiden3d-demo -> aiden3drenderer.Demo.silly_skull:demo_inv
- aiden3d-mac -> aiden3drenderer.Demo.silly_skull:demo_mac

## Public functions

### demo()

Signature:

    demo() -> None

Behavior:

- Creates Renderer3D with a 600x600 window.
- Enables RASTERIZE mode and object-format rendering.
- Loads demo assets from package resources (skull.obj, skull.png, damage_image.png).
- Creates an Entity with a follow-camera script.
- Adds a compute-shader post pass that blends in a damage texture based on distance.
- Starts renderer.run().

### demo_inv()

Signature:

    demo_inv() -> None

Behavior:

- Same base setup as demo().
- Adds distance damage pass and an additional invert-colors post pass.
- Starts renderer.run().

### demo_mac()

Signature:

    demo_mac() -> None

Behavior:

- Creates Renderer3D in MESH mode (non-compute path).
- Loads skull assets from package resources.
- Adds follow-camera entity and starts renderer.run().

## Data and dependency flow

- Asset access uses importlib.resources.files plus as_file to stay compatible with installed wheels.
- Shader passes are created through CustomShader and registered in renderer.shaders.
- Scripted behavior is injected through Entity.add_script and executed via exec at runtime.

## Failure states and current drift

Current source contains a loader-contract mismatch in demo functions:

- demo code calls obj_loader.get_obj(path, renderer.add_texture_for_raster(...), scale=4).
- obj_loader.get_obj currently expects a Material object in argument 2.
- add_texture_for_raster returns a numeric texture layer index (or None on macOS compute-disabled path).
- Later, renderer.add_entity calls add_material on entity.model[5], which expects a Material-like object with texture_path.

Practical result:

- demo() and demo_inv() can fail when add_entity attempts material registration.
- demo_mac() can also fail for the same reason (and may pass None as material argument).

Until source is updated, treat these as legacy demos illustrating intended architecture rather than guaranteed runnable examples.

## Performance notes

- In demo() and demo_inv(), rendering cost is dominated by rasterization and post-process shader passes.
- Additional shader stages in renderer.shaders add one dispatch per pass, so cost scales with raster target pixel count.
- Lowering rasterization size through renderer.set_rasterization_downsize(...) is the primary runtime tuning control.

## Real-world usage

Run the packaged demo from an installed environment:

```bash
aiden3d-demo
```

Run the inverted-color variant:

```bash
inverted-aiden3d-demo
```

Run the macOS mesh fallback variant:

```bash
aiden3d-mac
```

See also: [Renderer](renderer.md), [Entities](entities.md), [Custom Shaders](custom_shaders.md), [Audit Report](audit_report.md).
