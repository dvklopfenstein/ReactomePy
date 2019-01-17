#!/usr/bin/env python
"""Write pathway2proteins into a Python module.

Usage: pathway_molecules.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""
from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from neo4j import GraphDatabase
from reactomeneo4j.code.wrpy.pathway_molecules import PathwayMolecules
from reactomeneo4j.code.utils import get_args


# pylint: disable=line-too-long
def main():
    """Save the participating molecules for a pathway into a Python module."""

    # 2049 Pathways contain 10912 items from UniProt for Homo sapiens
    # 1623 Pathways contain 12207 items from UniProt for Mus musculus
    # 1374 Pathways contain  9316 items from UniProt for Drosophila melanogaster
    #     ->
    # src/reactomeneo4j/data/hsa/pathways/pwy2uniprot.py
    # src/reactomeneo4j/data/dme/pathways/pwy2uniprot.py
    # src/reactomeneo4j/data/mmu/pathways/pwy2uniprot.py
    species = [
        'Homo sapiens',
        'Mus musculus',
        'Drosophila melanogaster',
    ]
    dct = get_args(__doc__, ['neo4j_password', 'neo4j_username', 'url'])
    gdbdr = GraphDatabase.driver(dct['url'], auth=(dct['neo4j_username'], dct['neo4j_password']))
    obj = PathwayMolecules(gdbdr)
    for org in species:
        obj.wrpy_pw2molecules(org, 'UniProt')


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
