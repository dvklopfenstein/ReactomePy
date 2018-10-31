#!/usr/bin/env python
"""Describe the Pathway(s) requested by user."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.describe_pathway import DescribePathway


def main():
    """Describe the Pathway(s) requested by user."""
    obj = DescribePathway('hsa')
    pmids = obj.get_pwys_w_all()
    print('{N} Pathways of {M} have all types of data'.format(N=len(pmids), M=len(obj.pw2nt)))
    obj.prt_pw('R-HSA-202040')
    obj.prt_pw('R-HSA-168898')


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
