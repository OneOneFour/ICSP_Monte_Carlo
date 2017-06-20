#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError as err:
    from distutils.core import setup
import os

def find_version():
    for line in open(os.path.join('sgc', '__init__.py')):
        if line.startswith('__version__'):
            return line.split('=')[1].strip().strip('"').strip("'")
    raise RuntimeError("Unable to find __version__ declaration")
version = find_version()

if __name__ == "__main__":
    setup (
        name = "SimpleGC",
        version = version,
        description = "GUI Library for Pygame",
        author = "Sam Bull",
        options = {
            'sdist': {
                'formats': ['gztar','zip'],
            },
        },
        url = "https://launchpad.net/simplegc",
        license = "BSD",
        packages = ['sgc','sgc.widgets', 'sgc.widgets.composite', 'sgc.widgets._interface'],
        package_dir = {
            'sgc': 'sgc',
            'sgc.widgets': os.path.join('sgc', 'widgets'),
            'sgc.widgets.composite': os.path.join('sgc', 'widgets', 'composite'),
            'sgc.widgets._interface': os.path.join('sgc', 'widgets', '_interface')
        },
    )
