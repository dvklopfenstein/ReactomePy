"""Write pathway2proteins into a Python module."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import collections as cx
import timeit
from reactomepy.code.utils import get_hms
from reactomepy.code.wrpy.utils import REPO
from reactomepy.code.wrpy.utils import prt_docstr_module
from reactomepy.code.wrpy.utils import prt_copyright_comment

TIC = timeit.default_timer()

# pylint: disable=line-too-long
class PathwayMolecules(object):
    """Extract and print participating molecules for a pathway."""

    def __init__(self, gdbdr):
        self.gdbdr = gdbdr

    @staticmethod
    def get_query(database):
        """Return all paticipating molecules for all pathways."""
        return "".join([
            'MATCH (p:Pathway)-[:hasEvent*]->(rle:ReactionLikeEvent),',
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

    def get_pw2molecules(self, database='UniProt'):
        """Get the Participating molecules for a pathway."""
        pwid2molecules = cx.defaultdict(set)
        with self.gdbdr.session() as session:
            query = self.get_query(database)
            # print("QUERY: {Q}".format(Q=query))
            for rec in session.run(query).records():
                # print(rec)
                pwid2molecules[rec['pwid']].add(rec['mol_id'])
        return pwid2molecules

    def wrpy_pw2molecules(self, fout_py, database='UniProt'):
        """Print the Participating molecules for a pathway."""
        pw2molecules = self.get_pw2molecules(database)
        molecules = set(m for ms in pw2molecules.values() for m in ms)
        hms = get_hms(TIC)
        msg = '{HMS} {N:4} Pathways contain {M:5} items from {DB}'.format(
            HMS=hms, N=len(pw2molecules), M=len(molecules), DB=database)
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt_docstr_module(msg, prt)
            prt.write('# pylint: disable=line-too-long, too-many-lines\n')
            prt.write('PWY2{ITEM}S = {{\n'.format(ITEM=database.upper()))
            for pwy, molecules in sorted(pw2molecules.items(), key=lambda t: int(t[0].split('-')[2])):
                prt.write("    '{PWY}':".format(PWY=pwy))
                mstrs = ["'{V}'".format(V=m) for m in sorted(molecules)]
                prt.write("{{{SET}}},\n".format(SET=", ".join(mstrs)))
            # prt_namedtuple(self.dcts, 'SPECIES', fields, prt)
            prt.write('}\n')
            prt_copyright_comment(prt)
        filesize = int(os.stat(os.path.join(REPO, fout_py)).st_size/1000000.0)
        print("  {HMS} {MB} Mbytes {MSG} WROTE: {PY}".format(HMS=hms, MB=filesize, MSG=msg, PY=fout_py))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
