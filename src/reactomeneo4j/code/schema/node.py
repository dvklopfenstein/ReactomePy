"""Holds information for one data schema item."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
#### import collections as cx
from PyBiocode.graph.node import Node
#### from dvkbiodnld.data.hgnc.famid2rootsym import FAMILYID2ROOTSYM
#### from dvkbiodnld.data.hgnc.famid2pubmedids import FAMILYID2PUBMEDIDS
#### from dvkbiodnld.data.hgnc.famid2desc import FAMILYID2NTDESC


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class DataSchemaNode(Node):
    """Holds information for one data schema item."""

    prtfmt = "D-{DEPTH} {DCNT:2}=dcnt {NAME}"
    #### ntobj = cx.namedtuple("ntgf", "FAMILY_ID NAME ROOTSYM DEPTH DCNT")

    def __init__(self, name):
        super(DataSchemaNode, self).__init__(name, None)
    ####  self.rootsyms = FAMILYID2ROOTSYM.get(family_id, set())
    ####  self.pubmedids = FAMILYID2PUBMEDIDS.get(family_id, set())
    ####  self.ntdesc = FAMILYID2NTDESC.get(family_id)

    #### def get_nt(self):
    ####   """Get namedtuple containing gene family information. (Used for printing)."""
    ####   return self.ntobj(
    ####     FAMILY_ID=self.item_id,
    ####     NAME=self.name,
    ####     ROOTSYM=self.rootsym,
    ####     DEPTH=self.depth,
    ####     DCNT=self.dcnt,
    ####   )

    #### def get_all_parents(self):
    ####   """Return all parent GO IDs."""
    ####   all_parents_ids = set()
    ####   for parent in self.parents:
    ####     all_parents_ids.add(parent.item_id)
    ####     all_parents_ids |= parent.get_all_parents()
    ####   return all_parents_ids

    #### def get_all_children(self):
    ####   """Return all children GO IDs."""
    ####   all_children_ids = set()
    ####   for parent in self.children:
    ####     all_children_ids.add(parent.item_id)
    ####     all_children_ids |= parent.get_all_children()
    ####   return all_children_ids

    def __str__(self):
        return self.prtfmt.format(
            NAME=self.item_id,
            DEPTH=self.depth,
            DCNT=self.dcnt)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
