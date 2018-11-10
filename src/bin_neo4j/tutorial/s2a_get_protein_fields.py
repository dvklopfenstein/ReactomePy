#!/usr/bin/env python
"""Identifiers for proteins or chemicals."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#identifiers-proteins-or-chemicals

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

def main(password):
    """Identifiers for proteins or chemicals."""
    # Retrieve only a couple of fields for the target node.
    # Follow the reference entity link in order to get the identifier:
    qry = ('MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}),'
           '(ewas)-[:referenceEntity]->(re:ReferenceEntity)'
           'RETURN ewas.displayName AS EWAS, re.identifier AS Identifier')
    # NOTE: The identifier is not directly stored in the node for the EWAS
    # but is a property of another node pointed from the EWAS which is a ReferenceEntity

    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        for rec in session.run(qry).records():
            print(rec.data())


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
