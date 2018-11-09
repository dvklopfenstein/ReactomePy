#!/usr/bin/env python
"""Breaking down complexes and sets to get thier participants."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#complexes-sets-participants

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase


# MATCH (Complex{stId:"R-HSA-983126"})-[:hasComponent]->(pe:PhysicalEntity) RETURN pe.stId AS component_stId, pe.displayName AS component
def main(password):
    """Breaking down complexes and sets to get thier participants."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        #     component_stId   component
        #     --------------   ----------
        #     'R-HSA-976075    E3 ligases in proteasomal degradation [cytosol]
        #     'R-ALL-983035    antigenic substrate [cytosol]
        #     'R-HSA-976165    Ubiquitin:E2 conjugating enzymes [cytosol]
        qry = ('MATCH (Complex{stId:"R-HSA-983126"})-[:hasComponent]->(pe:PhysicalEntity) RETURN '
               'pe.stId AS component_stId, pe.displayName AS component')
        for dct in session.run(qry).data():
            print('{component_stId} {component}'.format(**dct))

        qry = ('MATCH (Complex{stId:"R-HSA-983126"})'
               '-[:hasComponent|hasMember|hasCandidate*]->(pe:PhysicalEntity) RETURN '
               'pe.stId AS component_stId, pe.displayName AS component')
        fout_txt = 'complex_components_all.txt'
        with open(fout_txt, 'w') as prt:
            for idx, dct in enumerate(session.run(qry).data()):
                prt.write('{component_stId} {component}\n'.format(**dct))
            print('  {N} compents WROTE: {TXT}'.format(N=idx, TXT=fout_txt))

if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
