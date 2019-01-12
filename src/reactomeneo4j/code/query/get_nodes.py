"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import re
import timeit
import collections as cx
from reactomeneo4j.code.neo4jnode import Neo4jNode
# from reactomeneo4j.code.neo4jnodebasic import Neo4jNodeBasic
from reactomeneo4j.code.utils import get_hms
# from reactomeneo4j.code.query.relationship_agg import RelationshipCollapse
# from reactomeneo4j.code.node.schemaclass_factory import SCHEMACLASS2CLS
# from reactomeneo4j.code.relationships import Relationships


class NodeGetter():
    """Get a node or set of nodes with data filled in."""

    def __init__(self, gdbdr):
        self.tic = timeit.default_timer()
        self.gdbdr = gdbdr

    def prt_summary_dbid2rel2sch2dbids(self, dbid2rel2sch2dbids, prt=sys.stdout):
        prt.write("# SUMMARY OF RELATIONSHIPS/DESTINATION COUNTS FOR {N:} dbIds:\n".format(
            N=len(dbid2rel2sch2dbids)))
        rel2dstcnt = self._get_rel_cnts(dbid2rel2sch2dbids)
        for (rel, dsch), cnt in sorted(rel2dstcnt.items(), key=lambda t: [t[0][0], -1*t[1]]):
            prt.write('#     {N:7,} {REL:20} {DSCH}\n'.format(N=cnt, REL=rel, DSCH=dsch))

    def get_dbid2val(self, qry, prt=sys.stdout):
        """Get a value for every dbId from Reactome."""
        dbid2val = {}
        # Example: 'MATCH (f:Figure) RETURN f.dbId AS dbId, f.url AS val'
        with self.gdbdr.session() as session:
            for rec in session.run(qry).records():
                dbid2val[rec['dbId']] = rec['val']
        if prt:
            prt.write('  {HMS} {N:,} dbIds: {Q}\n'.format(
                HMS=get_hms(self.tic), N=len(dbid2val), Q=self._shorten_queryprt(qry)))
        return dbid2val

    def get_dbid2set(self, qry, prt=sys.stdout):
        """Get a set of values for every dbId from Reactome."""
        dbid2set = cx.defaultdict(set)
        # Example: MATCH (s:InstanceEdit)-[r]->(f:Figure) RETURN s.dbId AS dbId, f.dbId AS val
        with self.gdbdr.session() as session:
            for rec in session.run(qry).records():
                dbid2set[rec['dbId']].add(rec['val'])
        if prt:
            prt.write('  {HMS} {N:,} dbIds: {Q}\n'.format(
                HMS=get_hms(self.tic), N=len(dbid2set), Q=self._shorten_queryprt(qry)))
        return {dbid:vals for dbid, vals in dbid2set.items()}

    def get_dbid2ntset(self, qry, prt=sys.stdout):
        """Get a set of tuples (rel, dst.dbId) for each spepcified source dbId from Reactome."""
        dbid2ntset = cx.defaultdict(set)
        # Ex: MATCH (e:InstanceEdit)-[r]->(f:Figure)
        #     RETURN f.dbId AS key_dbId, type(r) AS rtyp, e.dbId AS val_dbId
        ntobj = cx.namedtuple('NtIdRel', 'dbId rel')
        with self.gdbdr.session() as session:
            for rec in session.run(qry).records():
                dbid2ntset[rec['key_dbId']].add(ntobj(dbId=rec['val_dbId'], rel=rec['rtyp']))
        if prt:
            prt.write('  {HMS} {N:,} rel-dbIds: {Q}\n'.format(
                HMS=get_hms(self.tic), N=len(dbid2ntset), Q=self._shorten_queryprt(qry)))
        return {dbid:vals for dbid, vals in dbid2ntset.items()}

    # def get_dbid2node2(self, dbids):
    #     """Get Summation as a Neo4jNode."""
    #     dbid2node = {}
    #     tic = timeit.default_timer()
    #     qupat = 'WITH [{IDs}] AS IDs MATCH (s) WHERE s.dbId IN IDs RETURN s'
    #     with self.gdbdr.session() as session:
    #         query = qupat.format(IDs=', '.join(str(i) for i in dbids))
    #         for rec in session.run(query).records():
    #             node = rec['s']
    #             dbid2node[node['dbId']] = Neo4jNode(node)
    #     print('SLOW  {HMS} {N:,} nodes found'.format(HMS=get_hms(tic), N=len(dbid2node)))
    #     return dbid2node

    def get_nodes(self, srchstr, msg=None):
        """Get Summation as a Neo4jNode."""
        nodes = []
        tic = timeit.default_timer()
        qry = 'MATCH (s:{SRCHSTR}) RETURN s'.format(SRCHSTR=srchstr)
        with self.gdbdr.session() as session:
            for rec in session.run(qry).records():
                nodes.append(Neo4jNode(rec['s']))
        print('  {HMS} {N:,} {MSG}'.format(HMS=get_hms(tic), N=len(nodes), MSG=msg if msg else srchstr))
        return nodes

    def get_dbid2node(self, dbids, msg='nodes found'):
        """Get Summation as a Neo4jNode."""
        dbid2node = {}
        tic = timeit.default_timer()
        qupat = 'MATCH (s:DatabaseObject{{dbId:{DBID}}}) RETURN s'
        with self.gdbdr.session() as session:
            for dbid in dbids:
                query = qupat.format(DBID=dbid)
                for rec in session.run(query).records():
                    dbid2node[dbid] = Neo4jNode(rec['s'])
        print('FASTISH  {HMS} {N:,} {MSG}'.format(HMS=get_hms(tic), N=len(dbid2node), MSG=msg))
        return dbid2node

    @staticmethod
    def _shorten_queryprt(qry):
        """Shorten print of query if it starts with WITH and is long."""
        len_qry = len(qry)
        if len_qry < 120:
            return qry
        if qry[:5] == 'WITH ':
            return re.sub(r'WITH \[.*\] AS', 'WITH [...] AS', qry, flags=re.I)
        return qry

    def get_dbid2rel2sch2dbids(self, nodestr, prt=sys.stdout):
        """2) Get all Pathway (includes TopLevelPathway) dbIds."""
        qrypat = ('MATCH (s:{NODESTR})-[r]->(d) '
                  'RETURN s.dbId AS src_dbid, type(r) AS rtyp, '
                  'd.dbId AS dst_dbid, d.schemaClass AS dsch')
        query = qrypat.format(NODESTR=nodestr)
        dbid2rel2sch2dbids = cx.defaultdict(lambda: cx.defaultdict(lambda: cx.defaultdict(set)))
        # 1) Get a list of all Pathways, with the number of TopLevelPathways
        # 2) For each pathway, find all relationships
        with self.gdbdr.session() as session:
            print("QUERY: {Q}".format(Q=query))
            idx = 0
            for idx, rec in enumerate(session.run(query).records(), 1):
                dbid2rel2sch2dbids[rec['src_dbid']][rec['rtyp']][rec['dsch']].add(rec['dst_dbid'])
            print('  {HMS} {N:,} Pathways over {R:,} records: {QU}'.format(
                HMS=get_hms(self.tic), QU=query, N=len(dbid2rel2sch2dbids), R=idx))
        # 3) Report the number of relationships and destination schemaClass types
        if prt:
            self.prt_summary_dbid2rel2sch2dbids(dbid2rel2sch2dbids, prt)
        return dbid2rel2sch2dbids

    @staticmethod
    def _get_rel_cnts(dbid2rel2sch2dbids):
        """Get counts of relationships seen in pathways.
            85,736 hasEvent             Reaction
            23,694 hasEvent             Pathway
             7,761 hasEvent             BlackBoxEvent
               349 hasEvent             FailedReaction
               227 hasEvent             Polymerisation
                36 hasEvent             Depolymerisation

             1,348 precedingEvent       Pathway
               426 precedingEvent       Reaction
                21 precedingEvent       BlackBoxEvent

             4,692 hasEncapsulatedEvent Pathway
                18 hasEncapsulatedEvent TopLevelPathway

            23,524 summation            Summation
            23,520 species              Species
            21,071 evidenceType         EvidenceType
            20,689 inferredTo           Pathway
            15,796 compartment          Compartment
            12,332 goBiologicalProcess  GO_BiologicalProcess
             9,437 literatureReference  LiteratureReference
               112 literatureReference  Book
                11 literatureReference  URL
             1,830 crossReference       DatabaseIdentifier
               542 disease              Disease
               408 inferredTo           TopLevelPathway
               300 normalPathway        Pathway
               279 figure               Figure
               206 relatedSpecies       Species
        """
        ctr = cx.Counter()
        for rel2sch2dbids in dbid2rel2sch2dbids.values():
            for rel, sch2dbids in rel2sch2dbids.items():
                for sch, dbids in sch2dbids.items():
                    ctr[(rel, sch)] += len(dbids)
        return ctr

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
