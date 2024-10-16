#!/usr/bin/env python
"""Save all species in Reactome to Python modules.

Usage: test_args.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.wrpy.species import Species
from reactomepy.code.utils import get_gdbdr


def prt_species():
    """Print all species in Reactome."""
    obj = Species(get_gdbdr())
    obj.wrpy_info('src/reactomepy/data/species.py')
    obj.wrpy_common_names('src/reactomepy/data/species_commonnames.py')


if __name__ == '__main__':
    prt_species()

# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
