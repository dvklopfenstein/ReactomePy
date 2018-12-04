#!/usr/bin/env python
"""In which pathways does CCR5 (UniProt:P51681) participate?

From Figure 4b in:
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
    """In which pathways does CCR5 (UniProt:P51681) participate?"""

    fout_txt = 'fig4b_pathways_containing_CCR5.txt'

    qry = ('MATCH (p:Pathway)-[:hasEvent*]->(rle:ReactionLikeEvent), '
           '(rle)-[:input|output|catalystActivity|entityFunctionalStatus|physicalEntity|'
           'regulatedBy|regulator|hasComponent|hasMember|hasCandidate|repeatedUnit*]->(pe:PhysicalEntity), '
           '(pe)-[:referenceEntity]->(re:ReferenceEntity{identifier:"P51681"}), '
           '(re)-[:referenceDatabase]->(rd:ReferenceDatabase{displayName:"UniProt"}) '
           'RETURN DISTINCT p.stId AS Identifier, p.displayName AS Pathway')

    data = _get_data(qry, password)
    with open(fout_txt, 'w') as prt:
        _prt_data(data, prt)
        print('  WROTE: {TXT}'.format(TXT=fout_txt))


def _prt_data(data, prt):
    """Print the Participating molecules for a pathway."""
    msg = '{N} participants in Pathway(R-HSA-983169)'.format(N=len(data))
    prt.write("{MSG}\n\n".format(MSG=msg))
    prt.write('Identifier      Pathway\n')
    prt.write('--------------- --------\n')
    for dct in sorted(data, key=lambda d: [d['Pathway'], d['Identifier']]):
        prt.write('{Identifier:15} {Pathway}\n'.format(**dct))
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
