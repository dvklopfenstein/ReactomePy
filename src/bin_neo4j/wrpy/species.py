#!/usr/bin/env python
"""Save all species in Reactome to Python modules."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomeneo4j.code.wrpy.species import Species


def prt_species(password):
    """Print all species in Reactome."""
    obj = Species(password)
    obj.wrpy_info('src/reactomeneo4j/data/species.py')
    obj.wrpy_common_names('src/reactomeneo4j/data/species_commonnames.py')


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    prt_species(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
