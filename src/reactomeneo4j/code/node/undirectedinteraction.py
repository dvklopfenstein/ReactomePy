"""Reactome UndirectedInteraction Neo4j Node.

  - Interaction (dcnt=1)
> -- UndirectedInteraction (dcnt=0)

   35,113 Interaction  35113 UndirectedInteraction  35113  35113  1.0000 accession
   35,113 Interaction  35113 UndirectedInteraction  35113  35113  1.0000 databaseName
   35,113 Interaction  35113 UndirectedInteraction  35113  35113  1.0000 score
   35,113 Interaction  35113 UndirectedInteraction  35113  35113  1.0000 url
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class UndirectedInteraction(DatabaseObject):
    """UndirectedInteraction."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ['databaseName', 'accession', 'url', 'score']

    relationships = {
        'referenceDatabase': set(['ReferenceDatabase']),
        'interactor': set(['ReferenceEntity']),
    }

    def __init__(self):
        super(UndirectedInteraction, self).__init__('UndirectedInteraction')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
