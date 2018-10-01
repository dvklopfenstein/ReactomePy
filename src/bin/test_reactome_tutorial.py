#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# http::

from __future__ import print_function

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
from reactomeneo4j.neo4j.lit_ref import LiteratureReference
from reactomeneo4j.neo4j.pathway import Pathway


def test_reactome_tutorial(pwd, abc='hsa'):
    """Mirror Reactome/Neo4j tutorial in Python."""
    dbpw = GraphDatabase('http://localhost:7474', username='neo4j', password=pwd)

    # 1) RETRIEVING OBJECTS BASED ON THEIR IDENTIFIER
    qry = 'MATCH (pathway:Pathway{stId:"R-HSA-1236975"}) RETURN pathway'
    print(qry)
    query_1a(qry, dbpw)

def query_1a(qry, dbpw):
    labels = ['delete', 'get', 'id', 'items', 'labels', 'properties',
              'relationships', 'set', 'traverse', 'update', 'url']
    results = dbpw.query(qry, returns=(client.Node, str, client.Node))
    for res in results:
        print("RESULTS:", res)
        # node_top.id = 2052401
        # node_top.labels 'Neo4j Label': DatabaseObject Pathway Event
        # node_top.properties == node_top.items
        # node_top.relationships: .count()=36 .create .get
        # node_top.url = http://localhost:7474/db/data/node/2052401
        # node_top.get(key)
        # node_top.set(key, value)
        # node_top.update()
        # node_top.traverse() iterator on Neo4j Nodes
        node_top = res[0]
        objpw = Pathway(node_top)
        
        print('{R} {A} {B}'.format(R=res, A=node_top['name'], B=node_top['stId']))
        # keys same as properties
        for key, val in node_top.items():
            print('items {K:12} {V:}'.format(K=key, V=val))
        #for relationship in node_top.relationships:
        #    print('relationships {L:12}'.format(L=relationship))
        # for label in node_top.labels:
        #     print('labels {L:12}'.format(L=label))
        # print("DIR:", dir(node_top))
        print('\n')
        print(objpw)
        for node in node_top.traverse():
            if 'LiteratureReference' in node.labels:
                print(LiteratureReference(node))
        # for e in dir(node_top):
        #     if e[0] != "_":
        #         print("{:20}".format(e), node_top[e])
        #print('({A})-[{B}]->({C})'.format(A=res[0]['name'], B=res[1], C=res[2]['name']))
    #       {
    #         "schemaClass": "Pathway",
    #         "speciesName": "Homo sapiens",
    #         "oldStId": "REACT_111119",
    #         "isInDisease": false,
    #         "releaseDate": "2011-09-20",
    #         "displayName": "Antigen processing-Cross presentation",
    #         "stIdVersion": "R-HSA-1236975.1",
    #         "dbId": 1236975,
    #         "name": [
    #           "Antigen processing-Cross presentation"
    #         ],
    #         "stId": "R-HSA-1236975",
    #         "hasDiagram": false,
    #         "isInferred": false
    #       }
    # print("{ID}:{PW}".format(ID=pwid, PW=obj.id2pw[pwid]))

    # # 1) RETRIEVING OBJECTS BASED ON THEIR IDENTIFIER
    # peid = 'R-HSA-199420'


if __name__ == '__main__':
    if len(sys.argv) != 1:
        pwd = sys.argv[1]
        print(pwd)
        test_reactome_tutorial(pwd)
    else:
        print('First arg must be the password')

# 'Neo4j Label' combos (all contain DatabaseObject):
#     22 'Pathway'       'Event'
#      6 'Publication'   'LiteratureReference'
#      3 'InstanceEdit'  
#      1 'Taxon'         'Species'
#      1 'GO_Term'       'GO_BiologicalProcess'
#      1 'Summation'
 
# neo4j-shell -file query.cql > out.txt
# bin/cypher-shell -u neo4j -p free2beme
# https://marcobonzanini.com/2015/04/06/getting-started-with-neo4j-and-python/

# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
