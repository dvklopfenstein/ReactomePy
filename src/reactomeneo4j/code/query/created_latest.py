"""Get the first created and the lastest modified date and author."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
import sys
import timeit
# import datetime
import collections as cx
# from reactomeneo4j.code.neo4jnode import Neo4jNode
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

    ntobj = cx.namedtuple('NtNewMod', 'created modified')

    def __init__(self, gdbdr):
        self.tic = timeit.default_timer()
        self.gdbdr = gdbdr
        self.objng = NodeGetter(gdbdr)

    def get_dbid2nteditsummary(self, dbid2ntreleid):
        """For each dbId, get one namedtuple summarizing: created+au, last_modified+au."""
        # nt: User.dbId -> rel InstanceEdit.dbId, ...
        dbids_instanceedit = set(nt.dbId for nts in dbid2ntreleid.values() for nt in nts)
        edit2authors = self.get_editid2authors(dbids_instanceedit)
        edit2node = self.objng.get_dbid2node(dbids_instanceedit)
        # Get ALL edit dates
        # nt: created/modified dateTime authors
        dbid2ntedits = self.get_editdates(dbid2ntreleid, edit2node, edit2authors)
        # Consolidate to create-au + last_modified-au (if exists)
        dbid2ntd = self.get_edits(dbid2ntedits)  # many dates -> created last_modified
        dateau_list = self._get_edit_date_au(dbid2ntd.values())
        dbid2ntshort = self._get_dbid2ntshort(dbid2ntd, dateau_list)
        return dateau_list, dbid2ntshort

    def _get_dbid2ntshort(self, dbid2ntd, dateau_list):
        """Get namedtuple(created modified) with idx pointing to values."""
        dbid2ntshort = {}
        dateau2idx = {nt:i for i, nt in enumerate(dateau_list)}
        for dbid, ntd in dbid2ntd.items():
            idx0 = dateau2idx.get(ntd.created)
            idxn = dateau2idx.get(ntd.modified)
            dbid2ntshort[dbid] = self.ntobj(created=idx0, modified=idxn)
        return dbid2ntshort

    def get_editid2authors(self, dbids_instanceedit):
        """Create Figure data using associated: InstanceEdit Person."""
        # Given InstanceEdit dbIds, get Persons who author
        edit2auids = self._get_edit2person(dbids_instanceedit, sys.stdout)
        # Given author Person dbIds, get author names
        auids = set(au for aus in edit2auids.values() for au in aus)
        auid2names = self._get_auid2names(auids)
        # editid2authors: Return InstanceEdit dbId -> Authornames
        return {editid:frozenset(auid2names[a] for a in auids) for editid, auids in edit2auids.items()}

    @staticmethod
    def get_editdates(dbid2ntedits, edit2node, edit2authors):
        """Get ALL edit dates for user-nodes."""
        dbid2rel2ntedit = cx.defaultdict(lambda: cx.defaultdict(list))
        ntobj = cx.namedtuple('NtDateAu', 'year authors')
        exp_rels = {'created', 'modified'}
        for dbid_tgt, ntedits in dbid2ntedits.items():
            for ntedit in ntedits:
                dbid_edit = ntedit.dbId
                authors = edit2authors[dbid_edit]
                editnode = edit2node[dbid_edit]
                ntd = ntobj(year=editnode.ntp.dateTime.year, authors=authors)
                dbid2rel2ntedit[dbid_tgt][ntedit.rel].append(ntd)
                assert ntedit.rel in exp_rels, 'NEW FIGURE EDIT RELATIONSHIPS FOUND; UPDATE CODE'
        return dbid2rel2ntedit

    def get_edits(self, dbid2rel2ntedits):
        """Get the instance edit date, created and latest modified, for figures."""
        tic = timeit.default_timer()
        # Keep only first_created and last_modified, if present
        # min_chg = datetime.timedelta(days=15)
        fig2dct = {}
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
        print('  {HMS} {N:,} Figures HAVE EDIT DATES'.format(HMS=get_hms(tic), N=len(fig2dct)))
        return {dbid:self.ntobj(created=dct.get('created'), modified=dct.get('modified')) for dbid, dct in fig2dct.items()}

    def _get_edit_date_au(self, ntd_dates):
        """Get years edited and authorname from the list of first_created and last_modified."""
        date_au = set()
        for ntd in ntd_dates:
            if ntd.created:
                date_au.add(ntd.created)
            if ntd.modified:
                date_au.add(ntd.modified)
        print('  {HMS} {N:,} UNIQUE EDIT AUTHOR DATES'.format(HMS=get_hms(self.tic), N=len(date_au)))
        return sorted(date_au, key=lambda nt: [nt.year, nt.authors])

    def _get_auid2names(self, person_dbids):
        """Get the Person names, fiven Person dbIds."""
        qrypat = ('WITH [{IDs}] AS dbIds_Person MATCH (person:Person) WHERE person.dbId IN dbIds_Person '
                  'RETURN person.dbId AS dbId, person.displayName AS val')
        query = qrypat.format(IDs=', '.join(set(str(au) for au in person_dbids)))
        return self.objng.get_dbid2val(query)  # auid2names

    def _get_edit2person(self, edit_dbids, prt=sys.stdout):
        """Get the Person(s) who author for a set of InstanceEdit dbIds."""
        qrypat = ('WITH [{IDs}] AS dbIds_InstanceEdit '
                  'MATCH (person:Person)-[:author]->(instanceedit:InstanceEdit) '
                  'WHERE instanceedit.dbId IN dbIds_InstanceEdit '
                  'RETURN person.dbId AS val, instanceedit.dbId AS dbId')
        query = qrypat.format(IDs=', '.join(set(str(e) for e in edit_dbids)))
        return self.objng.get_dbid2set(query, prt)  # InstanceEdit.dbId->set(Person.dbId)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
