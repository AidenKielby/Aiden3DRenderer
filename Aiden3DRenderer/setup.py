from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aiden3drenderer",
    version="1.3.2",
    author="Aiden",
    author_email="headstone.yt@gmail.com",
    description="A lightweight 3D wireframe renderer built from scratch using Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AidenKielby/3D-mesh-Renderer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pygame>=2.6.0",
        "pywavefront>=1.3.3",
        "numpy>=2.4.2",
        "opencv-python>=4.13.0.90"
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