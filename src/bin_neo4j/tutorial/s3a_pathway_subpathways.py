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

    # To find out its subpathways, the slot to query is "hasEvent":
    # Direct subpathways for the pathway with stable identifier R-HSA-983169
    qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent]->(sp:Pathway)'
           'RETURN p.stId AS Pathway, sp.stId AS SubPathway, sp.displayName as DisplayName')
    data = _get_data(qry, password)
    prt.write('\n{N} subpathways directly in Pathway(R-HSA-983169)'.format(N=len(data)))
    _prt_data(data, prt)

    # It is important to note that subpathways might contain other subpathways,
    # so to get ALL the supathways of R-HSA-198933, the query is as follows:
    qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent*]->(sp:Pathway)'
           'RETURN p.stId AS Pathway, sp.stId AS SubPathway, sp.displayName as DisplayName')
    prt.write('\nALL {N} subpathways in Pathway(R-HSA-983169)'.format(N=len(data)))
    data = _get_data(qry, password)
    _prt_data(data, prt)


def _prt_data(data, prt):
    """Print the reactions for a given pathway."""
    prt.write('Pathway      SubPathway     DisplayName\n')
    prt.write('------------ -------------- ------------\n')
    for dct in sorted(data, key=lambda d: [d['Pathway'], d['SubPathway']]):
        prt.write('{Pathway:13} {SubPathway:13} {DisplayName}\n'.format(**dct))

def _get_data(qry, password):
    """Run query. Collect data."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        return [rec.data() for rec in session.run(qry).records()]


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
