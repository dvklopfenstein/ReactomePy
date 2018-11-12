"""Write pathway2proteins into a Python module."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import collections as cx
from neo4j import GraphDatabase
from reactomeneo4j.data.species import SPECIES
from reactomeneo4j.code.wrpy.utils import REPO
from reactomeneo4j.code.wrpy.utils import prt_docstr_module
from reactomeneo4j.code.wrpy.utils import prt_namedtuple
from reactomeneo4j.code.wrpy.utils import prt_dict
from reactomeneo4j.code.wrpy.utils import prt_copyright_comment


# pylint: disable=line-too-long
class PathwayMolecules(object):
    """Extract and print participating molecules for a pathway."""

    def __init__(self, password):
        self.gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
        self.name2ntabc = {nt.displayName:nt for nt in SPECIES}

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
                # print(rec)
                pwid2molecules[rec['pwid']].add(rec['mol_id'])
        return pwid2molecules

    def wrpy_pw2molecules(self, species='Homo sapiens', database='UniProt'):
        """Print the Participating molecules for a pathway."""
        fout_py = "src/reactomeneo4j/data/{ABC}/pathways/pwy2{DB}.py".format(
            ABC=self.name2ntabc[species].abc, DB=database.lower())
        pw2molecules = self.get_pw2molecules(species, database)
        molecules = set(m for ms in pw2molecules.values() for m in ms)
        msg = '{N:4} Pathways contain {M:5} items from {DB} for {ORG:23}'.format(
            N=len(pw2molecules), M=len(molecules), DB=database, ORG=species)
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt_docstr_module(msg, prt)
            prt.write('PWY2ITEMS = {\n')
            for pwy, molecules in sorted(pw2molecules.items(), key=lambda t: int(t[0].split('-')[2])):
                prt.write("    '{PWY}':".format(PWY=pwy))
                mstrs = ["'{V}'".format(V=m) for m in sorted(molecules)]
                prt.write("{{{SET}}},\n".format(SET=", ".join(mstrs)))
            # prt_namedtuple(self.dcts, 'SPECIES', fields, prt)
            prt.write('}\n')
            prt_copyright_comment(prt)
        print("  {MSG} WROTE: {PY}".format(MSG=msg, PY=fout_py))

    def wrpy_info(self, fout_py):
        """Print Reactome species main information."""
        fields = ['abc', 'abbreviation', 'taxId', 'displayName']
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt_docstr_module('Species in Reactome', prt)
            prt_namedtuple(self.dcts, 'SPECIES', fields, prt)
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
