#!/usr/bin/env python
"""Identifiers for proteins or chemicals."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#identifiers-proteins-or-chemicals

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

# pylint: disable=line-too-long
def main(password):
    """Identifiers for proteins or chemicals."""
    # Retrieve the reference database in addition to fields found on the EWAS node.
    # The reference database is a node pointed from ReferenceEntity by an edge called referenceDatabase.
    # Follow the reference entity and database links to get the identifier and the database of reference:
    qry = ('MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}),'
           '(ewas)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]->(rd:ReferenceDatabase)'
           'RETURN ewas.displayName AS EWAS, re.identifier AS Identifier, rd.displayName AS Database')

    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        for dct in session.run(qry).data():
            for fld, val in dct.items():
                print('{FLD:10} {VAL}'.format(FLD=fld, VAL=val))


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
