"""Holds information for one data schema item."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
from collections import namedtuple
from reactomeneo4j.code.node.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Neo4jNode():
    """Holds data extracted from Neo4j."""

    # Query to determine Nodes in this item's relationships
    qrypat = 'MATCH (src:DatabaseObject{{dbId:{DBID}}})-[rel]->(dst) RETURN src, rel, dst'
    ntrel = namedtuple('NtRel', 'rel dst')

    def __init__(self, neo4jnode, **kws):  # gdbdr=None, prtfmt=None):
        # kws: gdbdr prtfmt
        self.objsch = self._init_objsch(neo4jnode['schemaClass'])
        self.rel_excl = kws['rel_excl'] if 'rel_excl' in kws else {'inferredTo'}
        self.ntrels = self._init_ntrels(neo4jnode['dbId'], kws.get('gdbdr'))
        self.ntp = self.objsch.get_nt(neo4jnode)
        self.fmtpat = kws['prtfmt'] if 'prtfmt' in kws else self.objsch.fmtpat

    def __str__(self):
        return self.fmtpat.format(**self.ntp._asdict())

    def prt_verbose(self, prt):
        """Return a string with all details of the Node and its relationships."""
        prt.write('\n{NT}\n'.format(NT=self.ntp)) 
        prt.write('\n{O}\n'.format(O=self)) 
        for ntrel in self.ntrels:
            prt.write('DDDD {REL:20} {D}\n'.format(REL=ntrel.rel, D=ntrel.dst))

    # def _init_rels(self, **kws):
    #     """Collect all Neo4j Nodes at the end of this object's relationships."""
    #     rel2nodes = {}
    #     if 'gdbdr' in kws:
    #         # print('\n--------------------------------------------------------------')
    #         # print(self)
    #         gdbdr = kws['gdbdr']
    #         for rel, schset in self.objsch.relationships.keys():
    #             for exp_sch in schset:
    #                 rel2nodes[rel] = self.__init_rels(rel, exp_sch, gdbdr)
    #     return rel2nodes

    def __init_ntrels(self, dbid, gdbdr):
        """Query for objects at the end of this relationship."""
        rels = []
        qryrel = '|'.join(self.objsch.relationships.keys())
        qry = self.qrypat.format(DBID=dbid, REL=qryrel)
        #print('\n{Q}'.format(Q=qry))
        with gdbdr.session() as session:
            _ntrel = self.ntrel
            for idx, rec in enumerate(session.run(qry).records()):
                rel = rec['rel'].type
                if rel not in self.rel_excl:
                    #print('{IDX} {REL:19} {NODE}'.format(IDX=idx, REL=rec['rel'].type, NODE=rec['dst']))
                    rels.append(_ntrel(rel=rel, dst=Neo4jNode(rec['dst'])))
        return rels

    def _init_ntrels(self, dbid, gdbdr):
        """Initialize relationships."""
        ntrels = []
        if gdbdr:
            return self.__init_ntrels(dbid, gdbdr)
        return ntrels

    @staticmethod
    def _init_objsch(sch):
        """Given schemaClass, create data framework object."""
        assert sch in SCHEMACLASS2CONSTRUCTOR, '**FATAL: BAD schemaClass({S})'.format(S=sch)
        return SCHEMACLASS2CONSTRUCTOR[sch]

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
