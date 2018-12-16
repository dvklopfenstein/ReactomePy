"""Reactome CatalystActivity Neo4j Node.

Hier: CatalystActivity

  - DatabaseObject (dcnt=80)
> -- CatalystActivity (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class CatalystActivity(DatabaseObject):
    """Report the dates that a pathway was edited."""

    # params: dbId schemaName displayName

    relationships = {
        'physicalEntity': set(['PhysicalEntity']),
        'activeUnit': set(['Complex', 'EntitySet', 'GenomeEncodedEntity']),
        'activity': set(['GO_MolecularFunction']),
    }

    def __init__(self):
        super(CatalystActivity, self).__init__('CatalystActivity')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
