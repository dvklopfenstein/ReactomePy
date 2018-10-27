#!/usr/bin/env python
"""Print publications associated with Pathway(s) provided by user."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.publication import Publication


def main():
    """Print Reactome data schema."""
    obj = Publication('hsa')


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
