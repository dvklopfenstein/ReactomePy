"""Reactome Publication Neo4j Node.

    - Publication (dcnt=3)
  > -- Book (dcnt=0)
  > -- LiteratureReference (dcnt=0)
  > -- URL  (dcnt=0)

   28,896 Publication                       28758 LiteratureReference               28758  28758  1.0000 journal              
   28,896 Publication                       28758 LiteratureReference               28584  28758  0.9939 pages                
   28,896 Publication                       28758 LiteratureReference               28744  28758  0.9995 pubMedIdentifier     
   28,896 Publication                       28758 LiteratureReference               28596  28758  0.9944 volume               
   28,896 Publication                       28758 LiteratureReference               28758  28758  1.0000 year                 

   28,896 Publication                         117 Book                                101    117  0.8632 ISBN                 
   28,896 Publication                         117 Book                                 84    117  0.7179 chapterTitle         
   28,896 Publication                         117 Book                                 74    117  0.6325 pages                
   28,896 Publication                         117 Book                                117    117  1.0000 year                 

   28,896 Publication                          21 URL                                  21     21  1.0000 uniformResourceLocator 
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Publication(DatabaseObject):
    """Params seen on all Publication."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_req = DatabaseObject.params_req + ['title']

    def __init__(self, name):
        super(Publication, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
