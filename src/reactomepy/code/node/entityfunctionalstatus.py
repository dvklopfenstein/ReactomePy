"""Reactome EntityFunctionalStatus Neo4j Node.

  - DatabaseObject(dcnt=80)
> -- EntityFunctionalStatus(dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class EntityFunctionalStatus(DatabaseObject):
    """Report the dates that a pathway was edited."""

    # params: dbId schemaName displayName

    relationships = {
        #### 'physicalEntity': frozenset(['CandidateSet', 'DefinedSet',
        ####                              'EntityWithAccessionedSequence', 'Complex']),
        'normalEntity': frozenset(['CandidateSet', 'DefinedSet',
                                   'EntityWithAccessionedSequence', 'Complex', 'Polymer']),
        'diseaseEntity': frozenset(['CandidateSet', 'DefinedSet',
                                    'EntityWithAccessionedSequence', 'Complex']),
        'functionalStatus': frozenset(['FunctionalStatus']),
    }

    def __init__(self):
        super(EntityFunctionalStatus, self).__init__('EntityFunctionalStatus')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
