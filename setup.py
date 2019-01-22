#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Setup for PyPI usage."""

import os.path as op

from glob import glob
from setuptools import setup
from setup_helper import SetupHelper


NAME = "reactomeneo4j"
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]

# Use the helper
HLPR = SetupHelper(initfile="reactomeneo4j/__init__.py", readmefile="README.md")

SETUP_DIR = op.abspath(op.dirname(__file__))

setup(
    name=NAME,
    version=0.1,
    author='DV Klopfenstein',
    author_email='dvklopfenstein@gmail.com',
    license=HLPR.license,
    long_description=('Explore peer-reviewed biological pathways '
                      'in Reactome using Python to run neo4j queries'),
    packages=[
        NAME,
        NAME + ".code",
        NAME + ".code.node",
        NAME + ".code.node.query",
        NAME + ".code.schema",
        NAME + ".data",
        NAME + ".work"],
    include_package_data=True,
    # package_data={"reactomeneo4j.test_data.nbt_3102": ["*.*"]},
    scripts=glob('scripts/*.py'),
    classifiers=CLASSIFIERS,
    url='http://github.com/dvklopfenstein/reactome_neo4j_py',
    description='Explore biological pathways in Reactome from the command-line',
    install_requires=['timeit', 'datetime', 'collections'],
)
