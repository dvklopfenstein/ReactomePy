"""Reactome CatalystActivity Neo4j Node.

  - DatabaseObject(dcnt=80)
> -- CatalystActivity(dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class CatalystActivity(DatabaseObject):
    """Report the dates that a pathway was edited."""

    # params: dbId schemaName displayName

    relationships = {
        'physicalEntity': set(['PhysicalEntity']),
    }

    def __init__(self):
        super(CatalystActivity, self).__init__('CatalystActivity')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.