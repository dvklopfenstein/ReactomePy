#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Setup for PyPI usage."""

import sys
from glob import glob
from setuptools import setup

def get_long_description():
    """Get the package's long description."""
    with open("README.md", "r") as ifstrm:
        return ifstrm.read()

def get_version():
    """Get the package's version from without using an import."""
    with open("src/reactomepy/__init__.py", "r") as ifstrm:
        for line in ifstrm:
            if line[:15] == "__version__ = '":
                return line.rstrip()[15:-1]

def get_install_requires():
    """Get requirements for installation."""
    # pip: User installs items in requirements.txt
    base = ['enrichmentanalysis_dvklopfenstein', 'requests']
    # conda: Anaconda installs all needed to run scripts
    if sys.argv[1:2] == ['bdist_conda']:
        pkgs = [
            'neobolt',
            'neo4j-python-driver',
        ]
        base.extend(pkgs)
    return base

def get_distclass():
    """If building for anaconda, get CondaDistribution class."""
    if sys.argv[1:2] != ['bdist_conda']:
        return None
    from distutils.command.bdist_conda import CondaDistribution
    return CondaDistribution

PACKAGES = [
    'reactomepy',
    'reactomepy.code',
    'reactomepy.code.cli',
    'reactomepy.code.enrich',
    'reactomepy.code.ex',
    'reactomepy.code.node',
    'reactomepy.code.query',
    'reactomepy.code.rest',
    'reactomepy.code.run',
    'reactomepy.code.schema',
    'reactomepy.code.subdag',
    'reactomepy.code.wrpy',
    'reactomepy.data',
    'reactomepy.data.all',
    'reactomepy.data.pwy',
    'reactomepy.work',
]

setup(
    name='reactomepy',
    version=get_version(),
    author='DV Klopfenstein',
    author_email='dvklopfenstein@gmail.com',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=PACKAGES,
    package_dir={p:'src/{PKG}'.format(PKG=p).replace('.', '/') for p in PACKAGES},
    # include_package_data=True,
    # package_data={"reactomepy.test_data.nbt_3102": ["*.*"]},
    scripts=glob('src/bin/*.py') + glob('src/bin_neo4j/tutorial/*.py'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: OS Independent',
    ],
    #distclass=get_distclass(),
    url='http://github.com/dvklopfenstein/ReactomePy',
    description='Explore biomolecular pathways in Reactome from the command line',
    install_requires=get_install_requires(),
)

# We use the Neo4j Python driver is officially supported by Neo4j, called neo4j.
# https://neo4j.com/developer/python/
# https://github.com/neo4j/neo4j-python-driver

# These install the same package (neo4j is not listed as a Python Anaconda Python package):
#    * pip install neo4j
#    * conda install neo4j-python-driver


