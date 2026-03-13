from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aiden3drenderer",
    version="1.5.3",
    author="Aiden",
    author_email="headstone.yt@gmail.com",
    description="A lightweight 3D wireframe renderer built from scratch using Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AidenKielby/3D-mesh-Renderer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords=[
        "3d", "renderer", "wireframe", "pygame", "mesh",
        "3d-rendering", "procedural", "terrain", "physics",
        "opengl", "rasterizer", "projection", "camera",
        "computer-graphics", "3d-engine"
    ],
    python_requires=">=3.9",
    install_requires=[
        "pygame>=2.6.0",
        "numpy>=2.4.2",
        "opencv-python>=4.13.0.90",
        "moderngl>=5.12.0",
        "pillow>=12.1.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "black", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "aiden3d-demo=aiden3drenderer.renderer:main",
        ],
    },
    include_package_data=True,

)