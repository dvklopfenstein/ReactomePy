#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://github.com/reactome/graph-core/issues/1

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from importlib import import_module


def prt_pathways():
    """Print pathways and their details for a species."""
    modstr_pwy = 'reactomepy.data.pwy.stid2pwy'
    modstr_img = 'reactomepy.data.pwy.pwy2figs'
    pw2nt = import_module(modstr_pwy).STID2NTPWY
    pws_imgfilename = set(p for p in import_module(modstr_img).PWY2FIGS)
    pws_hasdiag = set(p for p, nt in pw2nt.items() if 'F' in nt.TDFIPBU.upper())
    pws_no_fname = pws_hasdiag.difference(pws_imgfilename)
    print('{N:6,} Pathways Total for human'.format(N=len(pw2nt)))
    print('{N:6,} Pathways hasDiagram=true'.format(N=len(pws_hasdiag)))
    print('{N:6,} Pathways hasDiagram=true and a figure filename'.format(N=len(pws_imgfilename)))
    print('{N:6,} Pathways hasDiagram=true have no "figure" relationship or image filename'.format(
        N=len(pws_no_fname)))
    # Check that all pwys that have figure names also have hasDiagram=true
    # TBD: Use isInferred
    #assert not pws_imgfilename.difference(pws_hasdiag)

if __name__ == '__main__':
    prt_pathways()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
