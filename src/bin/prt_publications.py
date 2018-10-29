#!/usr/bin/env python
"""Print publications associated with Pathway(s) provided by user."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.publication import Publication


def main():
    """Print Reactome data schema."""
    obj = Publication('hsa')
    pmids = obj.get_pwys_w_all()
    print('{N} Pathways of {M} have all types of data'.format(N=len(pmids), M=len(obj.pw2nt)))
    obj.prt_pw('R-HSA-202040')


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
