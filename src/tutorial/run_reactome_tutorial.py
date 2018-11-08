#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# https://reactome.org/dev/graph-database/extract-participating-molecules

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import neo4j
from neo4j import GraphDatabase
from reactomeneo4j.code.session import Session
from reactomeneo4j.code.node import Node
from reactomeneo4j.code.record import Record


def test_reactome_tutorial(pwd, abc='hsa'):
    """Mirror Reactome/Neo4j tutorial in Python."""
    gdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', pwd))
    with gdr.session() as session:
        ses = Session(session)
        #help(session)
        _run(ses)

def _1a_getobj_w_id(qry, session):
    """1a) RETRIEVING OBJECTS BASED ON THEIR IDENTIFIER')."""
    # MATCH (pathway:Pathway{stId:"R-HSA-1236975"}) RETURN pathway
    pwy_node = session.run(qry).data()[0]['pathway']
    #    NEO4J NODE ID(2052401)
    #    dbId        1236975
    #    displayName Antigen processing-Cross presentation
    #    hasDiagram  False
    #    isInDisease False
    #    isInferred  False
    #    name        ['Antigen processing-Cross presentation']
    #    oldStId     REACT_111119
    #    releaseDate 2011-09-20
    #    schemaClass Pathway
    #    speciesName Homo sapiens
    #    stId        R-HSA-1236975
    #    stIdVersion R-HSA-1236975.1
    #print(pwy)
    #help(pwy.graph)
    # <Node id=2052401 labels={'DatabaseObject', ... properties={...
    print("NEO4J NODE ID({})".format(pwy_node.id))
    # Neo4j's properties:
    for key, val in sorted(pwy_node.items()):
        print("{KEY:11} {VAL}".format(KEY=key, VAL=val))
    session.prt_relationships(session.get_str_node(pwy_node))

def _1b_get_protein(qry, session):
    """1b) RETRIEVE PROTEIN'"""
    # MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}) RETURN ewas
    res = session.run(qry)        # neo4j.BoltStatementResult
    ewas = res.data()[0]['ewas']  # EntityWithAccessionedSequence
    #    NEO4J NODE ID(2052401)
    #    dbId        1236975
    #    displayName Antigen processing-Cross presentation
    #    hasDiagram  False
    #    isInDisease False
    #    isInferred  False
    #    name        ['Antigen processing-Cross presentation']
    #    oldStId     REACT_111119
    #    releaseDate 2011-09-20
    #    schemaClass Pathway
    #    speciesName Homo sapiens
    #    stId        R-HSA-1236975
    #    stIdVersion R-HSA-1236975.1
    session.prt_properties_node(ewas)
    session.prt_relationships(session.get_str_node(ewas))

def _1c_get_protein_name(qry, session):
    """1c) RETRIEVE PROTEIN's displayName and Identifier:"""
    # MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}), (ewas)-[:referenceEntity]->(re:ReferenceEntity) RETURN ewas.displayName AS EWAS, re.identifier AS ID
    #     EWAS             ID
    #     ---------------  ------
    #     PTEN [cytosol]   P60484
    res = session.run(qry)  # neo4j.BoltStatmentResult
    print(res.data())  # [{'EWAS': 'PTEN [cytosol]', 'ID': 'P60484'}]

def _1d_get_protein_name(qry, session):
    """1c) RETRIEVE PROTEIN's displayName and Identifier:"""
    # TIP: the _MATCH_ part of the previous one
    # MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"})-[:referenceEntity]->(re:ReferenceEntity) RETURN ewas.displayName AS EWAS, re.identifier AS ID
    #     EWAS             ID
    #     ---------------  ------
    #     PTEN [cytosol]   P60484
    res = session.run(qry)  # neo4j.BoltStatmentResult
    print(res.data())  # [{'EWAS': 'PTEN [cytosol]', 'ID': 'P60484'}]

def _1e_get_protein_name(qry, session):
    """1c) RETRIEVE PROTEIN's displayName and Identifier:"""
    # Continuing on it, it is possible to construct a query to retrieve the "reference database"
    # on top of the previously retrieved fields.
    # MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"})-[:referenceEntity]->(re:ReferenceEntity) RETURN ewas.displayName AS EWAS, re.identifier AS ID
    #     EWAS             ID
    #     ---------------  ------
    #     PTEN [cytosol]   P60484
    res = session.run(qry)  # neo4j.BoltStatmentResult
    print(res.data())  # [{'EWAS': 'PTEN [cytosol]', 'ID': 'P60484'}]


def _run(session):
    # Methods: data value values | attached consume detach graph keys peek records single summary

    print('1a) RETRIEVING OBJECTS BASED ON THEIR IDENTIFIER')
    qry = 'MATCH (pathway:Pathway{stId:"R-HSA-1236975"}) RETURN pathway'
    _1a_getobj_w_id(qry, session)

    print('\n1b) RETRIEVE PROTEIN')
    qry = 'MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}) RETURN ewas'
    _1b_get_protein(qry, session)
    #session.prt_relationships_all()
   
    print("\n1c) RETRIEVE PROTEIN's displayName and Identifier:")
    qry = ('MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}),'
           '(ewas)-[:referenceEntity]->(re:ReferenceEntity) '
           'RETURN ewas.displayName AS EWAS, re.identifier AS ID')
    _1c_get_protein_name(qry, session)  # [{'EWAS': 'PTEN [cytosol]', 'ID': 'P60484'}]

    print("\n1d) RETRIEVE PROTEIN's ref database on top of the previously:")
    qry = ('MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"})-'
           '[:referenceEntity]->(re:ReferenceEntity) '
           'RETURN ewas.displayName AS EWAS, re.identifier AS ID')
    _1d_get_protein_name(qry, session)  # [{'EWAS': 'PTEN [cytosol]', 'ID': 'P60484'}]

    # MATCH PART CAN ALSO BE:
    print('\n1e) ALSO GET REFERENCE DB(node) ON TOP OF PREVIOUSLY RETRIEVED FIELDS')
    qry = ('MATCH (ewas:EntityWithAccessionedSequence{stId:"R-HSA-199420"}),'
           '(ewas)-[:referenceEntity]->(re:ReferenceEntity)'
           '-[:referenceDatabase]->(rd:ReferenceDatabase) '
           'RETURN ewas.displayName AS EWAS, re.identifier AS Identifier, rd.displayName AS Database')
    _1e_get_protein_name(qry, session)
    ## # [['PTEN [cytosol]', 'P60484', 'UniProt']]
    ## print(session.run(qry).data())

    return

    #### print('\n2) BREAKING DOWN COMPLEXES AND SETS TO GET THEIR PARTICIPANTS')
    #### # https://reactome.org/content/schema/Complex
    #### # MATCH (Complex{stId:"R-HSA-983126"})-[:hasComponent]->(pe:PhysicalEntity) RETURN pe.stId AS component_stId, pe.displayName AS component
    #### qry = ('MATCH (Complex{stId:"R-HSA-983126"})-'
    ####        '[:hasComponent]->(pe:PhysicalEntity) RETURN '
    ####        'pe.stId AS component_stId, '
    ####        'pe.displayName AS component')
    #### #
    #### #     component_stId   component
    #### #     --------------   ----------
    #### #     'R-HSA-976075    E3 ligases in proteasomal degradation [cytosol]
    #### #     'R-ALL-983035    antigenic substrate [cytosol]
    #### #     'R-HSA-976165    Ubiquitin:E2 conjugating enzymes [cytosol]
    #### for dct in session.run(qry).data():
    ####     print('{ID} {NAME}'.format(ID=dct['component_stId'], NAME=dct['component']))

    #### qry = ('MATCH (Complex{stId:"R-HSA-983126"})-'
           '[:hasComponent]->(pe:PhysicalEntity) RETURN pe')
    res = session.run(qry)
    graph = res.graph()
    print(graph)
    print(dir(res))
    print("")
    for rec in res.records():
        # print(rec['pe'].data())
        print(rec)
        print(rec.data())
        print("RECORD", dir(rec))
        print("PE", rec['pe'])
        # print('ITEMS:', rec.items())
        # for key, val in rec.items():
        #     print("KEY-VAL {KEY:11} {VAL}".format(KEY=key, VAL=val))
        print("")
    for rec in res.records():
        print("RRRRRRRRRRRRRR", rec)

    ses = Session(session)
    ses.prt_relationships('Complex{stId:"R-HSA-983126"}')
    ses.get_node(2020241)
    

    # query_1b('MATCH (c:Complex{stId:"R-HSA-983126"}) RETURN c', gdb)
    #
    # GET SET AND COMPLEX INSIDE COMPLEX, R-HSA-983126 (returns ~284 entities)
    # query_1b(('MATCH (Complex{stId:"R-HSA-983126"})-'
    #           '[:hasComponent|hasMember|hasCandidate*]->'
    #           '(pe:PhysicalEntity) RETURN DISTINCT '
    #           'pe.stId AS component_stId, '
    #           'pe.displayName AS component'), gdb)

    # 3) RETRIEVING PATHWAYS, SUBPATHWAYS, AND SUPERPATHWAYS
    # Pathway      SubPathway    DisplayName
    # R-HSA-983169 R-HSA-983168  Antigen proc.: Ubiq. & Proteasome degradation
    # R-HSA-983169 R-HSA-1236975 Antigen proc-Cross presentation
    # R-HSA-983169 R-HSA-983170  Antigen Pres.: Folding, assembly & peptide loading of MHC-I
    # query_1b(('MATCH (p:Pathway{stId:"R-HSA-983169"})-'
    #           '[:hasEvent]->(sp:Pathway) RETURN '
    #           'p.stId AS Pathway, '
    #           'sp.stId AS SubPathway, '
    #           'sp.displayName as DisplayName'), gdb)
    #query_1b('MATCH (p:Pathway{stId:"R-HSA-983169"}) RETURN p', gdb)
    #
    # GET ALL SUB-PATHWAYS UNDER SUB-PATHWAYS
    # query_1b(('MATCH (p:Pathway{stId:"R-HSA-983169"})-'
    #           '[:hasEvent*]->(sp:Pathway) RETURN '
    #           'p.stId AS Pathway, '
    #           'sp.stId AS SubPathway, '
    #           'sp.displayName as DisplayName'), gdb)
    #
    # GET SUPER-PATHWAY:
    #     Pathway      SubPathway    DisplayName
    #     R-HSA-983169 R-HSA-1280218 Adaptive Immune System
    # ('MATCH (p:Pathway{stId:"R-HSA-983169"})<-'
    #  '[:hasEvent]-(sp:Pathway) RETURN '
    #  'p.stId AS Pathway, '
    #  'sp.stId AS SubPathway, '
    #  'sp.displayName as DisplayName')
    #
    #     Pathway      SubPathway    DisplayName
    #     R-HSA-983169 R-HSA-1280218 Adaptive Immune System
    #     R-HSA-983169 R-HSA-168256  Immune System
    # GET ALL SUPER-PATHWAYS UP TO ROOT
    # ('MATCH (p:Pathway{stId:"R-HSA-983169"})<-'
    #  '[:hasEvent*]-(sp:Pathway) RETURN '
    #  'p.stId AS Pathway, '
    #  'sp.stId AS SubPathway, '
    #  'sp.displayName as DisplayName')

    # 4) RETRIEVING THE REACTIONS FOR A GIVEN PATHWAY
    # ('MATCH (p:Pathway{stId:"R-HSA-983169"})'
    #  '-[:hasEvent*]->(rle:ReactionLikeEvent) RETURN '
    #  'p.stId AS Pathway, '
    #  'rle.stId AS Reaction, '
    #  'rle.displayName as ReactionName')

    # 5) RETRIEVING THE PARTICIPANTS OF A REACTION
    #   Reaction      Participant   DisplayName
    #   R-HSA-8863895 R-HSA-168113  CHUK:IKBKB:IKBKG [cytosol]
    #   R-HSA-8863895 R-ALL-113592  ATP [cytosol]
    #   R-HSA-8863895 R-HSA-8863966 SNAP23 [phagocytic vesicle membrane]
    #   R-HSA-8863895 R-HSA-8863923 p-S95-SNAP23 [phagocytic vesicle membrane]
    #   R-HSA-8863895 R-ALL-29370   ADP [cytosol]
    #   R-HSA-8863895 R-HSA-937033  oligo-MyD88:Mal:BTK:activated TLR [plasma membrane]
    #
    # ('MATCH (r:ReactionLikeEvent{stId:"R-HSA-8863895"})-'
    #  '[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator*]->'
    #  '(pe:PhysicalEntity) RETURN DISTINCT '
    #  'r.stId AS Reaction, '
    #  'pe.stId as Participant, '
    #  'pe.displayName AS DisplayName')
    #
    # INCLUDE COMPONENTS OF COMPLEXES AND SETS
    #('MATCH (r:ReactionLikeEvent{stId:"R-HSA-8863895"})-'
    # '[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator|'
    # 'hasComponent|hasMember|hasCandidate*]->(pe:PhysicalEntity) '
    # 'RETURN DISTINCT '
    # 'r.stId AS Reaction, '
    # 'pe.stId as Participant, '
    # 'pe.displayName AS DisplayName')

    # 6) JOINING THE PIECES: PARTICIPATING MOLECULES FOR A PATHWAY
    # Concatenate all preceding queries to get all proteins/chemicals in pathway
    #('MATCH (p:Pathway{stId:"R-HSA-983169"})-'
    # '[:hasEvent*]->(rle:ReactionLikeEvent),(rle)-'
    # '[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator|'
    # 'hasComponent|hasMember|hasCandidate*]->(pe:PhysicalEntity),'
    # '(pe)-[:referenceEntity]->(re:ReferenceEntity)-'
    # '[:referenceDatabase]->(rd:ReferenceDatabase) RETURN DISTINCT '
    # 're.identifier AS Identifier, rd.displayName AS Database')

def query_1b(qry, gdb):
    """Examine protein stored in QuerySequence."""
    node = gdb.get_query_node(qry)
    print("SSSSSSSSS", node)
    print("SSSSSSSSS", dir(node))
    # res.cast(cls, elements)
    # res.columns        ['ewas']
    # res.count(value)
    # res.elements       []
    # res.get_response() {'columns': ['ewas'], 'data': []}
    # res.graph          None
    # res.index(value)
    # res.params         None
    # res.q              'MATCH (ewas:EntityWithAcessionedSeq ...
    # res.rows
    # res.stats
    # res.to_html
    # print("RESULTS:", res.rows)

def query_1a(qry, gdb):
    """MATCH (pathway:Pathway{stId:"R-HSA-1236975"}) RETURN pathway"""
    print(qry)
    labels = ['delete', 'get', 'id', 'items', 'labels', 'properties',
              'relationships', 'set', 'traverse', 'update', 'url']
    # <neo4jrestclient.query.QuerySequence
    results = gdb.query(qry, returns=(client.Node, str, client.Node))
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

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
