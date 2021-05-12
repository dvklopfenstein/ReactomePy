#!/usr/bin/env python
"""Write pathway2proteins into a Python module.

Usage: pathway_molecules.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""
from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.wrpy.pathway_molecules import PathwayMolecules
from reactomepy.code.utils import get_gdbdr


# pylint: disable=line-too-long
def main():
    """Save the participating molecules for each pathway into a Python module."""
    fout_py = 'src/reactomepy/data/pwy/pwy2uniprot.py'
    obj = PathwayMolecules(get_gdbdr())
    obj.wrpy_pw2molecules(fout_py, 'UniProt')


if __name__ == '__main__':
    main()

# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
