#!/usr/bin/env python
"""Print all disease in Reactome."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomeneo4j.code.wrpy.disease import Diseases
from neo4j import GraphDatabase


def prt_disease(password):
    """Print all disease in Reactome."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    obj = Diseases(gdbdr)
    fout_disease_py = 'src/reactomeneo4j/data/disease_definitions.py'
    obj.wrpy_disease2fld(fout_disease_py, 'definition', 'DISEASE2DEFN')
    #fout_common_py = 'src/reactomeneo4j/data/disease_synonyms.py'
    # TBD Names and synonyms


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    prt_disease(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
