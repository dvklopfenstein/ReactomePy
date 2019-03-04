#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Setup for PyPI usage."""

from glob import glob
from setuptools import setup

def get_long_description():
    """Get the package's long description."""
    with open("README.md", "r") as fh:
        long_description = fh.read()

PACKAGES = [
    'reactomeneo4j',
    'reactomeneo4j/code',
    'reactomeneo4j/code/cli',
    'reactomeneo4j/code/enrich',
    'reactomeneo4j/code/ex',
    'reactomeneo4j/code/mkpy',
    'reactomeneo4j/code/node',
    'reactomeneo4j/code/query',
    'reactomeneo4j/code/rest',
    'reactomeneo4j/code/run',
    'reactomeneo4j/code/schema',
    'reactomeneo4j/code/subdag',
    'reactomeneo4j/code/wrpy',
    'reactomeneo4j/data',
    'reactomeneo4j/data/all',
    'reactomeneo4j/data/hsa',
    'reactomeneo4j/data/hsa/pathways',
    'reactomeneo4j/data/pwy',
    'reactomeneo4j/work',
]

setup(
    name='reactomeneo4j',
    version='0.0.1',
    author='DV Klopfenstein',
    author_email='dvklopfenstein@gmail.com',
    long_description=get_long_description(),
    packages=PACKAGES,
    package_dir={p:'src/{PKG}'format(PKG=p) for p in PACKAGES},
    # include_package_data=True,
    # package_data={"reactomeneo4j.test_data.nbt_3102": ["*.*"]},
    scripts=glob('src/bin/*.py'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: OS Independent',
    ],
    url='http://github.com/dvklopfenstein/reactome_neo4j_py',
    description='Explore biological pathways in Reactome from the command-line',
    install_requires=['timeit', 'datetime', 'collections'],
)
