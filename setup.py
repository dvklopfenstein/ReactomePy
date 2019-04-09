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
    'reactomepy',
    'reactomepy/code',
    'reactomepy/code/cli',
    'reactomepy/code/enrich',
    'reactomepy/code/ex',
    'reactomepy/code/node',
    'reactomepy/code/query',
    'reactomepy/code/rest',
    'reactomepy/code/run',
    'reactomepy/code/schema',
    'reactomepy/code/subdag',
    'reactomepy/code/wrpy',
    'reactomepy/data',
    'reactomepy/data/all',
    'reactomepy/data/pwy',
    'reactomepy/work',
]

setup(
    name='reactomepy',
    version='0.68.0004',
    author='DV Klopfenstein',
    author_email='dvklopfenstein@gmail.com',
    long_description=get_long_description(),
    packages=PACKAGES,
    package_dir={p:'src/{PKG}'.format(PKG=p) for p in PACKAGES},
    # include_package_data=True,
    # package_data={"reactomepy.test_data.nbt_3102": ["*.*"]},
    scripts=glob('src/bin/*.py') + glob('src/bin_neo4j/tutorial/*.py') + glob('src/bin_neo4j/wrpy/*.py'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: OS Independent',
    ],
    url='http://github.com/dvklopfenstein/ReactomePy',
    description='Explore biomolecular pathways in Reactome from the command line',
    install_requires=['enrichmentanalysis_dvklopfenstein'],
)

# We use the Neo4j Python driver is officially supported by Neo4j, called neo4j.
# https://neo4j.com/developer/python/
# https://github.com/neo4j/neo4j-python-driver

# These install the same package:
#    * pip install neo4j
#    * conda install neo4j-python-driver
