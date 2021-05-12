#!/usr/bin/env python
"""Print all disease in Reactome.

Usage: test_args.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.utils import get_gdbdr
from reactomepy.code.wrpy.utils import prt_docstr_module
from reactomepy.code.wrpy.utils import prt_copyright_comment
from reactomepy.code.query.functions import get_version


def main():
    """Print Reactome version in downloaded DAG."""
    fout_py = 'src/reactomepy/data/reactome_version.py'
    with open(fout_py, 'w') as prt:
        prt_docstr_module('Reactome version in DAG', prt)
        # CYPHER: MATCH (v:DBInfo) RETURN v
        version = get_version(get_gdbdr())
        prt.write('VERSION = {V}\n'.format(V=version))
        prt_copyright_comment(prt)
        print('  Version {V} WROTE: {PY}\n'.format(PY=fout_py, V=version))
    #obj.wrpy_version('src/reactomepy/data/reactome_version.py', get_version(get_gdbdr()))


if __name__ == '__main__':
    main()

# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
