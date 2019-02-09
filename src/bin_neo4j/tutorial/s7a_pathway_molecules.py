#!/usr/bin/env python
"""Joining the pieces: Participating molecules for a pathway."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#joining-pieces

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
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
        return [rec.data() for rec in session.run(qry).records()]


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])


# Tutorial 7a) Joining the pieces: Participating molecules for a pathway
What are all the molecules in the pathway, R-HSA-983169, _Class I MHC mediated antigen processing & presentation_?

[**Reactome Tutorial**: Joining the pieces: Participating molecules for a pathway](https://reactome.org/dev/graph-database/extract-participating-molecules#joining-pieces)

## Step 1) [Connect to Neo4j loaded with the Reactome Knowledgebase](https://github.com/dvklopfenstein/reactome_neo4j_py/blob/master/doc/md/README_gdbdr.md)

# Link to Reactome Knowledbase loaded into Neo4j
from neo4j import GraphDatabase

neo4j_url = 'bolt://localhost:7687'
neo4j_usr = 'neo4j'
neo4j_password = 'myneo4j_password'
neo4j_password = 'free2beme'

gdbdr = GraphDatabase.driver(neo4j_url, auth=(neo4j_usr, neo4j_password))

## Step 2) Pathway Molecules Query
### What are all the molecules in the pathway, R-HSA-983169, _Class I MHC mediated antigen processing & presentation_?

query = ('MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent*]->(rle:ReactionLikeEvent),'
         '(rle)-[:'
         'input|output|catalystActivity|regulatedBy|'
         'physicalEntity|regulator|hasComponent|hasMember|hasCandidate*'
         ']->(pe:PhysicalEntity),'
         '(pe)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]->(rd:ReferenceDatabase)'
         'RETURN DISTINCT '
         'pe.displayName AS Name, re.identifier AS Identifier, rd.displayName AS Database')

# Query and get the sub-pathways under R-HSA-983169
def _get_data():
    with gdbdr.session() as session:
        return [rec.data() for rec in session.run(query).records()]

data = _get_data()
# Print sub-pathways under R-HSA-983169
print('Database| ID     | Name')
print('--------|--------|------')
for data in sorted(data, key=lambda r:[r['Database'], r['Identifier']]):
    print("{Database:8}| {Identifier:6} | {Name}".format(**data))




# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
