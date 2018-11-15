"""Functions to write Reactome data extracted from Neo4j to Python."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import collections as cx


def chk_unique(dcts, fld2expunique):
    """Ex: Expect that taxIds and displayNames are unique while abbreviation is not."""
    num_dcts = len(dcts)
    fld2sets = cx.OrderedDict([(f, set()) for f in fld2expunique])
    for dct in dcts:
        for fld in fld2expunique:
            fld2sets[fld].add(dct[fld])
    for fld, items in fld2sets.items():
        actually_unique = len(items) == num_dcts
        assert actually_unique == fld2expunique[fld]


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
