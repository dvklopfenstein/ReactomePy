"""Reactome FunctionalStatus Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- FunctionalStatus (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class FunctionalStatus(DatabaseObject):
    """FunctionalStatus."""

    # params: dbId schemaClass displayName

    relationships = {
        'referenceDatabase': set(['ReferenceDatabase']),
        'functionalStatusType': set(['FunctionalStatusType']),
        'structuralVariant': set(['SequenceOntology']),
    }

    def __init__(self):
        super(FunctionalStatus, self).__init__('FunctionalStatus')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
