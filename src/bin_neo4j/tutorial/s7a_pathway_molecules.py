#!/usr/bin/env python
"""Joining the pieces: Participating molecules for a pathway."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#joining-pieces

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

# pylint: disable=line-too-long
def main(password):
    """Joining the pieces: Participating molecules for a pathway."""
    fout_txt = 'pathway_molecules_R-HSA-983169.txt'

    # ALL paticipating molecules for pathway R-HSA-983169
    qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent*]->(rle:ReactionLikeEvent),'
           '(rle)-[:'
           'input|output|catalystActivity|regulatedBy|'
           'physicalEntity|regulator|hasComponent|hasMember|hasCandidate*'
           ']->(pe:PhysicalEntity),'
           '(pe)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]->(rd:ReferenceDatabase)'
           'RETURN DISTINCT re.identifier AS Identifier, rd.displayName AS Database')

    data = _get_data(qry, password)
    with open(fout_txt, 'w') as prt:
        _prt_data(data, prt)
        print('  WROTE: {TXT}'.format(TXT=fout_txt))


def _prt_data(data, prt):
    """Print the Participating molecules for a pathway."""
    msg = '{N} participants in Pathway(R-HSA-983169)'.format(N=len(data))
    prt.write("{MSG}\n\n".format(MSG=msg))
    prt.write('Identifier Database\n')
    prt.write('---------- --------\n')
    for dct in sorted(data, key=lambda d: [d['Database'], d['Identifier']]):
        prt.write('{Identifier:10} {Database}\n'.format(**dct))
    print(msg)

def _get_data(qry, password):
    """Get the Participating molecules for a pathway."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        return session.run(qry).data()


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
