"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import timeit
import collections as cx
from reactomeneo4j.code.neo4jnodebasic import Neo4jNodeBasic
from reactomeneo4j.code.utils import get_hms
from reactomeneo4j.code.query.relationship_agg import RelationshipCollapse
from reactomeneo4j.code.node.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR
from reactomeneo4j.code.node.databaseobject import DatabaseObject

class NodeHier():
    """Create, collect, and report a Node hierarchy."""

    patini = ('MATCH (src:DatabaseObject{PARAMS})-[rels:RELS*]->(dst) RETURN DISTINCT '
              'src.dbId AS src_dbId, src.schemaClass AS src_schemaClass, '
              'dst.dbId AS dst_dbId, dst.schemaClass AS dst_schemaClass')
              #'rels, '

    # inferredTo increases query times greatly, so exclude
    excl_rel_dft = {'inferredTo'}

    def __init__(self, gdbdr, excl_rel=None, all_details=True):
        self.gdbdr = gdbdr
        self.excl_rel = self.excl_rel_dft if excl_rel is None else set(excl_rel)
        self.all_details = all_details

    def wr_dbid2node(self, fout_txt, id2node, dbid2dct):
        """Write all nodes."""
        with open(fout_txt, 'w') as prt:
            self.prt_summary(id2node, prt)
            for nodebasic in id2node.values():
                prt.write('\n>>>>>>>\n{NODE}\n-------\n'.format(NODE=nodebasic))
                for rel, dst_dbnodes in nodebasic.relationship.items():
                    for dst in dst_dbnodes:
                        param_vals = sorted(dbid2dct[dst.dbid].items())
                        dctlst = ['{}({})'.format(k, v) for k, v in param_vals]
                        prt.write('{SRC} REL {R} {DST}\n'.format(
                            SRC=nodebasic.sch, R=rel, DST=' '.join(dctlst)))
                prt.write('<<<<<<<\n')
            print('  {N:,} nodes WROTE: {TXT}'.format(N=len(id2node), TXT=fout_txt))

    @staticmethod
    def prt_summary(dbid2node, prt=sys.stdout):
        """Print query summary."""
        ctrsch = cx.Counter()
        ctrrel = cx.Counter()
        for node in dbid2node.values():
            ctrsch[node.sch] += 1
            for rel in node.relationship:
                ctrrel[rel] += 1
        prt.write('  {N:6} nodes\n'.format(N=len(dbid2node)))
        prt.write('  {N:6} schemaClasses used:\n'.format(N=len(ctrsch)))
        for sch, cnt in ctrsch.most_common():
            prt.write('        {N:6} {SCH}\n'.format(N=cnt, SCH=sch))
        prt.write('  {N:6} relationship types:\n'.format(N=len(ctrrel)))
        for rel, cnt in ctrrel.most_common():
            prt.write('        {N:6} {REL}\n'.format(N=cnt, REL=rel))

    def get_dbid2node(self, schemaclass='Complex', paramvalstr='stId:"R-HSA-167199"', exact=True):
        """Find user-specfied Node and return it and all Nodes below it."""
        print('FIND ALL LOWER-LEVEL NODE IDS...')
        dbid2node = self.get_dbid2nodebasic(schemaclass, paramvalstr)
        print('FILL NODES WITH PARAMETER VALUES AND RELATIONSHIPS')
        dbid2dct = self.get_relationship_dcts(dbid2node)
        print('COLLAPSE SOME RELATIONSHIPS INTO MAIN DICT')
        RelationshipCollapse(dbid2node, dbid2dct, exact)
        # popped = self.collapse_relationships(dbid2node)
        # for rel, item in popped.items():
        #     print(rel)
        for dbid, dct in dbid2dct.items():
            node = dbid2node[dbid]
            node.ntp = node.objsch.get_nt_g_dct(dct)
        return dbid2node, dbid2dct

    def get_relationship_dcts(self, dbid2nodebasic):
        """Add parameter values and relationships w/their destination dbIds."""
        with self.gdbdr.session() as session:
            pat = 'MATCH (s:DatabaseObject{dbId:ID})-[r]->(d) RETURN s, r, d.dbId AS d_Id'
            #### id2node_norel = self._addval_src_rel_dst(pat, dbid2nodebasic, session)
            dbid2dct = self._addval_src_rel_dst(pat, dbid2nodebasic, session)
            pat = 'MATCH (src:DatabaseObject{dbId:DBID}) RETURN src'
            dbid2node_missing = {n:o for n, o in dbid2nodebasic.items() if not o.relationship}
            assert not set(dbid2dct).issubset(dbid2node_missing)
            #### self._addval_src_norel(pat, id2node_norel, session)
            dbid2dct.update(self._addval_src_norel(pat, dbid2node_missing, session))
            assert len(dbid2dct) == len(dbid2nodebasic)
            return dbid2dct

    def get_dbid2nodebasic(self, schemaclass, paramstr):
        """Get the schemaClasses and dbIds for all nodes below the specified node."""
        # MATCH (src{USERVALS})-[rels:RELS*]->(dst) RETURN DISTINCT ...
        dbid2nodebasic = {}
        tic = timeit.default_timer()
        qry = self.get_query(schemaclass, paramstr, self.patini)
        with self.gdbdr.session() as session:
            for rec in session.run(qry).records():
                if rec['src_dbId'] not in dbid2nodebasic:
                    self._add_id2nodeb(dbid2nodebasic, rec['src_dbId'], rec['src_schemaClass'])
                if rec['dst_dbId'] not in dbid2nodebasic:
                    self._add_id2nodeb(dbid2nodebasic, rec['dst_dbId'], rec['dst_schemaClass'])
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
            HMS=get_hms(tic), N=len(dbid2nodebasic), Q=qry))
        return dbid2nodebasic

    @staticmethod
    def _add_id2nodeb(dbid2nodebasic, dbid, schemaclass):
        """Add a Neo4jNodeBasic node to the dbId dict."""
        if dbid not in dbid2nodebasic:
            dbid2nodebasic[dbid] = Neo4jNodeBasic(dbid, schemaclass)

    #### def _addval_src_norel(self, pat, id2node_norel, session):
    @staticmethod
    def _addval_src_norel(pat, dbid2node_missing, session):
        """Add paramter values for node IDs that have no relationships."""
        dbid2dct = {}
        tic = timeit.default_timer()
        for dbid, nodebasic in dbid2node_missing.items():
            qry = pat.replace('DBID', str(dbid))
            for rec in session.run(qry).records():
                dbid2dct[dbid] = nodebasic.objsch.get_dict(rec['src'])
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
            HMS=get_hms(tic), N=len(dbid2node_missing,), Q=qry))
        return dbid2dct

    def _addval_src_rel_dst(self, pat, dbid2nodebasic, session):
        """Get dict w/parameter values and relationships w/their destination dbIds."""
        dbid2dct = {}
        #### dbid2nodenorel = {}
        tic = timeit.default_timer()
        for dbid, nodebasic in dbid2nodebasic.items():
            qry = pat.replace('ID', str(dbid))
            for rec in session.run(qry).records():
                #### nodebasic.dct = nodebasic.objsch.get_dict(rec['s'])
                dbid2dct[dbid] = nodebasic.objsch.get_dict(rec['s'])
                rel = rec['r'].type
                if rel not in self.excl_rel:
                    nodebasic.relationship[rel].add(dbid2nodebasic[rec['d_Id']])
            #### if not nodebasic.relationship:
            ####     dbid2nodenorel[dbid] = nodebasic
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(HMS=get_hms(tic), N=len(dbid2dct), Q=qry))
        #### print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
        ####     HMS=get_hms(tic), N=len(dbid2nodebasic)-len(dbid2nodenorel), Q=qry))
        #### return dbid2nodenorel
        return dbid2dct

    def get_query(self, schemaclass, paramstr, qrypat):
        """Get query to return all lower-level nodes."""
        # query = qrypat.replace('SCH', schemaclass)
        query = qrypat.replace('PARAMS', paramstr)
        rels = get_relationships_lte(schemaclass)
        rels.difference_update(self.excl_rel)
        query = query.replace('RELS', '|'.join(sorted(rels)))
        return query


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
    # for rel in sorted(rels_all):
    #     print('REL', rel)
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
