"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import timeit
import datetime
import collections as cx
from reactomeneo4j.code.node.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR
from reactomeneo4j.code.neo4jnodebasic import Neo4jNodeBasic
from reactomeneo4j.code.node.databaseobject import DatabaseObject

class NodeHier():
    """Create, collect, and report a Node hierarchy."""

    patini = ('MATCH (src:DatabaseObject{PARAMS})-[rels:RELS*]->(dst) RETURN DISTINCT '
              'src.dbId AS src_dbId, src.schemaClass AS src_schemaClass, '
              'dst.dbId AS dst_dbId, dst.schemaClass AS dst_schemaClass')
              #'rels, '

    # inferredTo increases query times greatly, so exclude
    excl_rel_dft = {'inferredTo'}

    def __init__(self, gdbdr, excl_rel=None):
        self.gdbdr = gdbdr
        self.excl_rel = self.excl_rel_dft if excl_rel is None else set(excl_rel)

    def wr_dbid2node(self, fout_txt, id2node):
        """Write all nodes."""
        with open(fout_txt, 'w') as prt:
            self.prt_summary(id2node, prt)
            for nodebasic in id2node.values():
                prt.write('\n>>>>>>>\n{NODE}\n-------\n'.format(NODE=nodebasic))
                for rel, dst_dbnodes in nodebasic.relationship.items():
                    for dst in dst_dbnodes:
                        param_vals = sorted(id2node[dst.dbid].dct.items())
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

    def get_dbid2node(self, schemaclass='Complex', paramvalstr='stId:"R-HSA-167199"'):
        """Find user-specfied Node and return it and all Nodes below it."""
        print('FIND ALL LOWER-LEVEL NODE IDS...')
        dbid2node = self.get_dbid2nodebasic(schemaclass, paramvalstr)
        print('FILL NODES WITH PARAMETER VALUES AND RELATIONSHIPS')
        self.add_values(dbid2node)
        print('COLLAPSE SOME RELATIONSHIPS INTO MAIN DICT')
        self.collapse_relationships(dbid2node)
        # popped = self.collapse_relationships(dbid2node)
        # for rel, item in popped.items():
        #     print(rel)
        for node in dbid2node.values():
            node.ntp = node.objsch.get_nt_g_dct(node.dct)
        return dbid2node

    def collapse_relationships(self, dbid2node):
        """Collapse specfied relationships into the main node dict."""
        popped = {}
        for dbid, node in dbid2node.items():
            k2v = node.dct
            rel = node.relationship
            if 'abc' in k2v and 'species' in rel:
                abc = self._get_abc(k2v['abc'], rel['species'], node)
                k2v['abc'] = abc
                assert abc not in {'???', 'XXX'}
                popped[(dbid, 'species')] = rel.pop('species')
            if 'compartment' in rel:
                for comp in rel['compartment']:
                    if comp.dct['displayName'] not in node.dct['displayName']:
                        print('ADDING COMPARTMENT', node)
                        node.dct['displayName'] += '[{COMP}]'.format(COMP=comp.dct['displayName'])
                popped[(dbid, 'compartment')] = rel.pop('compartment')
        return popped

    @staticmethod
    def _get_abc(abc_param, species_nodes, node):
        """Return a value for abc."""
        _abc = DatabaseObject.species2nt.get
        abc_rel = '-'.join(_abc(o.dct['displayName'], '???').abbreviation for o in species_nodes)
        # if abc_param == '...' or abc_param == abc_rel:
        if abc_param in {'...', abc_rel}:
            return abc_rel
        print('**ERROR: {SCH}{{dbId:{DBID}}} PARAMETER({P}) != species RELATIONSHIP({R})'.format(
            DBID=node.dbid, SCH=node.sch, P=abc_param, R=abc_rel))
        return 'XXX'

    def add_values(self, dbid2nodebasic):
        """Add parameter values and relationships w/their destination dbIds."""
        with self.gdbdr.session() as session:
            pat = 'MATCH (s:DatabaseObject{dbId:ID})-[r]->(d) RETURN s, r, d.dbId AS d_Id'
            id2node_norel = self._addval_src_rel_dst(pat, dbid2nodebasic, session)
            pat = 'MATCH (src:DatabaseObject{dbId:DBID}) RETURN src'
            self._addval_src_norel(pat, id2node_norel, session)

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
            HMS=self.get_hms(tic), N=len(dbid2nodebasic), Q=qry))
        return dbid2nodebasic

    @staticmethod
    def _add_id2nodeb(dbid2nodebasic, dbid, schemaclass):
        """Add a Neo4jNodeBasic node to the dbId dict."""
        if dbid not in dbid2nodebasic:
            dbid2nodebasic[dbid] = Neo4jNodeBasic(dbid, schemaclass)

    def _addval_src_norel(self, pat, id2node_norel, session):
        """Add paramter values for node IDs that have no relationships."""
        tic = timeit.default_timer()
        for dbid, nodebasic in id2node_norel.items():
            qry = pat.replace('DBID', str(dbid))
            for rec in session.run(qry).records():
                nodebasic.dct = nodebasic.objsch.get_dict(rec['src'])
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
            HMS=self.get_hms(tic), N=len(id2node_norel), Q=qry))

    def _addval_src_rel_dst(self, pat, dbid2nodebasic, session):
        """Add parameter values and relationships w/their destination dbIds."""
        dbid2nodenorel = {}
        tic = timeit.default_timer()
        for dbid, nodebasic in dbid2nodebasic.items():
            qry = pat.replace('ID', str(dbid))
            for rec in session.run(qry).records():
                nodebasic.dct = nodebasic.objsch.get_dict(rec['s'])
                rel = rec['r'].type
                if rel not in self.excl_rel:
                    nodebasic.relationship[rel].add(dbid2nodebasic[rec['d_Id']])
            if not nodebasic.relationship:
                dbid2nodenorel[dbid] = nodebasic
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
            HMS=self.get_hms(tic), N=len(dbid2nodebasic)-len(dbid2nodenorel), Q=qry))
        return dbid2nodenorel

    def get_query(self, schemaclass, paramstr, qrypat):
        """Get query to return all lower-level nodes."""
        # query = qrypat.replace('SCH', schemaclass)
        query = qrypat.replace('PARAMS', paramstr)
        rels = get_relationships_lte(schemaclass)
        rels.difference_update(self.excl_rel)
        query = query.replace('RELS', '|'.join(sorted(rels)))
        return query

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
