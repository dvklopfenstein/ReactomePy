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

    def get_dbids(self, qry, prt=sys.stdout):
        """Get dbIds given a query."""
        # Example: 'MATCH (s:Figure) RETURN s.dbId AS dbId'
        dbids = set()
        with self.gdbdr.session() as session:
            for idx, rec in enumerate(session.run(qry).records()):
                dbids.add(rec['dbId'])
                if prt and idx%10000 == 0:
                    prt.write('{HMS} {IDX} {DBID}'.format(
                        HMS=get_hms(self.tic), IDX=idx, DBID=rec['dbId']))
        return dbids

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

    def get_dbid2ntnodes(self, qry, prt=sys.stdout):
        """Get a set of tuples (rel, dst.dbId) for each specified source dbId from Reactome."""
        dbid2ntnodes = cx.defaultdict(dict)
        # Ex: MATCH (s:InstanceEdit)-[r]->(d:Figure) RETURN s, type(r) AS rtyp, d
        ntobjkey = cx.namedtuple('NtIdRel', 'dbId rel')
        ntobjnode = cx.namedtuple('NtSRD', 'src rel dst')
        with self.gdbdr.session() as session:
            for rec in session.run(qry).records():
                src = rec['s']
                rel = rec['rtyp']
                dst = rec['d']
                ntkey = ntobjkey(dbId=dst['dbId'], rel=rel)
                ntnodes = ntobjnode(src=src, rel=rel, dst=dst)
                dbid2ntnodes[dst['dbId']][ntkey] = ntnodes
        if prt:
            prt.write('  {HMS} {N:,} rel-dbIds: {Q}\n'.format(
                HMS=get_hms(self.tic), N=len(dbid2ntnodes), Q=self._shorten_queryprt(qry)))
        return {dbid:vals for dbid, vals in dbid2ntnodes.items()}

    def get_nodes(self, srchstr, msg=None):
        """Get Summation as a Neo4jNode."""
        nodes = []
        tic = timeit.default_timer()
        qry = 'MATCH (s:{SRCHSTR}) RETURN s'.format(SRCHSTR=srchstr)
        with self.gdbdr.session() as session:
            for rec in session.run(qry).records():
                nodes.append(Neo4jNode(rec['s']))
        print('  {HMS} {N:,} {MSG}'.format(
            HMS=get_hms(tic), N=len(nodes), MSG=msg if msg else srchstr))
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


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
