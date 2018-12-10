"""Reactome Figure Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- Figure (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Figure(DatabaseObject):
    """Figure."""

    # params: dbId schemaClass displayName
    params_req = ['url']

    def __init__(self):
        super(Figure, self).__init__('Figure')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
