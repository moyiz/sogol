from setuptools import find_packages, setup

try:
    with open("README.md") as f:
        readme = f.read()
except FileNotFoundError:
    readme = ""


setup(
    name="sogol",
    version="0.2.0-alpha",
    packages=find_packages(exclude=("tests",)),
    author="moyiz",
    author_email="8603313+moyiz@users.noreply.github.com",
    description="Sound of Game of Life.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="gol sol game sound of life conway wave sine",
    install_requires=["docopt==0.6.2", "simpleaudio>=1.0.0"],
    url="https://github.com/moyiz/sogol",
    entry_points={"console_scripts": ["sogol=sogol:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research"
        "Programming Language :: Python :: 3 :: Only"
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
    ],
)
