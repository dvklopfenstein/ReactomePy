#!/usr/bin/env python
"""Retrieving pathways, subpathways, and superpathways."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#retrieving-pathways

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

def main(password, prt=sys.stdout):
    """Retrieving the reactions for a given pathway."""

    # Retrieving the superpathway is as easy as changing the direction of the edge in the query:
    # Direct superpathway for the pathway with stable identifier R-HSA-198933
    qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})<-[:hasEvent]-(sp:Pathway)'
           'RETURN p.stId AS Pathway, sp.stId AS SuperPathway, sp.displayName as DisplayName')
    data = _get_data(qry, password)
    prt.write('\n{N} super-pathways directly above Pathway(R-HSA-983169)\n'.format(N=len(data)))
    _prt_data(data, prt)

    # ALL superpathways for the pathway with stable identifier R-HSA-198933
    qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})<-[:hasEvent*]-(sp:Pathway)'
           'RETURN p.stId AS Pathway, sp.stId AS SuperPathway, sp.displayName as DisplayName')
    data = _get_data(qry, password)
    prt.write('\nALL {N} super-pathways at all levels above Pathway(R-HSA-983169)\n'.format(N=len(data)))
    _prt_data(data, prt)


def _prt_data(data, prt):
    """Print the reactions for a given pathway."""
    prt.write('Pathway      SuperPathway   DisplayName\n')
    prt.write('------------ -------------- ------------\n')
    for dct in sorted(data, key=lambda d: [d['Pathway'], d['SuperPathway']]):
        prt.write('{Pathway:13} {SuperPathway:13} {DisplayName}\n'.format(**dct))

def _get_data(qry, password):
    """Run query. Collect data."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        return [rec.data() for rec in session.run(qry).records()]


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
