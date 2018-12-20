"""Neo4jNode built in steps using groups of dbIds, avoiding duplicate queries."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
from collections import defaultdict
from reactomeneo4j.code.node.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR as S2C


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Neo4jNodeBasic():
    """Neo4jNode built in steps using groups of dbIds, avoiding duplicate queries."""

    patfmt = '{dbId} {schemaClass}'

    def __init__(self, dbid, schemaclass):
        self.dbid = dbid
        self.sch = schemaclass
        self.objsch = self._init_objsch()    # derived from DatabaseObject
        self.dct = {}
        self.relationship = defaultdict(set)

    def set_dict(self, neo4jnode):
        """Extract parameter values from a neo4j.Node."""
        self.dct = self.objsch.get_dict(neo4jnode)

    def set_rel(self, reltype, dst_dbid):
        """Add relationship to dbId."""
        self.relationship[reltype].add(dst_dbid)


    #### def set_nt(self, neo4jnode, rel2nodes):
    ####     """Fill in data nt w/data from relationships, if provided."""
    ####     if rel2nodes:
    ####         k2v = self.objsch.get_dict(neo4jnode)
    ####         if 'abc' in k2v and 'species' in rel2nodes:
    ####             k2v['abc'] = self._get_abc(k2v['abc'], rel2nodes['species'])
    ####         return self.objsch.ntobj(**k2v)
    ####     return self.objsch.get_nt(neo4jnode)

    def __str__(self):
        # Parameters on all Nodes
        msg = ['{dbId} {schemaClass}'.format(dbId=self.dbid, schemaClass=self.sch)]
        if self.dct:
            # Required Parameters on this Node
            msg[0] += ' ' + self.dct['displayName']
            excl = {'dbId', 'schemaClass', 'displayName', 'optional'}
            dctlst = ['{}({})'.format(k, v) for k, v in sorted(self.dct.items()) if k not in excl]
            if dctlst:
                msg.append(' '.join(dctlst))
            # Optional Parameters on this Node
            if 'optional' in self.dct:
                optlst = ['{}({})'.format(k, v) for k, v in sorted(self.dct['optional'].items())]
                msg.append(' '.join(optlst))
        return '\n'.join(msg)

    #### def prt_verbose(self, prt):
    ####     """Return a string with all details of the Node and its relationships."""
    ####     prt.write('\n{NT}\n'.format(NT=self.ntp))
    ####     prt.write('\n{O}\n'.format(O=self))
    ####     for rel, nodes in self.rel2nodes.items():
    ####         for dst in nodes:
    ####             prt.write('DDDD {REL:20} {D}\n'.format(REL=rel, D=dst))
    ####             if rel in set(['referenceEntity']):
    ####                 prt.write('---- {NT}\n'.format(NT=dst.ntp))

    def _init_objsch(self):
        """Given schemaClass, create data framework object."""
        assert self.sch in S2C, '**FATAL: BAD schemaClass({S})'.format(S=self.sch)
        return S2C[self.sch]

    #### def _get_abc(self, abc_param, species_nodes, objsch):
    ####     """Return a value for abc."""
    ####     abc_rel = '-'.join(objsch.species2nt.get(o.ntp.displayName, '???').abbreviation for o in species_nodes)
    ####     # if abc_param == '...' or abc_param == abc_rel:
    ####     if abc_param in {'...', abc_rel}:
    ####         return abc_rel
    ####     print('**ERROR: {SCH}{{dbId:{DBID}}} PARAMETER({P}) != species RELATIONSHIP({R})'.format(
    ####         DBID=self.dbid, SCH=self.sch, P=abc_param, R=abc_rel))
    ####     return 'XXX'

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
