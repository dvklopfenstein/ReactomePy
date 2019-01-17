#!/usr/bin/env python
"""Print all disease in Reactome.

Usage: test_args.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.utils import get_gdbdr
from reactomeneo4j.code.wrpy.wrpy_general import WrPy
from reactomeneo4j.code.query.functions import get_version


def main():
    """Print all disease in Reactome."""
    obj = WrPy()
    obj.wrpy_version('src/reactomeneo4j/data/reactome_version.py', get_version(get_gdbdr(__doc__)))


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
