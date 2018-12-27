"""Holds information for one data schema item."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
from collections import defaultdict
from reactomeneo4j.code.node.schemaclass_factory import SCHEMACLASS2OBJ


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Neo4jNode():
    """Holds data extracted from Neo4j."""


    def __init__(self, neo4jnode, **kws):  # gdbdr=None, prtfmt=None):
        # kws: gdbdr prtfmt rel_excl
        _ini = _Init(neo4jnode['dbId'], neo4jnode['schemaClass'], **kws)
        self.objsch = SCHEMACLASS2OBJ[neo4jnode['schemaClass']]  # derived from DatabaseObject
        self.rel2nodes = _ini.get_rel2nodes()
        self.ntp = _ini.get_nt(neo4jnode, self.rel2nodes, self.objsch)
        self.prtfmt = kws['prtfmt'] if 'prtfmt' in kws else self.objsch.prtfmt

    def __str__(self):
        opt = self.objsch.get_optstr(self.ntp.optional)
        return self.prtfmt.format(**self.ntp._asdict(), **opt)

    def prt_verbose(self, prt):
        """Return a string with all details of the Node and its relationships."""
        prt.write('\n{NT}\n'.format(NT=self.ntp))
        prt.write('\n{O}\n'.format(O=self))
        for rel, nodes in self.rel2nodes.items():
            for dst in nodes:
                prt.write('DDDD {REL:20} {D}\n'.format(REL=rel, D=dst))
                if rel in set(['referenceEntity']):
                    prt.write('---- {NT}\n'.format(NT=dst.ntp))

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


class _Init():
    """Initialize a Python Node from a neo4j.node."""

    # Query to determine Nodes in this item's relationships
    qrypat = 'MATCH (src:DatabaseObject{{dbId:{DBID}}})-[rel]->(dst) RETURN src, rel, dst'

    def __init__(self, dbid, schemaclass, **kws):
        self.item_id = dbid
        self.sch = schemaclass
        self.kws = kws  # kws: gdbdr rel_excl
        self.rel_excl = kws['rel_excl'] if 'rel_excl' in kws else {'inferredTo'}

    def get_nt(self, neo4jnode, rel2nodes, objsch):
        """Fill in data nt w/data from relationships, if provided."""
        if rel2nodes:
            k2v = objsch.get_dict(neo4jnode)
            if 'abc' in k2v and 'species' in rel2nodes:
                k2v['abc'] = self._get_abc(k2v['abc'], rel2nodes['species'], objsch)
            return objsch.ntobj(**k2v)
        return objsch.get_nt(neo4jnode)

    def get_rel2nodes(self):
        """Query for objects at the end of this Node's relationships."""
        if 'gdbdr' in self.kws:
            rel2nodes = defaultdict(list)
            qry = self.qrypat.format(DBID=self.item_id)
            #print('\n{Q}'.format(Q=qry))
            with self.kws['gdbdr'].session() as session:
                for rec in session.run(qry).records():
                    rel = rec['rel'].type
                    if rel not in self.rel_excl:
                        #print('{I} {R:19} {NOD}'.format(I=idx, R=rec['rel'].type, NOD=rec['dst']))
                        rel2nodes[rel].append(Neo4jNode(rec['dst']))
            return {rel:o for rel, o in rel2nodes.items()}
        return {}

    def _get_abc(self, abc_param, species_nodes, objsch):
        """Return a value for abc."""
        abc_rel = '-'.join(objsch.species2nt.get(o.ntp.displayName, '???').abbreviation for o in species_nodes)
        # if abc_param == '...' or abc_param == abc_rel:
        if abc_param in {'...', abc_rel}:
            return abc_rel
        print('**ERROR: {SCH}{{dbId:{DBID}}} PARAMETER({P}) != species RELATIONSHIP({R})'.format(
            DBID=self.item_id, SCH=self.sch, P=abc_param, R=abc_rel))
        return 'XXX'


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
