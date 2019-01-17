#!/usr/bin/env python
"""Save all species in Reactome to Python modules.

Usage: test_args.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase
from reactomeneo4j.code.wrpy.species import Species
from reactomeneo4j.code.utils import get_args


def prt_species():
    """Print all species in Reactome."""
    dct = get_args(__doc__, ['neo4j_password', 'neo4j_username', 'url'])
    gdbdr = GraphDatabase.driver(dct['url'], auth=(dct['neo4j_username'], dct['neo4j_password']))
    obj = Species(gdbdr)
    obj.wrpy_info('src/reactomeneo4j/data/species.py')
    obj.wrpy_common_names('src/reactomeneo4j/data/species_commonnames.py')


if __name__ == '__main__':
    prt_species()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
