#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://github.com/reactome/graph-core/issues/1

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from importlib import import_module


def prt_pathways(abc='hsa'):
    """Print pathways and their details for a species."""
    PMDS = 'reactomeneo4j.data.{ABC}.pathways.pathways'
    IMGS = 'reactomeneo4j.data.{ABC}.pathways.pwy2imgname'
    pw2nt = {nt.stId:nt for nt in import_module(PMDS.format(ABC=abc)).PWYNTS}
    pws_imgfilename = set(p for p in import_module(IMGS.format(ABC=abc)).PW2FIGS)
    pws_hasdiag = set(p for p, nt in pw2nt.items() if 'F' in nt.marks.upper())
    pws_no_fname = pws_hasdiag.difference(pws_imgfilename)
    # Check that all pwys that have figure names also have hasDiagram=true
    assert not pws_imgfilename.difference(pws_hasdiag)
    print('{N:5,} Pathways Total for human'.format(N=len(pw2nt)))
    print('{N:5,} Pathways hasDiagram=true'.format(N=len(pws_hasdiag)))
    print('{N:5,} Pathways hasDiagram=true and a figure filename'.format(N=len(pws_imgfilename)))
    print('{N:5,} Pathways hasDiagram=true have no "figure" relationship or image filename'.format(N=len(pws_no_fname)))

if __name__ == '__main__':
    prt_pathways()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
