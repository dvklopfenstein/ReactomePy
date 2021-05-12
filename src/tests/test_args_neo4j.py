#!/usr/bin/env python
"""Test command-line-interface for user runtime args.

Usage: test_args.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomepy.code.cli.bin_neo4j import get_argparser


def test_args():
    """Test command-line-interface for user runtime args."""
    parser = get_argparser()

    # TEST: $ src/test/test_args.py password
    assert vars(parser.parse_args(['password',])) == {
        'neo4j_password': 'password', 'neo4j_username': 'neo4j', 'url': 'bolt://localhost:7687'}

    ## TEST: $ src/test/test_args.py password -u usr
    argv = ['password', '-u', 'usr']
    assert vars(parser.parse_args(argv)) == {
        'neo4j_password': 'password', 'neo4j_username': 'usr', 'url': 'bolt://localhost:7687'}

    ## TEST: $ src/test/test_args.py password --url bolt://localhost:8888
    argv = ['password', '--url', 'bolt://localhost:8888']
    assert vars(parser.parse_args(argv)) == {
        'neo4j_password': 'password', 'neo4j_username': 'neo4j', 'url': 'bolt://localhost:8888'}

    ## TEST: $ src/test/test_args.py password --url bolt://localhost:8888 -u usr
    argv = ['password', '--url', 'bolt://localhost:8888', '-u', 'usr']
    assert vars(parser.parse_args(argv)) == {
        'neo4j_password': 'password', 'neo4j_username': 'usr', 'url': 'bolt://localhost:8888'}
    print('TEST PASSED')


if __name__ == '__main__':
    test_args()

