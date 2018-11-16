#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://reactome.org/dev/graph-database/extract-participating-molecules

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
from neo4j import GraphDatabase
# import collections as cx
# import timeit
# import datetime
# import textwrap
# from reactomeneo4j.data.species import SPECIES
from reactomeneo4j.code.wrpy.pathway_query import PathwayQuery
from reactomeneo4j.code.wrpy.query_general import Query
from reactomeneo4j.code.wrpy.wrpy_general import WrPy
from reactomeneo4j.code.wrpy.pathway_wrpy import PathwayWrPy
from reactomeneo4j.code.species import Species

def main(password):
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    objqry = Query(gdbdr)
    objwr = WrPy()
    objwr.wrpy_version('src/reactomeneo4j/data/reactome_version.py', objqry.get_version())
    orgs = [
        'Homo sapiens',
        'Mus musculus',
        'Drosophila melanogaster',
    ]
    pmid2nt = {}
    for species in orgs:
        objabc = Species(species)
        fout_log = '{ABC}_pathways.log'.format(ABC=objabc.abc)
        with open(fout_log, 'w') as log:
            objqu = PathwayQuery(objabc, gdbdr, log)
            objwr = PathwayWrPy(objqu, log)
            prt_pathways(objwr, objabc.abc)
            print('  WROTE: {LOG}'.format(LOG=fout_log))

def prt_pathways(objwr, abc):
    """Print pathways and their details for a species."""
    dir_pwy = 'src/reactomeneo4j/data/{ABC}/pathways/'.format(ABC=abc)
    fout_py = 'src/reactomeneo4j/data/{ABC}/pathways/pathways.py'.format(ABC=abc)
    fout_sum = 'src/reactomeneo4j/data/{ABC}/pathways/pwy2summation.py'.format(ABC=abc)
    fout_pub = 'src/reactomeneo4j/data/{ABC}/pathways/pwy2pmids.py'.format(ABC=abc)
    fout_fig = 'src/reactomeneo4j/data/{ABC}/pathways/pwy2imgname.py'.format(ABC=abc)
    fout_inf = 'src/reactomeneo4j/data/{ABC}/pathways/inferredto.py'.format(ABC=abc)
    fout_pmd = 'src/reactomeneo4j/data/{ABC}/pathways/pmid2nt.py'.format(ABC=abc)
    fous_txt = '{ABC}_pathways_short.txt'.format(ABC=abc)
    fout_txt = '{ABC}_pathways.txt'.format(ABC=abc)
    objwr.wrpwys(fous_txt)
    objwr.wrpy_pwy2nt(fout_py)
    objwr.wrpy_pwy2summation(fout_sum)
    objwr.wrpy_pwy2pmids(fout_pub)
    pmid2nt = objwr.wrpy_pubmeds(fout_pmd)
    objwr.wrtxt(fout_txt)
    objwr.wrpy_figure(fout_fig)
    objwr.wrpy_gons(os.path.join(dir_pwy, 'pwy2bp.py'), 'GO_BiologicalProcess')
    objwr.wrpy_gons(os.path.join(dir_pwy, 'pwy2cc.py'), 'Compartment')
    objwr.wrpy_relatedspecies(os.path.join(dir_pwy, 'pwy2relatedspecies.py'))
    objwr.wrpy_pwy2disease(os.path.join(dir_pwy, 'pwy2disease.py'))
    # objwr.wrpy_inferredto(fout_inf)
    return {'pmid2nt':pmid2nt}


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
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
