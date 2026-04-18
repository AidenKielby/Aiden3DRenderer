"""ShaderGraph package for aiden3drenderer.

Contains the ShaderGraph GUI and helper modules. Do not import
submodules here to avoid triggering optional dependencies at
package-import time.
"""

# Keep a minimal package marker; import submodules explicitly when needed.
__all__ = ["gui", "element", "elements", "shader_type"]
