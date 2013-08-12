#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = 'conceptnet5-client',
    version = '0.1',
    author = 'Hakki Caner Kirmizi',
    author_email = 'r00922148@csie.ntu.edu.tw',
    description = ('A Python programming interface and inference engine for ConceptNet5 Web API'),
    license = 'GPLv3',
    url = 'https://github.com/israkir/conceptnet5-client',
    packages = find_packages(),
    scripts = ['src/conceptnet5_client/bin/conceptnet-make.py'],
)
