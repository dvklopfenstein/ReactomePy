"""Command line interface to:

Usage: get_relationship_cnts.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import argparse


def get_argparser():
    """Argument parser for scripts in src/bin_neo4j"""
    parser = argparse.ArgumentParser(
        description="Run scripts that access a running neo4j process")
    parser.add_argument(
        'neo4j_password',
        help="Password for Reactome's graph.db running in neo4j")
    parser.add_argument(
        '-u', '--neo4j_username', default='neo4j',
        help='Neo4j Reactome username')
    parser.add_argument(
        '--url', default='bolt://localhost:7687')
    return parser

def get_args():
    """Argument parser for scripts in src/bin_neo4j"""
    return get_argparser().parse_args()


# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
