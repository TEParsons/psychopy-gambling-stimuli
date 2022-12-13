#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

# Define the name for your package, this will be used when calling `loadPlugin`.
# Note, for packages containing only a single module defining objects to export,
# you should name it something based off this name of the project to avoid
# import collisions with other packages.
name = "psychopy-gambling-stimuli"

# Version for the package. Use setuptools conventions for specifying the version
# string.
version = "0.1"

# Define packages to be included with this plugin.
packages = [
    'psychopy-gambling-stimuli'
]

# Define package directories.
package_dir = {
    'psychopy-gambling-stimuli': "psychopy_gambling_stimuli",
}

# Define package data. This is required for including icons or any other
# non-Python resource (e.g. documentation, images, videos, etc.) needed by the
# plugin.
package_data = {
   "": ["*.txt", "*.md", "*.png"]
}

# Define entry points. PsychoPy's plugin framework scans packages and looks for
# entry points advertised in the package metadata which pertains to PsychoPy.
# Entry points are a dictionary, where keys are fully qualified names to
# modules and unbound classes which you want to add/modify attributes. Values
# can be single strings, or lists of strings specifying what attributes of those
# PsychoPy objects are to reference objects defined in the plugin module.
entry_points = {
    'psychopy.visual.CoinFlipStim': [
        'CoinFlipStim = psychopy_gambling_stimuli.psychopy_coin_flip.visual.coinflip.coinflip:CoinFlipStim'
    ],
    'psychopy.experiment.components.coinflip': [
        'coinflip = psychopy_gambling_stimuli.psychopy_coin_flip.experiment.components.coinflip'
    ],
}

# Run the setup function.
setup(
    name=name,  # set the name
    version=version,  # put your plugin version here
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    author="Todd Parsons",
    author_email="todd@opensciencetools.org",
    description="Adds some handy components with pre-packaged stimuli useful for gambling tasks.",
    url="https://github.com/TEParsons/psychopy-gambling-stimuli",
    classifiers=[
        "License :: OSI Approved :: GPL3",
        'Programming Language :: Python :: 3'],
    keywords="psychopy assets gambling",
    zip_safe=False,
    entry_points=entry_points  # set our entry points in the package metadata
)
