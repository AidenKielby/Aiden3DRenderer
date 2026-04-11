# Contributing to Aiden3DRenderer

First off, thank you for considering contributing to Aiden3DRenderer! 
This project was built to make 3D graphics, projection math, and shaders more accessible and less "mystical" for Python developers. Whether you are fixing a typo, adding a new mathematical shape, or improving the GPU pipeline, your help is genuinely appreciated.

## Code of Conduct
This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### 1. Reporting Bugs
If you find a bug, please check the [Issues](https://github.com/AidenKielby/3D-mesh-Renderer/issues) tab to see if it has already been reported. If not, open a new issue and include:
* Your operating system and Python version.
* A clear description of the problem.
* Steps to reproduce the issue, or a small code snippet showing the bug.

### 2. Suggesting Enhancements
Have an idea for a new built-in shape, a cool shader, or a feature for the physics engine? 
* Open an issue describing your idea.
* Explain how it would benefit the project and its educational goals.
* If you want to build it yourself, let us know in the issue so we can assign it to you!

### 3. Adding New Shapes or Shaders
This is a great place for beginners to contribute! 
* **Shapes:** Look at how existing shapes are defined using the `@register_shape` decorator. You can add new procedural shapes to expand the gallery.
* **Shaders:** If you have a cool GLSL compute shader, you can add it to our examples or documentation.

## Setting Up Your Development Environment

To start making changes, you'll need to set up the project locally.

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/3D-mesh-Renderer.git](https://github.com/YOUR_USERNAME/3D-mesh-Renderer.git)
   cd 3D-mesh-Renderer/Aiden3DRenderer
