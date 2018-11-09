#!/usr/bin/env python
"""GET SET AND COMPLEX INSIDE COMPLEX."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
from neo4j import GraphDatabase

# pylint: disable=line-too-long
def main(password, schemaname='Complex', stid='R-HSA-983126', prt=sys.stdout):
    """GET SET AND COMPLEX INSIDE OF A COMPLEX, R-HSA-983126."""
    item_id = '{schemaName}{{stId:"{stId}"}}'.format(schemaName=schemaname, stId=stid)
    qry = "".join([
        'MATCH (src:{ITEM_ID})-'.format(ITEM_ID=item_id),
        '[rel:hasComponent|hasMember|hasCandidate]->',
        '(pe:PhysicalEntity) RETURN src, rel, pe'])

    data = _get_data(qry, password)
    _prt_data(item_id, data, prt)

def _prt_data(item_id, data, prt):
    """PRINT SET AND COMPLEX INSIDE COMPLEX, R-HSA-983126 (returns ~284 entities)."""
    prt.write('{ID}: All {N} sets and complexes\n\n'.format(ID=item_id, N=len(data)))
    prt.write('ID            Name\n')
    prt.write('------------  ----------------\n')
    for dct in data:
        # print('SRC:', dct['src'])
        print('REL:', dct['rel'])
        print('DST:', dct['pe'])
        print('')
    prt.write('{ID}: All {N} sets and complexes\n\n'.format(ID=item_id, N=len(data)))

def _get_data(qry, password):
    """GET SET AND COMPLEX INSIDE COMPLEX, R-HSA-983126 (returns ~284 entities)."""
    dicts = []
    ntrel = cx.namedtuple("NtRel", "ID TYPE")
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        src = None
        for rec in session.run(qry).records():
            print(rec)
            data = rec.data()
            if src is None:
                src = data['src']
            rel = ntrel(ID=data['rel'].id, TYPE=data['rel'].type)
            dct = {'rel':rel, 'pe':data['pe']['stId']}
            print(dct)
            dicts.append(dct)
    return dicts


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
