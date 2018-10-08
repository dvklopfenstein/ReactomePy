#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://reactome.org/dev/graph-database/extract-participating-molecules

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase
from reactomeneo4j.code.session import Session


def prt_pathways():
    """Print pathway information for a species."""
    assert len(sys.argv) != 1, "NO NEO4J PASSWORD PROVIDED"
    password = sys.argv[1]
    species = 'Homo sapiens'
    gdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    prt = sys.stdout
    with gdr.session() as session:
        ses = Session(session)
        _run(ses, species, prt)

def _run(session, species, prt=sys.stdout):
    """Print pathway information for a species."""
    qry = 'MATCH (pw:Pathway{{speciesName:"{species}"}}) RETURN pw'.format(species=species)
    res = session.run(qry)
    pw_flds = set(['releaseDate', 'stId', 'displayName'])
    for idx, rec in enumerate(res.records()):
        node = rec['pw']
        kws = {f:node.get(f) for f in pw_flds}
        prt.write("{IDX}) {releaseDate} {stId:13} {displayName}\n".format(IDX=idx, **kws))


# KEY-VAL pw          <Node id=2458192 labels={'DatabaseObject', 'Event', 'Pathway'} properties={'schemaClass': 'Pathway', 'speciesName': 'Homo sapiens', 'oldStId': 'REACT_163813', 'isInDisease': False,
# 'releaseDate': '2013-06-11', 'displayName': 'Scavenging by Class F Receptors', 'stIdVersion': 'R-HSA-3000484.1', 'dbId': 3000484, 'name': ['Scavenging by Class F Receptors'], 'stId': 'R-HSA-3000484',
# 'hasDiagram': False, 'isInferred': False}>

if __name__ == '__main__':
    prt_pathways()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
