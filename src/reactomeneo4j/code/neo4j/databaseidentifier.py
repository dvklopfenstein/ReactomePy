"""Reactome DatabaseIdentifier Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- DatabaseIdentifier (dcnt=0)

  307,384 DatabaseIdentifier   307384 DatabaseIdentifier   307384 307384  1.0000 databaseName
  307,384 DatabaseIdentifier   307384 DatabaseIdentifier   307384 307384  1.0000 identifier
  307,384 DatabaseIdentifier   307384 DatabaseIdentifier   307384 307384  1.0000 url
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class DatabaseIdentifier(DatabaseObject):
    """DatabaseIdentifier."""

    # params: dbId schemaClass displayName
    params_opt = DatabaseObject.params_opt + ['databaseName', 'identifier', 'url']

    relationships = {
        'referenceDatabase': set(['ReferenceDatabase']),
    }

    def __init__(self):
        super(DatabaseIdentifier, self).__init__('DatabaseIdentifier')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.