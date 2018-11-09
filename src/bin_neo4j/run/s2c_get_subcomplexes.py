#!/usr/bin/env python
"""GET SET AND COMPLEX INSIDE COMPLEX, R-HSA-983126 (returns ~284 entities).
      https://reactome.org/dev/graph-database/extract-participating-molecules
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

# pylint: disable=line-too-long
def main(password, schemaname='Complex', stid='R-HSA-983126', prt=sys.stdout):
    """GET SET AND COMPLEX INSIDE COMPLEX, R-HSA-983126 (returns ~284 entities)."""
    # Run this command in your browser: http://localhost:7474/browser/
    # MATCH (Complex{stId:"R-HSA-983126"})-[:hasComponent|hasMember|hasCandidate*]->(pe:PhysicalEntity) RETURN DISTINCT pe.stId AS component_stId, pe.displayName AS component'

    # Or run the command using Python
    item_id = '{schemaName}{{stId:"{stId}"}}'.format(schemaName=schemaname, stId=stid)
    qry = "".join([
        'MATCH ({ITEM_ID})-'.format(ITEM_ID=item_id),
        '[:hasComponent|hasMember|hasCandidate*]->',
        '(pe:PhysicalEntity) RETURN DISTINCT ',
        'pe.stId AS component_stId, ',
        'pe.displayName AS component'])

    data = _get_data(qry, password)
    _prt_data(item_id, data, prt)

def _prt_data(item_id, data, prt):
    """PRINT SET AND COMPLEX INSIDE COMPLEX, R-HSA-983126 (returns ~284 entities)."""
    prt.write('{ID}: All {N} sets and complexes\n\n'.format(ID=item_id, N=len(data)))
    prt.write('ID            Name\n')
    prt.write('------------  ----------------\n')
    # for dct in sorted(data, key=lambda d: int(d['component_stId'].split('-')[2])):
    for dct in sorted(data, key=lambda d: d['component']):
        prt.write('{component_stId:14} {component}\n'.format(**dct))

def _get_data(qry, password):
    """GET SET AND COMPLEX INSIDE COMPLEX, R-HSA-983126 (returns ~284 entities)."""
    dicts = []
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        for rec in session.run(qry).records():
            dicts.append(rec.data())
    return dicts


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
