#!/usr/bin/env python
"""Save all species in Reactome to Python modules.
# TBD: Not complete

Usage: test_args.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from neo4j import GraphDatabase
from reactomepy.code.wrpy.inferredfrom import InferredFrom
from reactomepy.code.cli.bin_neo4j import get_args


def prt_inferredfrom():
    """Print all species in Reactome."""
    args = get_args()
    gdbdr = GraphDatabase.driver(args.url, auth=(args.neo4j_username, args.neo4j_password))
    obj = InferredFrom(gdbdr)
    obj.wrpy_info('src/reactomepy/data/species.py')


if __name__ == '__main__':
    prt_inferredfrom()

# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
