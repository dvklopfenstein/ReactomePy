#!/usr/bin/env python
"""Write pathway2proteins into a Python module.

Usage: pathway_molecules.py <neo4j_password> [--schemaClass=CLS] [--species=S] [-o] [-r]

Options:
  -h --help
  -c --schemaClass=CLS  Examples: Complex, Pathway, etc. [default: Complex]
  -s --species=S        Species [default: Homo sapiens]
  -o                    Write results into a file rather than to the screen
  -r                    Report lower-level source schema

"""
# https://reactome.org/dev/graph-database/extract-participating-molecules#joining-pieces

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
from docopt import docopt
from neo4j import GraphDatabase
from reactomeneo4j.code.wrpy.pathway_molecules import PathwayMolecules
from reactomeneo4j.data.species import SPECIES

# pylint: disable=line-too-long
def main(password, schemaname='Complex', stid='R-HSA-983126', prt=sys.stdout):
    """Save the participating molecules for a pathway into a Python module."""

    obj = PathwayMolecules(password)
    data = obj.get_pw2molecules('Homo sapiens', 'UniProt')
    #### # _prt_data(item_id, data, prt)
    #### with open(fout_txt, 'w') as prt:
    ####     _prt_data(data, prt)
    ####     print('  {N} WROTE: {TXT}'.format(N=len(data), TXT=fout_txt))


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
