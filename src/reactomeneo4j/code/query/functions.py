"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import timeit
import datetime
from collections import Counter
from reactomeneo4j.code.node.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR
from reactomeneo4j.code.neo4jnodebasic import Neo4jNodeBasic

class NodeHier():
    """Create, collect, and report a Node hierarchy."""

    patini = ('MATCH (src:SCH{PARAMS})-[rels:RELS*]->'
              '(dst) RETURN DISTINCT '
              'src.dbId AS src_dbId, src.schemaClass AS src_schemaClass, '
              'dst.dbId AS dst_dbId, dst.schemaClass AS dst_schemaClass')
              #'rels, '

    def __init__(self, gdbdr):
        self.gdbdr = gdbdr

    def get_dbid2nodebasic(self, schemaclass, paramstr, exclude=None):
        """Get the schemaClasses and dbIds for all nodes below cyphnode."""
        dbid2nodebasic = {}
        tic = timeit.default_timer()
        query = self.get_query(schemaclass, paramstr, self.patini, exclude)
        relctr = Counter()
        with self.gdbdr.session() as session:
            for rec in session.run(query).records():
                if rec['src_dbId'] not in dbid2nodebasic:
                    self._add_id2nodeb(dbid2nodebasic, rec['src_dbId'], rec['src_schemaClass'])
                if rec['dst_dbId'] not in dbid2nodebasic:
                    self._add_id2nodeb(dbid2nodebasic, rec['dst_dbId'], rec['dst_schemaClass'])
                #print('RRRRRRRRRRRRRR DST {SCH:32}'.format(SCH=rec['dst_schemaClass']), [r.type for r in rec['rels']])
        print('  HMS: {HMS} {N} dbIds'.format(HMS=self.get_hms(tic), N=len(dbid2nodebasic)))
        #self._prt_summary(tic, dbid2nodebasic, relctr)
        return dbid2nodebasic

    def _prt_summary(tic, dbid2nodebasic, relctr):
        """Print nodes and relationships found by query."""
        # for rel, cnt in rectr.items():
        #     print('  {N} {REL}'.format(N=cnt, REL=rel))

    @staticmethod
    def _add_id2nodeb(dbid2nodebasic, dbid, schemaclass):
        """Add a Neo4jNodeBasic node to the dbId dict."""
        dbid2nodebasic[dbid] = Neo4jNodeBasic(dbid, schemaclass)

    def get_query(self, schemaclass, paramstr, qrypat, exclude):
        """Get query to return all lower-level nodes."""
        query = qrypat.replace('SCH', schemaclass)
        query = query.replace('PARAMS', paramstr)
        rels = self.get_rels(schemaclass, exclude)
        query = query.replace('RELS', '|'.join(sorted(rels)))
        print('QQQQQQQQQQQQQQ', query)
        return query

    @staticmethod
    def get_rels(schemaclass, exclude):
        """Get relationships to query."""
        rels = get_relationships_lte(schemaclass)
        if exclude is None:
            # inferredTo increases query times greatly, so exclude
            rels.discard('inferredTo')
        else:
            rels.discard(exclude)
        return rels

    @staticmethod
    def get_hms(tic):
        """Get hours, minutes, seconds."""
        return str(datetime.timedelta(seconds=(timeit.default_timer()-tic)))

def get_version(gdbdr):
    """Get Reactome version."""
    version = None
    query = 'MATCH (v:DBInfo) RETURN v'
    with gdbdr.session() as session:
        for rec in session.run(query).records():
            dbinfo = rec['v']
            assert dbinfo.get('name') == 'reactome'
            version = dbinfo.get('version')
    assert version is not None
    return version

def get_relationships(schemaclass):
    """Given a DatabaseObject in code.node, return relationships of derived nodes."""
    rels_all = set()
    obj = SCHEMACLASS2CONSTRUCTOR[schemaclass]
    for rels_cur in obj.relationships:
        rels_all.add(rels_cur)
    return rels_all

def get_relationships_lte(schemaclass):
    """Given a DatabaseObject in code.node, return relationships of derived nodes."""
    rels_all = set()
    schs_all = set()
    seen = set()
    _get_relationships_lte(schemaclass, seen, rels_all, schs_all)
    for rel in sorted(rels_all):
        print('REL', rel)
    # print('SCH', schs_all)
    return rels_all

def _get_relationships_lte(schemaclass, seen, rels_all, schs_all):
    if schemaclass in seen:
        return
    # print('PPPPPPPP', schemaclass)
    seen.add(schemaclass)
    obj = SCHEMACLASS2CONSTRUCTOR[schemaclass]
    for rels_cur, schs_cur in obj.relationships.items():
        rels_all.add(rels_cur)
        schs_all.update(schs_cur)
    for sch in schs_all.difference(seen):
        _get_relationships_lte(sch, seen, rels_all, schs_all)

def get_dbids(gdbdr, nodestr='Complex{stId:"R-HSA-167199"}'):
    """Get DatabaseObject dbId, which is present on all Nodes."""
    dbids = set()
    query = 'MATCH (n:NODESTR) RETURN n'.format(NODESTR=nodestr)
    with gdbdr.session() as session:
        for rec in session.run(query).records():
            dbids.add(rec['n']['dbId'])
    return dbids


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
