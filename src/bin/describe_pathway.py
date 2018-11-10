#!/usr/bin/env python
"""Describe the Pathway(s) requested by user."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
from reactomeneo4j.code.wrpy.utils import REPO
from goatools.obo_parser import GODag
from goatools.base import get_godag
from goatools.base import dnld_gaf
from goatools.associations import read_gaf
from goatools.semantic import TermCounts
from goatools.gosubdag.gosubdag import GoSubDag
from goatools.gosubdag.plot.gosubdag_plot import GoSubDagPlot
from reactomeneo4j.code.describe_pathway import DescribePathway


def main(obo='go-basic.obo', gaf='goa_human.gaf'):
    """Describe the Pathway(s) requested by user."""
    gosubdag = _get_gosubdag(obo, gaf)
    obj = DescribePathway('hsa', gosubdag)
    pmids = obj.get_pwys_w_all()
    # return
    print('{N} Pathways of {M} have all types of data'.format(N=len(pmids), M=len(obj.pw2nt)))
    obj.prt_pw('R-HSA-202040')
    obj.prt_pw('R-HSA-168898')   # Multiple Species
    obj.prt_pw('R-HSA-5678420')  # Multiple diseases
    obj.prt_pw('R-HSA-15869')    # Biological Pathways
    obj.prt_pw('R-HSA-71288')    # Cellular Components
    # print(gosubdag.prt_attr)
    # print(gosubdag.prt_attr['fmt'])

def _get_gosubdag(obo, gaf):
    """Return a gosubdag object with human annotations."""
    # Load GO DAG with optional 'definition' field values
    godag = GODag(os.path.join(REPO, obo), ['defn'])
    # Annotations
    #   % wget http://geneontology.org/gene-associations/goa_human.gaf.gz
    #   % gunzip goa_human.gaf.gz
    gene2gos = read_gaf(gaf)
    tcntobj = TermCounts(godag, gene2gos)
    return GoSubDag(None, godag, tcntobj=tcntobj, prt=sys.stdout)


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
