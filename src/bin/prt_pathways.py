#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://reactome.org/dev/graph-database/extract-participating-molecules

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
from neo4j import GraphDatabase
import textwrap
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
        _run(ses, species, prt=prt)

def _run(session, species, linelen=120, prt=sys.stdout):
    """Print pathway information for a species."""
    field = 'hasDiagram'
    qry = 'MATCH (pw:Pathway{{speciesName:"{species}"}})-[:summation]->(s:Summation) RETURN pw, s'.format(species=species)
    res = session.run(qry)
    flds = cx.Counter()
    cnt = 0
    for idx, rec in enumerate(res.records()):
        pw_flds = rec['pw'].keys()
        for fld in pw_flds:
            flds[fld] += 1
        _prt_pw(rec, idx, prt, linelen)
    #_prt_rel(rec['pw'], session)
    #_prt_flds_seen(flds)
    # print(kws)
    # prt.write("\n{IDX}) {releaseDate} {stId:13} {displayName}\n".format(IDX=idx, **kws))
    qry = 'MATCH (pw:Pathway{stId:"R-HSA-3000480"})-[:summation]->(s:Summation) RETURN pw, s'
    res = session.run(qry)
    for idx, rec in enumerate(res.records()):
        print(rec)
        pwy = rec['pw']
        stmt = rec['s']
    print("{N} {FLD} FIELDS FOUND".format(N=cnt, FLD=field))

def _prt_rel(node, session):
    """Print relationships."""
    # Pathway relationships for Homo sapiens
    #      11 hasEvent
    #       9 inferredTo
    #       5 literatureReference
    #       3 compartment
    #       2 authored
    #       1 modified
    #       1 created
    #       1 summation
    #       1 species
    #       1 reviewed
    #       1 goBiologicalProcess
    #       1 edited
    session.prt_relationships(session.get_str_node(node))

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

def _prt_pw(rec, idx, prt, linelen=120):
    """Print field."""
    kws_pw = {f:rec['pw'].get(f) for f in rec['pw']}  # Pathway
    kws_su = {f:rec['s'].get(f) for f in rec['s']}    # Summation
    prt.write("\n{IDX}) {releaseDate} {stId:13} {displayName}\n".format(IDX=idx, **kws_pw))
    prt.write("{SUMMARY}\n".format(
        SUMMARY="\n".join(textwrap.wrap(kws_su['text'], linelen))))
    #prt.write("{VAL}\n".format(VAL=kws[fld]))  # on Event


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
