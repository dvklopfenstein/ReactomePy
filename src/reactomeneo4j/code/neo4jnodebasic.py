"""Neo4jNode built in steps using groups of dbIds, avoiding duplicate queries."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
from collections import defaultdict
from reactomeneo4j.code.node.schemaclass_factory import new_inst


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Neo4jNodeBasic():
    """Neo4jNode built in steps using groups of dbIds, avoiding duplicate queries."""

    def __init__(self, dbid, schemaclass):
        self.dbid = dbid
        #### self.sch = schemaclass
        self.objsch = new_inst(schemaclass, dbid)    # derived from DatabaseObject
        self.prtfmt = self.objsch.prtfmt
        #### self.dct = {}  # TBD: Make this ntp. Store init dct in ntp. dict->nt
        self.ntp = None
        self.children = set()
        self.parents = set()
        self.relationship = defaultdict(set)
        self.depth = None
        self.dcnt = None
        self.descendants = set()
        self.ancestors = set()

    def __str__(self):
        # Parameters on all Nodes
        msg = ['{dbId} {schemaClass}'.format(dbId=self.dbid, schemaClass=self.objsch.name)]
        # print('FMTPAT', self.objsch.prtfmt)
        # print('NT', self.ntp._asdict())
        msg.append('NT: {NT}'.format(NT=self.objsch.prtfmt.format(**self.ntp._asdict())))
        msg.append('NT: {NT}'.format(NT=self.ntp))
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

    #### @staticmethod
    #### def _init_objsch(sch, dbid):
    ####     """Given schemaClass, create data framework object."""
    ####     assert sch in S2C, '**FATAL: BAD schemaClass({S})'.format(S=sch)
    ####     return S2C[sch]


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
