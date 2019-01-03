"""Holds all Reactome data schema and their relationships to one another."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx
#### from reactomeneo4j.code.schema.data_schema import ITEM2CHILDREN
#### from dvkbiodnld.data.hgnc.famid2name import FAMILYID2NAME
#### from reactomeneo4j.code.schema.node import DataSchemaNode
from goatools.godag.go_tasks import get_id2children
from goatools.godag.go_tasks import get_id2parents


# pylint: disable=too-few-public-methods
class Init(object):
    """Initializes Reactome data schema objects."""

    def __init__(self, item2children, DataSchemaNode):
        _child2parents = self._get_child2parents(item2children)
        _names = set(item2children).union(_child2parents)
        self.name2obj = {name:DataSchemaNode(name) for name in _names}
        self._init_parents_children(_child2parents, item2children)
        self._init_depth()
        self._init_dcnt()
        self._init_ancestors()

    def _init_dcnt(self):
        """Initialize descendant count."""
        id2descendants = get_id2children(self.name2obj.values())
        for id_, descendants in id2descendants.items():
            obj = self.name2obj[id_]
            obj.descendants = descendants
            obj.dcnt = len(descendants)

    def _init_ancestors(self):
        """Initialize ancestors count."""
        id2ancestors = get_id2parents(self.name2obj.values())
        for id_, ancestors in id2ancestors.items():
            obj = self.name2obj[id_]
            obj.ancestors = ancestors

    def _init_depth(self):
        """Set depth for a Reactome data schema object."""
        # Local function for finding depth
        def _init_depth_local(rec):
            """Recursive depth function"""
            if rec.depth is None:
                if rec.parents:
                    rec.depth = max(_init_depth_local(rec) for rec in rec.parents) + 1
                else:
                    rec.depth = 0
            return rec.depth
        # Initialize depth for each DataSchemaNode
        for rec in self.name2obj.values():
            if rec.depth is None:
                _init_depth_local(rec)

    def _init_parents_children(self, child2parents, item2children):
        """Add links to an Reactome data schema's child and parent gene families."""
        for obj in self.name2obj.values():
            name = obj.item_id
            if name in item2children:
                obj.children = set(self.name2obj[i] for i in item2children[name])
            if name in child2parents:
                obj.parents = set(self.name2obj[i] for i in child2parents[name])

    @staticmethod
    def _get_child2parents(item2children):
        """Get child-to-parent relationships for data schema."""
        child2parents = cx.defaultdict(set)
        for parent, children in item2children.items():
            for child in children:
                child2parents[child].add(parent)
        return child2parents


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
