"""Processes ancestors and descnedants (like go_tasks)."""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


def get_id2parents(objs):
    """Get all parent item IDs for each item in dict keys."""
    id2parents = {}
    for obj in objs:
        _get_id2parents(id2parents, obj.dbid, obj)
    return id2parents

def get_id2children(objs):
    """Get all parent item IDs for each item in dict keys."""
    id2children = {}
    for obj in objs:
        _get_id2children(id2children, obj.dbid, obj)
    return id2children

# ------------------------------------------------------------------------------------
def _get_id2parents(id2parents, dbid, item_obj):
    """Add the parent item IDs for one item object and their parents."""
    if dbid in id2parents:
        return id2parents[dbid]
    parent_ids = set()
    for parent_obj in item_obj.parents:
        parent_id = parent_obj.dbid
        parent_ids.add(parent_id)
        parent_ids |= _get_id2parents(id2parents, parent_id, parent_obj)
    id2parents[dbid] = parent_ids
    return parent_ids

def _get_id2children(id2children, dbid, item_obj):
    """Add the child item IDs for one item object and their children."""
    if dbid in id2children:
        return id2children[dbid]
    child_ids = set()
    for child_obj in item_obj.children:
        child_id = child_obj.dbid
        child_ids.add(child_id)
        child_ids |= _get_id2children(id2children, child_id, child_obj)
    id2children[dbid] = child_ids
    return child_ids


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
