from setuptools import setup, find_packages


setup(
    name="sogol",
    version="0.1",
    packages=find_packages(),
    scripts=['sogolife.py'],
    author="moyiz",
    author_email="",
    description="Sound of game of life.",
    license="BSD",
    keywords="gol sol game of life sound of life",
    install_requires=['pyglet'],
    url=""
)
