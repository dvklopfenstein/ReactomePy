"""Reactome ControlReference Neo4j Node.

Hier: ControlReference

  - DatabaseObject (dcnt=80)
> -- ControlReference (dcnt=2)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class ControlReference(DatabaseObject):
    """Report the dates that a pathway was edited."""

    # params: dbId schemaName displayName

    relationships = {
        'literatureReference': frozenset(['URL', 'Book', 'LiteratureReference']),
        #'activity': frozenset(['GO_MolecularFunction']),
        #'activeUnit': frozenset([
        #    'CandidateSet', 'DefinedSet',
        #    'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
        #    'Complex']),
        #'literatureReference': frozenset(['LiteratureReference']),
        ## 'physicalEntity': frozenset(['PhysicalEntity']),
        #'physicalEntity': frozenset([
        #    'CandidateSet', 'DefinedSet',
        #    'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
        #    'Complex', 'OtherEntity', 'Polymer']),
    }

    def __init__(self, name='ControlReference'):
        super(ControlReference, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
