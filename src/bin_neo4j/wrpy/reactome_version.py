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

from neo4j import GraphDatabase
from reactomeneo4j.code.utils import get_args
from reactomeneo4j.code.wrpy.wrpy_general import WrPy
from reactomeneo4j.code.query.functions import get_version


def main():
    """Print all disease in Reactome."""
    dct = get_args(__doc__, ['neo4j_password', 'neo4j_username', 'url'])
    gdbdr = GraphDatabase.driver(dct['url'], auth=(dct['neo4j_username'], dct['neo4j_password']))
    obj = WrPy()
    obj.wrpy_version('src/reactomeneo4j/data/reactome_version.py', get_version(gdbdr))


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
