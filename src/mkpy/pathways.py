#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://reactome.org/dev/graph-database/extract-participating-molecules

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import collections as cx
import timeit
import datetime
from neo4j import GraphDatabase
import textwrap
from reactomeneo4j.code.session import Session
from reactomeneo4j.data.species import SPECIES
from reactomeneo4j.code.mkpy.pathways import PathwayMaker


def prt_pathways():
    """Print pathway information for a species."""
    species = 'Homo sapiens' if len(sys.argv)==2 else sys.argv[2]
    # fout_txt = 'log/pathways_{ABC}.py'.format(ABC=abc)
    assert len(sys.argv) != 1, "NO NEO4J PASSWORD PROVIDED"
    password = sys.argv[1]
    obj = PathwayMaker(species, password)
    pw2dcts = obj.get_pw2dcts()

    # prt = sys.stdout
    # with gdr.session() as session:
    #     ses = Session(session)
    #     with open(fout_txt, 'w') as prt:
    #         num_pws = _run(ses, species, prt=prt)
    #         print("  {N:5} WROTE: {TXT}".format(N=num_pws, TXT=fout_txt))
    # #os.system('tail -60 {TXT}'.format(TXT=fout_txt))

####def _prt_rel(node, session):
####    """Print relationships."""
####    # Pathway relationships for Homo sapiens
####    #      11 hasEvent
####    #       9 inferredTo
####    #       5 literatureReference
####    #       3 compartment
####    #       2 authored
####    #       1 modified
####    #       1 created
####    #       1 summation
####    #       1 species
####    #       1 reviewed
####    #       1 goBiologicalProcess
####    #       1 edited
####    session.prt_relationships(session.get_str_node(node))
####
####def _prt_flds_seen(fld2cnt):
####    """Report the fields found and their counts."""
####    # Pathways for Homo sapiens
####    #     2222 schemaClass
####    #     2222 isInDisease
####    #     2222 releaseDate
####    #     2222 displayName
####    #     2222 stId
####    #     2222 speciesName
####    #     2222 stIdVersion
####    #     2222 dbId
####    #     2222 name
####    #     2222 hasDiagram
####    #     2222 isInferred
####    #     1648 oldStId
####    #      892 diagramHeight
####    #      892 diagramWidth
####    #      404 doi
####    #       53 releaseStatus
####    #       16 definition
####    for key, val in fld2cnt.most_common():
####        print("{CNT:4} {FLD}".format(CNT=val, FLD=key))

####def _prt_pw(rec, idx, prt, linelen=120):
####    """Print field."""
####    kws_pw = {f:rec['pw'].get(f) for f in rec['pw']}  # Pathway
####    kws_rel = {f:rec['r'].get(f) for f in rec['r']}    # Summation 'text'
####    kws_dst = {f:rec['dst'].get(f) for f in rec['dst']}    # Summation 'text'
####    print("\n{IDX}) {releaseDate} {stId:13} {displayName}\n".format(IDX=idx, **kws_pw))
####    # prt.write("{SUMMARY}\n".format(
####    #     SUMMARY="\n".join(textwrap.wrap(kws_su['text'], linelen))))
####    #prt.write("{VAL}\n".format(VAL=kws[fld]))  # on Event
####    for e in kws_rel.items():
####        print("R    ", e)
####    for e in kws_dst.items():
####        print("    ", e)


##### KEY-VAL pw <Node id=2458192 labels={'DatabaseObject', 'Event', 'Pathway'} 
##### properties={
#####   'schemaClass': 'Pathway'
#####   'speciesName': 'Homo sapiens'
#####   'oldStId': 'REACT_163813'
#####   'isInDisease': False,
#####   'releaseDate': '2013-06-11'
#####   'displayName': 'Scavenging by Class F Receptors'
#####   'stIdVersion': 'R-HSA-3000484.1'
#####   'dbId': 3000484
#####   'name': ['Scavenging by Class F Receptors']
#####   'stId': 'R-HSA-3000484',
#####   'hasDiagram': False, 'isInferred': False}>

if __name__ == '__main__':
    prt_pathways()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
