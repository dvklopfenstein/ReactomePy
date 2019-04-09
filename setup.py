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
    name='reactomepy_dvklopfenstein',
    version='0.0.1',
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
    install_requires=['datetime', 'collections', 'enrichmentanalysis', 'neo4j'],
)
