#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://reactome.org/dev/graph-database/extract-participating-molecules

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase


def main(password, abc='hsa'):
    """Mirror Reactome/Neo4j tutorial in Python."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        _run(session)


def _run(session):
    """2) BREAKING DOWN COMPLEXES AND SETS TO GET THEIR PARTICIPANTS"""
    # https://reactome.org/content/schema/Complex
    # MATCH (Complex{stId:"R-HSA-983126"})-[:hasComponent]->(pe:PhysicalEntity) RETURN pe.stId AS component_stId, pe.displayName AS component
    qry = ('MATCH (Complex{stId:"R-HSA-983126"})-'
           '[:hasComponent]->(pe:PhysicalEntity) RETURN '
           'pe.stId AS component_stId, '
           'pe.displayName AS component')
    
    #     component_stId   component
    #     --------------   ----------
    #     'R-HSA-976075    E3 ligases in proteasomal degradation [cytosol]
    #     'R-ALL-983035    antigenic substrate [cytosol]
    #     'R-HSA-976165    Ubiquitin:E2 conjugating enzymes [cytosol]
    for dct in session.run(qry).data():
        print('{ID} {NAME}'.format(ID=dct['component_stId'], NAME=dct['component']))



if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
