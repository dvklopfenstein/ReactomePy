#!/usr/bin/env python
"""Retrieving the reactions for a given pathway."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#retrieving-reactions

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

# pylint: disable=line-too-long
#### def main(password, schemaname='Complex', stid='R-HSA-8863895'):
def main(password, prt=sys.stdout):
    """Retrieving the reactions for a given pathway."""

    # To get ALL the reactions contained either directly in it or as part of any
    # of its subpathways, the query has to recursively traverse the "hasEvent" slot:

    # All reactions for the pathway with stable identifier R-HSA-983169
    qry = ('MATCH (p:Pathway{stId:"R-HSA-983169"})-[:hasEvent*]->(rle:ReactionLikeEvent)'
           'RETURN p.stId AS Pathway, rle.stId AS Reaction, rle.displayName AS ReactionName')

    data = _get_data(qry, password)
    _prt_data(data, prt)

def _prt_data(data, prt):
    """Print the reactions for a given pathway."""
    msg = '{N} reactions in Pathway(R-HSA-983169)'.format(N=len(data))
    prt.write("{MSG}\n\n".format(MSG=msg))
    prt.write('Pathway      Reaction      ReactionName\n')
    prt.write('------------ ------------- ------------\n')
    for dct in sorted(data, key=lambda d: [d['Pathway'], d['Reaction']]):
        prt.write('{Pathway:13} {Reaction:13} {ReactionName}\n'.format(**dct))
    print(msg)

def _get_data(qry, password):
    """Run query. Collect data."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        return [rec.data() for rec in session.run(qry).records()]


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
