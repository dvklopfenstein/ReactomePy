"""Holds all data schema items and their relationships to one another."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
# import os
from collections import namedtuple
## from dvkbiodnld.data.hgnc.famid2name import FAMILYID2NAME
from reactomeneo4j.code.schema.hier_init import Init
from PyBiocode.graph.hier_wr import WrHier


class DataSchemaHier(object):
    """Hold all data schema name hierarchies."""

    def __init__(self):
        self.name2obj = Init().name2obj

    def prt_data_schema_all(self, prt, **kws):
        """Print all data schema in a readable format."""
        prt.write('TOP DATA SCHEMA: DatabaseObject\n')
        prt.write('------------------------------------\n')
        self.prt_data_schema('DatabaseObject', prt, max_indent=2, **kws)
        # Get Data Schema depth-01 nodes which have descendents
        objs_d1_all = [o for o in self.name2obj.values() if o.depth == 1 and o.dcnt != 0]
        objs_d1_sel = [o for o in sorted(objs_d1_all, key=self.sortby)]
        # Print hierarchies for depth-01 data schema
        prt.write('\nDEPTH-01 DATA SCHEMA: DatabaseObject\n')
        prt.write('------------------------------------\n')
        for node_obj in objs_d1_sel:
            prt.write('\n')
            self.prt_data_schema(node_obj.item_id, prt, **kws)

    def get_ids_lte(self, name):
        """Return a set containing current data schema name ID and its descendants."""
        names = set(self.name2obj[name].descendants)
        names.add(name)
        return names

    def get_ids_lte_all(self, names):
        """Return a set containing current data schema names ID and their descendants."""
        names_all = set()
        for name in names:
            names_all.update(self.name2obj[name].descendants)
        names_all.update(names)
        return names_all

    def get_ids_gte_all(self, names):
        """Return a set containing current data schema names ID and their ancestors."""
        names_all = set()
        for name in names:
            names_all.update(self.name2obj[name].ancestors)
        names_all.update(names)
        return names_all

    def get_ids_gte(self, name):
        """Return a set containing current data schema name ID and its ancestors."""
        names = set(self.name2obj[name].descendants)
        names.add(name)
        return names

    def get_ancestor_d1(self, schema):
        """Get the ancestor at the depth-01 for given schema."""
        return self.get_ancestor_dn(schema, 1)

    def get_ancestor_dn(self, schema, depth):
        """Get the ancestor at the requested depth for given schema."""
        obj = self.name2obj[schema]
        names = set(a for a in obj.ancestors if self.name2obj[a].depth == depth)
        num_names = len(names)
        assert num_names <= 1
        if num_names == 1:
            return next(iter(names))
        elif obj.depth == depth:
            return schema
        return ''

    def get_obj(self, name):
        """Get data schema name object."""
        return self.name2obj[name]

    def prt_data_schema(self, root_schema='DatabaseObject', prt=sys.stdout, **kws):
        """Print Reactome Graph Database data schema hierarchy."""
        # cfg = {'name2prtfmt':{'ITEM':'({DCNT})'}}
        ntobj = namedtuple('ntprt', 'name dcnt')
        name2nt = {nm:ntobj(dcnt=o.dcnt, name=nm) for nm, o in self.name2obj.items()}
        name2prtfmt = {'ITEM':'(dcnt={dcnt})', 'ID':'{name}'}
        wri = WrHier(self.name2obj,
                     id2nt=name2nt, name2prtfmt=name2prtfmt, id_len=0, sortby=self.sortby, **kws)
        wri.prt_hier_down_id(root_schema, prt)  # Root schema

    @staticmethod
    def sortby(node_obj):
        """Sort by Data Schema item ID (which is also the name)."""
        return [-1*node_obj.dcnt, node_obj.item_id]

  ## def get_root_objs(self, gene_family_nodes):
  ##   """Get the root (depth=0) data schema name for each family in the list."""
  ##   ids_up = set()
  ##   for obj in gene_family_nodes:
  ##     ids_up.add(obj.item_id)
  ##     ids_up.update(obj.ancestors)  # Add ancestor IDs
  ##   objs_up = set(self.name2obj[i] for i in ids_up)
  ##   return set(o for o in objs_up if o.depth==0)

  ## @staticmethod
  ## def get_bset(avals, a2bset):
  ##   """Get bvals associated with given avals."""
  ##   bset = set()
  ##   for aval in avals:
  ##     if aval in a2bset:
  ##       bset.update(a2bset[aval])
  ##   return bset

  ## @staticmethod
  ## def get_b2aset(a2bset):
  ##   """Get name2geneid."""
  ##   b2aset = cx.defaultdict(set)
  ##   for aval, bset in a2bset.items():
  ##     for bval in bset:
  ##       b2aset[bval].add(aval)
  ##   return {b:aset for b, aset in b2aset.items()}

  ## @staticmethod
  ## def chk_name_set(name_set):
  ##   """Check that the data schema name IDs exist."""
  ##   not_found = name_set.difference(set(FAMILYID2NAME.keys()))
  ##   if not not_found:
  ##     return name_set
  ##   for missing_id in not_found:
  ##     print("**WARNING: {ID:4} NOT FOUND IN GENE FAMILIES".format(ID=missing_id))
  ##   return name_set.difference(not_found)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
