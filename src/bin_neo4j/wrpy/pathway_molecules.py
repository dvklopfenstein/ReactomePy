#!/usr/bin/env python
"""Write pathway2proteins into a Python module."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomeneo4j.code.wrpy.pathway_molecules import PathwayMolecules


# pylint: disable=line-too-long
def main(password, schemaname='Complex', stid='R-HSA-983126', prt=sys.stdout):
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
    obj = PathwayMolecules(password)
    for org in species:
        obj.wrpy_pw2molecules(org, 'UniProt')


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
