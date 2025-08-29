"""
Setup script for Algorithm Visualizer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="algorithm-visualizer",
    version="1.0.0",
    author="Richard Blea",
    author_email="rblea97@gmail.com",
    description="Desktop application for visualizing sorting algorithms with smooth animations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rblea97/Algorithm-Visualizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses Python standard library only
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "algorithm-visualizer=main:main",
        ],
    },
    keywords="sorting algorithms visualization education python tkinter",
    project_urls={
        "Bug Reports": "https://github.com/Rblea97/Algorithm-Visualizer/issues",
        "Source": "https://github.com/Rblea97/Algorithm-Visualizer",
        "Documentation": "https://github.com/Rblea97/Algorithm-Visualizer#readme",
        "LinkedIn": "https://www.linkedin.com/in/richard-blea-748914159/",
    },
)
