"""
Basic usage example for Aiden3DRenderer

This demonstrates the simplest way to use the renderer.
"""
from aiden3drenderer import Renderer3D


def main():
    # Create the renderer
    renderer = Renderer3D(width=1000, height=1000, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = "waves"
    
    # Run the renderer
    renderer.run()


if __name__ == "__main__":
    main()
