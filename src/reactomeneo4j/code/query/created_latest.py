"""Get the first created and the lastest modified date and author."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
import sys
import timeit
# import datetime
import collections as cx
from reactomeneo4j.code.neo4jnode import Neo4jNode
from reactomeneo4j.code.utils import get_hms
# from reactomeneo4j.code.wrpy.utils import REPO
# from reactomeneo4j.code.wrpy.utils import prt_docstr_module
# from reactomeneo4j.code.wrpy.utils import prt_namedtuple
# from reactomeneo4j.code.wrpy.utils import prt_copyright_comment
# from reactomeneo4j.code.neo4jnodebasic import Neo4jNodeBasic
# from reactomeneo4j.code.query.functions import NodeHier
from reactomeneo4j.code.query.get_nodes import NodeGetter


# pylint: disable=line-too-long
class CreatedLatest():
    """Get the first created and the lastest modified date and author."""

    def __init__(self, gdbdr):
        self.tic = timeit.default_timer()
        self.gdbdr = gdbdr
        self.objng = NodeGetter(gdbdr)

    # def _get_fig2nt(self):
    #     """Create Figure data using associated: InstanceEdit Person."""
    #     _ng = self.objng
    #     fig2url = _ng.get_dbid2val('MATCH (f:Figure) RETURN f.dbId AS dbId, f.url AS val')
    #     fig2edits = _ng.get_dbid2set('MATCH (e:InstanceEdit)-[r]->(f:Figure) RETURN f.dbId AS dbId, e.dbId AS val')
    #     # Given InstanceEdit dbIds, get Persons who author
    #     editids = set(e for es in fig2edits.values() for e in es)
    #     edit2authors = self.get_edit2person(editids)
    #     # Given author Person dbIds, get author names
    #     figid2ntedit = self._get_editdates(edit2authors, auid2name)  # created/modified dateTime authors
    #     fig2ntdct = self._get_edits(figid2ntedit)
    #     # Combine Figure information from Figure, ->InstanceEdit, and [author]->(Person)
    #     fig2nt = {}
    #     ntobj = cx.namedtuple('NtFig', 'dbId url created last_modified author')
    #     for fid, url in fig2url.items():
    #         pass
    #     return fig2nt

    def get_auid2names(self, person_dbids):
        """Get the Person names, fiven Person dbIds."""
        qrypat = ('WITH [{IDs}] AS dbIds_Person MATCH (person:Person) WHERE person.dbId in dbIds_Person '
                  'RETURN person.dbId AS dbId, person.displayName AS val')
        query = qrypat.format(IDs=', '.join(sorted(set(str(au) for au in person_dbids))))
        return self.objng.get_dbid2val(query)  # auid2names

    def get_edit2person(self, edit_dbids, prt=sys.stdout):
        """Get the Person(s) who author for a set of InstanceEdit dbIds."""
        qrypat = ('WITH [{IDs}] AS dbIds_InstanceEdit '
                  'MATCH (person:Person)-[:author]->(instanceedit:InstanceEdit) '
                  'WHERE instanceedit.dbId IN dbIds_InstanceEdit '
                  'RETURN person.dbId AS val, instanceedit.dbId AS dbId')
        query = qrypat.format(IDs=', '.join(set(str(e) for e in edit_dbids)))
        return self.objng.get_dbid2set(query, prt)  # InstanceEdit.dbId->set(Person.dbId)

    def get_editdates(self, dststr, edit2auid, auid2name):
        """Get ALL edit dates for user-nodes."""
        qrypat = 'MATCH (e:InstanceEdit)-[r]->(dst:{DST}) RETURN e, type(r) AS rtyp, dst.dbId AS dbId'
        query = qrypat.format(DST=dststr)
        dbid2rel2ntedit = cx.defaultdict(lambda: cx.defaultdict(list))
        ntobj = cx.namedtuple('NtDateAu', 'year authors')
        exp_rels = {'created', 'modified'}
        with self.gdbdr.session() as session:
            for rec in session.run(query).records():
                dbid_edit = rec['e']['dbId']
                authors = frozenset(auid2name[auid] for auid in edit2auid[dbid_edit])
                rel = rec['rtyp']
                editnode = Neo4jNode(rec['e'])
                ntd = ntobj(year=editnode.ntp.dateTime.year, authors=authors)
                dbid2rel2ntedit[rec['dbId']][rel].append(ntd)
                assert rel in exp_rels, 'NEW FIGURE EDIT RELATIONSHIPS FOUND; UPDATE CODE'
        return dbid2rel2ntedit

    def get_edits(self, dbid2rel2ntedits):
        """Get the instance edit date, created and latest modified, for figures."""
        fig2dct = {}
        tic = timeit.default_timer()
        # Keep only first_created and last_modified, if present
        # min_chg = datetime.timedelta(days=15)
        for dbid, r2nt in dbid2rel2ntedits.items():
            fig2dct[dbid] = {}
            first_created = min(r2nt['created'], key=lambda nt: nt.year) if 'created' in r2nt else None
            last_modified = max(r2nt['modified'], key=lambda nt: nt.year) if 'modified' in r2nt else None
            if first_created:
                fig2dct[dbid]['created'] = first_created
            if last_modified:
                # Only store 'last_modified' if it is at least a year later than 'first_created'
                if first_created is None or last_modified.year != first_created.year:
                    fig2dct[dbid]['modified'] = last_modified
        # Find the unique date-author combinations
        dateau_list = self._get_edit_date_au(fig2dct.values())
        idx2dateau = {i:nt for i, nt in enumerate(dateau_list)}
        print('  {HMS} {N:,} Figures HAVE EDIT DATES'.format(HMS=get_hms(tic), N=len(fig2dct)))
        return fig2dct

    def _get_edit_date_au(self, dct_dates):
        """Get years edited and authorname from the list of first_created and last_modified."""
        date_au = set()
        for dct in dct_dates:
            if 'created' in dct:
                date_au.add(dct['created'])
            if 'modified' in dct:
                date_au.add(dct['modified'])
        print('  {HMS} {N:,} UNIQUE EDIT AUTHOR DATES'.format(HMS=get_hms(self.tic), N=len(date_au)))
        return sorted(date_au, key=lambda nt: [-1*nt.year, nt.authors])


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
