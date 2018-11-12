"""Write pathway2proteins into a Python module."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
from neo4j import GraphDatabase
from reactomeneo4j.data.species import SPECIES

# pylint: disable=line-too-long
class PathwayMolecules(object):
    """Extract and print participating molecules for a pathway."""

    def __init__(self, password):
        self.gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
        self.name2ntabc = {nt.taxId:nt for nt in SPECIES}

    def get_query(self, species, database):
        """Return all paticipating molecules for all pathways in a species."""
        return "".join([
            'MATCH (p:Pathway{speciesName:"', '{SPECIES}'.format(SPECIES=species), '"})'
            '-[:hasEvent*]->(rle:ReactionLikeEvent),',
            '(rle)',
            '-[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator',
            '|hasComponent|hasMember|hasCandidate*]',
            '->(pe:PhysicalEntity),',
            '(pe)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]',
            '->(rd:ReferenceDatabase{displayName:"', '{DATABASE}'.format(DATABASE=database), '"})',
            'RETURN DISTINCT p.stId as pwid, re.identifier AS mol_id, rd.displayName AS mol_db'])

    # qry = 'MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent*]->(e)-[r]->(pe:PhysicalEntity) RETURN e, r, pe'

    #### qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent*]->(e),'
    ####        '(e)-[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator|hasComponent|hasMember|hasCandidate*]->(pe:PhysicalEntity),'
    ####        '(pe)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]->(rd:ReferenceDatabase)'
    ####        'RETURN DISTINCT re.identifier AS Identifier, rd.displayName AS Database')

    #### qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent*]->(e),'
    ####        '(e)-[*]->(pe:PhysicalEntity),'
    ####        '(pe)-[:referenceEntity]->(re:ReferenceEntity)-[:referenceDatabase]->(rd:ReferenceDatabase)'
    ####        'RETURN DISTINCT re.identifier AS Identifier, rd.displayName AS Database')

    #### data = _get_data(qry, password)
    #### # _prt_data(item_id, data, prt)
    #### with open(fout_txt, 'w') as prt:
    ####     _prt_data(data, prt)
    ####     print('  {N} WROTE: {TXT}'.format(N=len(data), TXT=fout_txt))

    def get_pw2molecules(self, species='Homo sapiens', database='UniProt'):
        """Get the Participating molecules for a pathway."""
        pwid2molecules = cx.defaultdict(set)
        with self.gdbdr.session() as session:
            query = self.get_query(species, database)
            # print("QUERY: {Q}".format(Q=query))
            for rec in session.run(query).records():
                print(rec)
                pwid2molecules[rec['pwid']].add(rec['mol_id'])
        return pwid2molecules

def _prt_data(data, prt):
    """Print the Participating molecules for a pathway."""
    msg = '{N} participants in Pathway(R-HSA-983169)'.format(N=len(data))
    prt.write("{MSG}\n".format(MSG=msg))
    prt.write('Identifier Database\n')
    prt.write('---------- --------\n')
    for dct in sorted(data, key=lambda d: [d['Database'], d['Identifier']]):
        prt.write('{Identifier:10} {Database}\n'.format(**dct))
    print(msg)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
