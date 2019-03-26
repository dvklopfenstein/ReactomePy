"""Reactome FunctionalStatusType Neo4j Node.

Hier: FunctionalStatusType

  - DatabaseObject (dcnt=80)
> -- FunctionalStatusType (dcnt=0)

2018/12:
    "loss_of_function"
    "gain_of_function"
    "decreased_transcript_level"
    "partial_loss_of_function"
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class FunctionalStatusType(DatabaseObject):
    """FunctionalStatusType."""

    # params: dbId schemaClass displayName
    params_opt = ('name',)

    def __init__(self):
        super(FunctionalStatusType, self).__init__('FunctionalStatusType')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
