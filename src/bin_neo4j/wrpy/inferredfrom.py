#!/usr/bin/env python
"""Save all species in Reactome to Python modules."""
# TBD: Not complete

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomeneo4j.code.wrpy.inferredfrom import InferredFrom
from neo4j import GraphDatabase


def prt_inferredfrom(password):
    """Print all species in Reactome."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    obj = InferredFrom(gdbdr)
    # obj.wrpy_info('src/reactomeneo4j/data/species.py')


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    prt_inferredfrom(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
