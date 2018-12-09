"""Lists parameters seen on all ReferenceEntity.

  - DatabaseObject (dcnt=80)
> -- ReferenceDatabase (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject

# pylint: disable=too-few-public-methods
class ReferenceDatabase(DatabaseObject):
    """Lists parameters seen on all ReferenceEntity."""

    # req: dbId displayName schemaClass
    params_req = DatabaseObject.params_req + ['accessUrl', 'name', 'url']

    def __init__(self):
        super(ReferenceDatabase, self).__init__('ReferenceDatabase')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
