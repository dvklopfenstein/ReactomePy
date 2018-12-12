"""Holds information for one data schema item."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
from reactomeneo4j.code.neo4j.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Neo4jNode():
    """Holds data extracted from Neo4j."""

    # Query to determine Nodes in this item's relationships
    qrypat = 'MATCH (src)-[rel:{REL}]-(dst) WHERE ID(src) = {ID} RETURN src, rel, dst'

    def __init__(self, neo4jnode, **kws):  # gdbdr=None, prtfmt=None):
        # kws: gdbdr prtfmt
        _sch = neo4jnode['schemaClass']
        assert _sch in SCHEMACLASS2CONSTRUCTOR, '**FATAL: BAD schemaClass({S})'.format(S=_sch)
        self.objsch = SCHEMACLASS2CONSTRUCTOR[_sch]
        self.ntp = self.objsch.get_nt(neo4jnode)
        self.fmtpat = kws['prtfmt'] if 'prtfmt' in kws else self.objsch.fmtpat
        self.rels = self._init_rels(**kws)

    def __str__(self):
        return self.fmtpat.format(**self.ntp._asdict())

    def _init_rels(self, **kws):
        """Collect all Neo4j Nodes at the end of this object's relationships."""
        rel2nodes = {}
        if 'gdbdr' in kws:
            # print('\n--------------------------------------------------------------')
            # print(self)
            gdbdr = kws['gdbdr']
            for rel, schset in self.objsch.relationships.items():
                for exp_sch in schset:
                    rel2nodes[rel] = self.__init_rels(rel, exp_sch, gdbdr)
        return rel2nodes

    def __init_rels(self, rel, exp_sch, gdbdr):
        """Query for objects at the end of this relationship."""
        qry = self.qrypat.format(ID=self.ntp.Node_id, REL=rel)
        #print(qry)
        with gdbdr.session() as session:
            for idx, rec in enumerate(session.run(qry).records()):
                # print(idx, rec['dst'])
                node = Neo4jNode(rec['dst'])
                # print('{IDX} {REL:19} {NODE}'.format(IDX=idx, REL=rel, NODE=node))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
