#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://reactome.org/dev/graph-database/extract-participating-molecules

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
from neo4j import GraphDatabase
from reactomeneo4j.code.session import Session


def prt_pathways():
    """Print pathway information for a species."""
    assert len(sys.argv) != 1, "NO NEO4J PASSWORD PROVIDED"
    password = sys.argv[1]
    species = 'Homo sapiens'
    gdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdr.session() as session:
        ses = Session(session)
        _run(ses, species)

def _run(session, species):
    """Print pathway information for a species."""
    qry = 'MATCH (pw:Pathway{{speciesName:"{species}"}}) RETURN pw'.format(species=species)
    res = session.run(qry)
    flds = cx.Counter()
    idx = 0
    for idx, rec in enumerate(res.records(), 1):
        pw_flds = rec['pw'].keys()
        for fld in pw_flds:
            flds[fld] += 1
        kws_pw = {f:rec['pw'].get(f) for f in rec['pw']}  # Pathway
    assert flds['stId'] == idx, "EXP({E}) ACT({A})".format(E=idx, A=flds['stId'])
    #_prt_flds_seen(flds)
    # print(kws)
    # prt.write("\n{IDX}) {releaseDate} {stId:13} {displayName}\n".format(IDX=idx, **kws))

def _prt_flds_seen(fld2cnt):
    """Report the fields found and their counts."""
    # Pathways for Homo sapiens
    #     2222 schemaClass
    #     2222 isInDisease
    #     2222 releaseDate
    #     2222 displayName
    #     2222 stId
    #     2222 speciesName
    #     2222 stIdVersion
    #     2222 dbId
    #     2222 name
    #     2222 hasDiagram
    #     2222 isInferred
    #     1648 oldStId
    #      892 diagramHeight
    #      892 diagramWidth
    #      404 doi
    #       53 releaseStatus
    #       16 definition
    for key, val in fld2cnt.most_common():
        print("{CNT:4} {FLD}".format(CNT=val, FLD=key))

# KEY-VAL pw <Node id=2458192 labels={'DatabaseObject', 'Event', 'Pathway'}
# properties={
#   'schemaClass': 'Pathway'
#   'speciesName': 'Homo sapiens'
#   'oldStId': 'REACT_163813'
#   'isInDisease': False,
#   'releaseDate': '2013-06-11'
#   'displayName': 'Scavenging by Class F Receptors'
#   'stIdVersion': 'R-HSA-3000484.1'
#   'dbId': 3000484
#   'name': ['Scavenging by Class F Receptors']
#   'stId': 'R-HSA-3000484',
#   'hasDiagram': False, 'isInferred': False}>


if __name__ == '__main__':
    prt_pathways()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
