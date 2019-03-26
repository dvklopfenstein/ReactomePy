#!/usr/bin/env python
"""Test command-line-interface for user runtime args.

Usage: test_args.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomepy.code.utils import get_args


def test_args():
    """Test command-line-interface for user runtime args."""
    fields = ['neo4j_password', 'neo4j_username', 'url']
    fname = __file__

    # TEST: $ src/test/test_args.py password
    sys.argv = [fname, 'password']
    ntargs = get_args(__doc__, fields)
    assert dict(ntargs._asdict()) == {
        'neo4j_password': 'password', 'neo4j_username': 'neo4j', 'url': 'bolt://localhost:7687'}

    # TEST: $ src/test/test_args.py password -u usr
    sys.argv = [fname, 'password', '-u', 'usr']
    ntargs = get_args(__doc__, fields)
    assert dict(ntargs._asdict()) == {
        'neo4j_password': 'password', 'neo4j_username': 'usr', 'url': 'bolt://localhost:7687'}

    # TEST: $ src/test/test_args.py password --url bolt://localhost:8888
    sys.argv = [fname, 'password', '--url', 'bolt://localhost:8888']
    ntargs = get_args(__doc__, fields)
    assert dict(ntargs._asdict()) == {
        'neo4j_password': 'password', 'neo4j_username': 'neo4j', 'url': 'bolt://localhost:8888'}

    # TEST: $ src/test/test_args.py password --url bolt://localhost:8888 -u usr
    sys.argv = [fname, 'password', '--url', 'bolt://localhost:8888', '-u', 'usr']
    ntargs = get_args(__doc__, fields)
    assert dict(ntargs._asdict()) == {
        'neo4j_password': 'password', 'neo4j_username': 'usr', 'url': 'bolt://localhost:8888'}


if __name__ == '__main__':
    test_args()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
