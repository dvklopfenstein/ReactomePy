#!/usr/bin/env python
"""Print all ReferenceDatabase in Reactome.

Usage: referencedatabase.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.wrpy.referencedatabase import ReferenceDatabases
from reactomepy.code.utils import get_gdbdr

def prt_referencedatabase():
    """Print all ReferenceDatabase in Reactome."""
    fout_referencedatabase_py = 'src/reactomeneo4j/data/referencedatabase2nt.py'

    obj = ReferenceDatabases(get_gdbdr(__doc__))
    obj.wrpy_referencedatabase_nts(fout_referencedatabase_py)


if __name__ == '__main__':
    prt_referencedatabase()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
