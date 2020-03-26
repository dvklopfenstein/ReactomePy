"""Holds all Reactome data schema and their relationships to one another."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx
#### from reactomepy.code.schema.data_schema import ITEM2CHILDREN
#### from reactomepy.code.schema.node import DataSchemaNode
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
        self._init_ancestors(_names)

    def _init_dcnt(self):
        """Initialize descendant count."""
        id2descendants = get_id2children(self.name2obj.values())
        for id_, descendants in id2descendants.items():
            obj = self.name2obj[id_]
            obj.descendants = descendants
            obj.dcnt = len(descendants)

    def _init_ancestors(self, names):
        """Initialize ancestors count."""
        id2ancestors = get_id2parents(self.name2obj.values())
        for schemaclass, ancestors in id2ancestors.items():
            obj = self.name2obj[schemaclass]
            obj.ancestors = ancestors
        # 
        for schemaclass in names.difference(id2ancestors.keys()):
            obj = self.name2obj[schemaclass]
            obj.ancestors = set()

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

    def _init_name2obj(item2children, child2parents):
        """Create a DataSchemaNode for all schema"""
        names = set(item2children).union(child2parents)
        names.add('DBInfo')
        name2obj = {name:DataSchemaNode(name) for name in names}


# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
