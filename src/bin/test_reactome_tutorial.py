#!/usr/bin/env python
"""Mirror Reactome/Neo4j tutorial in Python."""
# neo4j-shell -file query.cql > out.txt
# bin/cypher-shell -u neo4j -p free2beme

from __future__ import print_function

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
# from PyBiocode.Utils.module_helper import import_var
# from PyBiocode.Utils.module_helper import import_mod


def test_reactome_tutorial(pwd, abc='hsa'):
    """Mirror Reactome/Neo4j tutorial in Python."""
    dag = GraphDatabase('http://localhost:7474', username='neo4j', password=pwd)
    # obj = _Data(abc)

    # # 1) RETRIEVING OBJECTS BASED ON THEIR IDENTIFIER
    # pwid = 'R-HSA-1236975'
    # #     MATCH (pathway:Pathway{stId:"R-HSA-1236975"}) RETURN pathway
    # #       {
    # #         "schemaClass": "Pathway",
    # #         "speciesName": "Homo sapiens",
    # #         "oldStId": "REACT_111119",
    # #         "isInDisease": false,
    # #         "releaseDate": "2011-09-20",
    # #         "displayName": "Antigen processing-Cross presentation",
    # #         "stIdVersion": "R-HSA-1236975.1",
    # #         "dbId": 1236975,
    # #         "name": [
    # #           "Antigen processing-Cross presentation"
    # #         ],
    # #         "stId": "R-HSA-1236975",
    # #         "hasDiagram": false,
    # #         "isInferred": false
    # #       }
    # print("{ID}:{PW}".format(ID=pwid, PW=obj.id2pw[pwid]))

    # # 1) RETRIEVING OBJECTS BASED ON THEIR IDENTIFIER
    # peid = 'R-HSA-199420'



if __name__ == '__main__':
    if len(sys.argv) != 1:
        pwd = sys.argv[1]
        print(pwd)
        # test_reactome_tutorial(pwd)

# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
