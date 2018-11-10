#!/usr/bin/env python
"""Retrieving a protein based on its identifier."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#retrieving-objects

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase


def main(password):
    """Retrieving a protein based on its identifier."""
    # EntityWithAccessionedSequence (EWAS) which corresponds to a protein in Reactome.
    # For this example we use one form of PTEN in the cytosol with identifier R-HSA-199420
    qry = 'MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}) RETURN ewas'

    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    print(qry)
    with gdbdr.session() as session:
        for rec in session.run(qry).records():
            for key, val in rec['ewas'].items():
                print("    {KEY:15} {VAL}".format(KEY=key, VAL=val))


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
