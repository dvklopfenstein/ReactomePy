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

    def get_ids_lte(self, name):
        """Return a set containing current data schema name ID and its descendants."""
        names = set(self.name2obj[name].descendants)
        names.add(name)
        return names

    def get_obj(self, name):
        """Get data schema name object."""
        return self.name2obj[name]

    def prt_data_schema(self, root_schema='DatabaseObject', prt=sys.stdout):
        """Print Reactome Graph Database data schema hierarchy."""
        cfg = {'name2prtfmt':{'ITEM':'({DCNT})'}}
        ntobj = namedtuple('ntprt', 'name dcnt')
        name2nt = {nm:ntobj(dcnt=o.dcnt, name=nm) for nm, o in self.name2obj.items()}
        name2prtfmt = {'ITEM':'(dcnt={dcnt})', 'ID':'{name}'}
        wri = WrHier(self.name2obj, id2nt=name2nt, name2prtfmt=name2prtfmt, id_len=0)
        wri.prt_hier_down_id(root_schema, prt)  # Root schema

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
