"""Reactome FunctionalStatusType Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- FunctionalStatusType (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class FunctionalStatusType(DatabaseObject):
    """FunctionalStatusType."""

    # params: dbId schemaClass displayName
    params_opt = ['name']

    def __init__(self):
        super(FunctionalStatusType, self).__init__('FunctionalStatusType')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
