#!/usr/bin/env python
"""Which molecules participate in Interleukin-4 and 13 signaling (R-HSA-678-6785807?

From Figure 4a in:
    Reactome graph database: Efficient access to complex pathway data
    https://journals.plos.org/ploscompbiol/article?rev=2&id=10.1371/journal.pcbi.1005968
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

# pylint: disable=line-too-long
def main(password):
    """Which molecules participate in Interleukin-4 and 13 signaling (R-HSA-678-6785807?"""
    fout_txt = 'fig4a_pathway_molecules_IL_sig_R-HSA-6785807.txt'

    qry = ('MATCH (p:Pathway{stId:"R-HSA-6785807"})-[:hasEvent*]->(rle:ReactionLikeEvent), '
           '(rle)-[:input|output|catalystActivity|entityFunctionalStatus|physicalEntity|'
           'regulatedBy|regulator|hasComponent|hasMember|hasCandidate|repeatedUnit*]->(pe:PhysicalEntity), '
           '(pe)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]->(rd:ReferenceDatabase) '
           'RETURN DISTINCT re.identifier AS Identifier, rd.displayName AS Database')

    data = _get_data(qry, password)
    with open(fout_txt, 'w') as prt:
        _prt_data(data, prt)
        print('  WROTE: {TXT}'.format(TXT=fout_txt))


def _prt_data(data, prt):
    """Print the Participating molecules for a pathway."""
    msg = '{N} participants in Pathway(R-HSA-983169)'.format(N=len(data))
    prt.write("{MSG}\n\n".format(MSG=msg))
    prt.write('Identifier      Database\n')
    prt.write('--------------- --------\n')
    for dct in sorted(data, key=lambda d: [d['Database'], d['Identifier']]):
        prt.write('{Identifier:15} {Database}\n'.format(**dct))
    print(msg)

def _get_data(qry, password):
    """Get the Participating molecules for a pathway."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        return [rec.data() for rec in session.run(qry).records()]


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
