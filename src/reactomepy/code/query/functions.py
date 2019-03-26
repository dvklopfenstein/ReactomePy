"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import timeit
import collections as cx
from reactomepy.code.neo4jnodebasic import Neo4jNodeBasic
from reactomepy.code.utils import get_hms
from reactomepy.code.query.relationship_agg import RelationshipCollapse
from reactomepy.code.node.schemaclass_factory import SCHEMACLASS2CLS
from reactomepy.code.relationships import Relationships

class NodeHier():
    """Create, collect, and report a Node hierarchy."""

    qidpat = ('WITH [{DBIDS}] AS dbIds MATCH (src)-[rels:{RELS}*]->(dst) WHERE src.dbId in dbIds '
              'RETURN DISTINCT '
              'src.dbId AS src_dbId, src.schemaClass AS src_schemaClass, '
              'dst.dbId AS dst_dbId, dst.schemaClass AS dst_schemaClass')

    patini = ('MATCH (src:DatabaseObject{PARAMS})-[rels:RELS*]->(dst) RETURN DISTINCT '
              'src.dbId AS src_dbId, src.schemaClass AS src_schemaClass, '
              'dst.dbId AS dst_dbId, dst.schemaClass AS dst_schemaClass')
              #'rels, '

    # inferredTo increases query times greatly, so exclude
    excl_rel_dft = {'inferredTo', 'crossReference'}

    def __init__(self, gdbdr, excl_rel=None, all_details=True):
        self.gdbdr = gdbdr
        self.excl_rel = self.excl_rel_dft if excl_rel is None else set(excl_rel)
        self.all_details = all_details

    def wr_dbid2node(self, fout_txt, dct_full):
        """Write all nodes in a verbose format."""
        excl = {'ReferenceDatabase'}
        with open(fout_txt, 'w') as prt:
            prt.write('{Q}\n\n'.format(Q=dct_full['query']))
            prt.write('Relationships in query:\n')
            for rel in sorted(dct_full['relationships']):
                prt.write("    '{REL}',\n".format(REL=rel))
            prt.write('\n\n')
            dbid2dct = dct_full['dbid2dct']
            self.prt_summary(dct_full['dbid2node'], prt)
            for nodebasic in dct_full['dbid2node'].values():
                if nodebasic.objsch.name in excl:
                    continue
                prt.write('\n>>>>>>>\n{NODE}\n-------\n'.format(NODE=nodebasic))
                dct_cur = dbid2dct[nodebasic.item_id]
                prt.write('DCT: {DCT}\n'.format(DCT=self.getstr_dct(dct_cur)))
                prt.write('=======\n')
                for rel, dst_dbnodes in nodebasic.relationship.items():
                    if rel in Relationships.physicalentity_hier:
                        ctr = cx.Counter(o.objsch.name for o in dst_dbnodes)
                        ctrmsg = ['{N}:{S}'.format(S=k, N=v) for k, v in ctr.most_common()]
                        prt.write('{SRC} REL {R} {DST}\n'.format(
                            SRC=nodebasic.objsch.name, R=rel, DST=' '.join(ctrmsg)))
                    else:
                        for dst in dst_dbnodes:
                            param_vals = sorted(dbid2dct[dst.item_id].items())
                            dctlst = ['{}({})'.format(k, v) for k, v in param_vals]
                            prt.write('{SRC} REL {R} {DST}\n'.format(
                                SRC=nodebasic.objsch.name, R=rel, DST='\n    '.join(dctlst)))
                prt.write('<<<<<<<\n')
            print('  {N:,} nodes WROTE: {TXT}'.format(N=len(dct_full['dbid2node']), TXT=fout_txt))

    @staticmethod
    def prt_summary(dbid2node, prt=sys.stdout):
        """Print query summary."""
        ctrsch = cx.Counter()
        ctrrel = cx.Counter()
        for node in dbid2node.values():
            ctrsch[node.objsch.name] += 1
            for rel in node.relationship:
                ctrrel[rel] += 1
        prt.write('  {N:6} nodes\n'.format(N=len(dbid2node)))
        prt.write('  {N:6} schemaClasses used:\n'.format(N=len(ctrsch)))
        for sch, cnt in ctrsch.most_common():
            prt.write('        {N:6} {SCH}\n'.format(N=cnt, SCH=sch))
        prt.write('  {N:6} relationship types:\n'.format(N=len(ctrrel)))
        for rel, cnt in ctrrel.most_common():
            prt.write('        {N:6} {REL}\n'.format(N=cnt, REL=rel))

    def get_dbid2node(self, paramvalstr, rels, exact=True):
        """1) Find user-specfied Node and return it and all Nodes below it."""
        # Ex: paramvalstr='stId:"R-HSA-167199"'
        print('FIND ALL LOWER-LEVEL NODE IDS...')
        query = self.get_query(rels, paramvalstr)
        print(query)
        print('GET ALL dbIds from QUERY AND LOWER')
        dbid2node, src_dbids = self.ses_dbid2nodebasic_srcdst(query, prt=sys.stdout)
        dbid2dct = self.get_dbid2dct_g_dbid2nodeb(dbid2node, exact)
        print('FILL DICT WITH PARAMETER VALUES AND RELATIONSHIP DESTINATION NODES')
        return {'dbid2node':dbid2node, 'dbid2dct':dbid2dct, 'relationships':rels,
                'query':query, 'src_dbids':src_dbids}

    def get_query_dbids(self, dbids, rels):
        """Get query to return all lower-level nodes of a set of dbIds."""
        #### tic = timeit.default_timer()
        return self.qidpat.format(DBIDS=", ".join(str(n) for n in dbids), RELS='|'.join(sorted(rels)))
        #### if prt:
        ####     prt.write('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(HMS=get_hms(tic), N=len(dbid2dct), Q=qry))

    def get_query(self, rels, paramstr):
        """1a) Get query to return all lower-level nodes."""
        query = self.patini.replace('PARAMS', paramstr)
        query = query.replace('RELS', '|'.join(sorted(rels)))
        return query

    def get_dbid2dct_g_dbid2nodeb(self, dbid2node, exact=True):
        """1c) Fill descendants/ancestors for all Nodes."""
        dbid2dct = self.ses_relationship_dcts(dbid2node)
        print('COLLAPSE SOME RELATIONSHIPS INTO MAIN DICT')
        objrel = RelationshipCollapse(dbid2node, dbid2dct, exact)
        objrel.merge_dctvals()
        # popped = self.collapse_relationships(dbid2node)
        # for rel, item in popped.items():
        #     print(rel)
        print('FROM DICT MAKE NAMEDTUPLE ON NODE')
        for dbid, dct in dbid2dct.items():
            node = dbid2node[dbid]
            node.ntp = node.objsch.get_nt_g_dct(dct)
        print('COLLAPSE HIERARCHY RELATIONSHIPS INTO CHILDREN')
        objrel.mv_children_parents(Relationships.physicalentity_hier)
        objrel.set_dcnt()
        objrel.set_ancestors()
        return dbid2dct

    def ses_relationship_dcts(self, dbid2nodebasic):
        """Add parameter values and relationships w/their destination dbIds."""
        with self.gdbdr.session() as session:
            pat = 'MATCH (s:DatabaseObject{dbId:ID})-[r]->(d) RETURN s, r, d.dbId AS d_Id'
            #### id2node_norel = self._addval_src_rel_dst(pat, dbid2nodebasic, session)
            dbid2dct = self._addval_src_rel_dst(pat, dbid2nodebasic, session)
            pat = 'MATCH (src:DatabaseObject{{dbId:{DBID}}}) RETURN src'
            dbid2node_missing = {n:o for n, o in dbid2nodebasic.items() if not o.relationship}
            assert not set(dbid2dct).issubset(dbid2node_missing), '{D} {M}'.format(
                D=len(dbid2dct), M=len(dbid2node_missing))
            #### self._addval_src_norel(pat, id2node_norel, session)
            dbid2dct.update(self._addval_src_norel(pat, dbid2node_missing, session))
            assert len(dbid2dct) == len(dbid2nodebasic)
            return dbid2dct

    def get_dbid2nodedct(self, dbids):
        """Get Neo4jNodes with neo4j params in a dict and direct children relationships loaded."""
        # Run 1: MATCH (src:DatabaseObject{dbId:DBID}) RETURN src.schemaClass AS schemaClass
        dbid2sch = self.ses_dbid2sch(dbids)
        assert set(dbids) == set(dbid2sch), "TBD: Report dbIds NOT FOUND"
        dbid2nodebasic = {dbid:Neo4jNodeBasic(dbid, sch) for dbid, sch in dbid2sch.items()}
        # Run 2a: MATCH (s:DatabaseObject{dbId:ID})-[r]->(d) RETURN s, r, d.dbId AS d_Id
        # Run 2b: MATCH (src:DatabaseObject{{dbId:{DBID}}}) RETURN src
        dbid2dct = self.get_dbid2dct_g_dbid2nodeb(dbid2nodebasic)
        return {'dbid2node':dbid2nodebasic, 'dbid2dct':dbid2dct}

    def ses_dbid2sch(self, dbids):
        """Given schemaClass given dbId for a set of dbIds."""
        dbid2sch = {}
        # 'MATCH (src:DatabaseObject{dbId:DBID}) RETURN src.schemaClass AS schemaClass'
        pre = 'MATCH (src:DatabaseObject{dbId:'
        post = '}) RETURN src.schemaClass AS schemaClass'
        with self.gdbdr.session() as session:
            for dbid in dbids:
                query = pre + str(dbid) + post
                for rec in session.run(query).records():
                    dbid2sch[dbid] = rec['schemaClass']
        return dbid2sch

    def ses_dbid2nodebasic_srcdst(self, query, prt=sys.stdout, idxmod=100000):
        """1b) Get the schemaClasses and dbIds for all nodes below the specified node."""
        # MATCH (src{USERVALS})-[rels:RELS*]->(dst) RETURN DISTINCT ...
        dbid2nodebasic = {}
        src_dbids = set()
        tic = timeit.default_timer()
        print('HELLO')
        with self.gdbdr.session() as session:
            for idx, rec in enumerate(session.run(query).records()):
                print('REC:', rec)
                src_dbid = rec['src_dbId']
                dst_dbid = rec['dst_dbId']
                src_dbids.add(src_dbid)
                if src_dbid not in dbid2nodebasic:
                    self._add_id2nodeb(dbid2nodebasic, src_dbid, rec['src_schemaClass'])
                if dst_dbid not in dbid2nodebasic:
                    self._add_id2nodeb(dbid2nodebasic, dst_dbid, rec['dst_schemaClass'])
                if prt and idx%idxmod == 0:
                    prt.write('  {HMS} {IDX:7,} {NT} ...\n'.format(HMS=get_hms(tic), IDX=idx, NT=rec))
        if prt:
            prt.write('  HMS: {HMS} {N:6,} dbIds: {Q}\n'.format(
                HMS=get_hms(tic), N=len(dbid2nodebasic), Q=query))
        return dbid2nodebasic, src_dbids

    def ses_dbid2nodebasic_src(self, query):
        """Get the schemaClasses and dbIds for all nodes below the specified node."""
        # MATCH (src{USERVALS}) RETURN DISTINCT ...
        dbid2nodebasic = {}
        src_dbids = set()
        tic = timeit.default_timer()
        with self.gdbdr.session() as session:
            for idx, rec in enumerate(session.run(query).records()):
                src_dbid = rec['src_dbId']
                src_dbids.add(src_dbid)
                if src_dbid not in dbid2nodebasic:
                    self._add_id2nodeb(dbid2nodebasic, src_dbid, rec['src_schemaClass'])
                if idx%100000 == 0:
                    print('  {HMS} {IDX:7,} {NT} ...'.format(HMS=get_hms(tic), IDX=idx, NT=rec))
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
            HMS=get_hms(tic), N=len(dbid2nodebasic), Q=query))
        return dbid2nodebasic, src_dbids

    @staticmethod
    def _add_id2nodeb(dbid2nodebasic, dbid, schemaclass):
        """Add a Neo4jNodeBasic node to the dbId dict."""
        if dbid not in dbid2nodebasic:
            dbid2nodebasic[dbid] = Neo4jNodeBasic(dbid, schemaclass)

    #### def _addval_src_norel(self, pat, id2node_norel, session):
    @staticmethod
    def _addval_src_norel(pat, dbid2node_missing, session):
        """Add paramter values for node IDs that have no relationships."""
        # MATCH (src:DatabaseObject{dbId:DBID}) RETURN src
        dbid2dct = {}
        tic = timeit.default_timer()
        for dbid, nodebasic in dbid2node_missing.items():
            qry = pat.format(DBID=str(dbid))
            for rec in session.run(qry).records():
                dbid2dct[dbid] = nodebasic.objsch.get_dict(rec['src'])
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
            HMS=get_hms(tic), N=len(dbid2node_missing,), Q=qry))
        return dbid2dct

    def _addval_src_rel_dst(self, pat, dbid2nodebasic, session):
        """Get dict w/parameter values and relationships w/their destination dbIds."""
        # MATCH (s:DatabaseObject{dbId:ID})-[r]->(d) RETURN s, r, d.dbId AS d_Id
        dbid2dct = {}
        #### dbid2nodenorel = {}
        tic = timeit.default_timer()
        for dbid, nodebasic in dbid2nodebasic.items():
            qry = pat.replace('ID', str(dbid))
            for rec in session.run(qry).records():
                #### nodebasic.dct = nodebasic.objsch.get_dict(rec['s'])
                dbid2dct[dbid] = nodebasic.objsch.get_dict(rec['s'])
                rel = rec['r'].type
                dstid = rec['d_Id']
                if dstid in dbid2nodebasic and rel not in self.excl_rel:
                    nodebasic.relationship[rel].add(dbid2nodebasic[dstid])
            #### if not nodebasic.relationship:
            ####     dbid2nodenorel[dbid] = nodebasic
        print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(HMS=get_hms(tic), N=len(dbid2dct), Q=qry))
        #### print('  HMS: {HMS} {N:6,} dbIds: {Q}'.format(
        ####     HMS=get_hms(tic), N=len(dbid2nodebasic)-len(dbid2nodenorel), Q=qry))
        #### return dbid2nodenorel
        return dbid2dct

    def get_rels_g_schs(self, schemaClasses):
        """Get the set of relationships to return all lower-level nodes."""
        rels = set()
        for sch in schemaClasses:
            rels.update(self.get_rels(sch))
        rels.difference_update(self.excl_rel)
        return rels

    def get_rels(self, schemaclass):
        """Get the set of relationships to return all lower-level nodes."""
        rels = get_relationships_lte(schemaclass)
        rels.difference_update(self.excl_rel)
        return rels

    @staticmethod
    def getstr_dct(dct):
        """Print params dct of one node."""
        # Required Parameters on this Node
        msg = ['{dbId} {schemaClass}'.format(dbId=dct['dbId'], schemaClass=dct['schemaClass'])]
        msg[0] += ' ' + dct['displayName']
        excl = {'dbId', 'schemaClass', 'displayName', 'optional'}
        dctlst = ['{}({})'.format(k, v) for k, v in sorted(dct.items()) if k not in excl]
        if dctlst:
            msg.append('\n    '.join(dctlst))
        # Optional Parameters on this Node
        if 'optional' in dct:
            optlst = ['{}({})'.format(k, v) for k, v in sorted(dct['optional'].items())]
            msg.append('\n    '.join(optlst))
        return '\n    '.join(msg)

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
    cls = SCHEMACLASS2CLS[schemaclass]
    for rels_cur in cls.relationships:
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
    cls = SCHEMACLASS2CLS[schemaclass]
    for rels_cur, schs_cur in cls.relationships.items():
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
