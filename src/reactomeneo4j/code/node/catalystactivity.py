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
        'activity': set(['GO_MolecularFunction']),

        'activeUnit': set(['Complex', 'CandidateSet', 'GenomeEncodedEntity', 'DefinedSet', 'EntityWithAccessionedSequence']),
        # 'physicalEntity': set(['PhysicalEntity']),
        'physicalEntity': set(['Complex', 'CandidateSet', 'GenomeEncodedEntity', 'DefinedSet', 'OtherEntity', 'Polymer', 'EntityWithAccessionedSequence']),
    }

    def __init__(self):
        super(CatalystActivity, self).__init__('CatalystActivity')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
