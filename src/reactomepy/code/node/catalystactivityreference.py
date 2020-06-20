"""Reactome CatalystActivityReference Neo4j Node.

Hier: CatalystActivityReference

  - DatabaseObject (dcnt=80)
  -- ControlReference (dcnt=2)
  --- CatalystActivityReference
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.controlreference import ControlReference


# pylint: disable=too-few-public-methods
class CatalystActivityReference(ControlReference):
    """Report the dates that a pathway was edited."""

    # params: dbId schemaName displayName

    relationships = {
        **ControlReference.relationships,
        **{
            'catalystActivity': frozenset(['CatalystActivity']),
            'literatureReference': frozenset(['LiteratureReference', 'Book']),
        },
    }
    #    'activity': frozenset(['GO_MolecularFunction']),

    #    'activeUnit': frozenset([
    #        'CandidateSet', 'DefinedSet',
    #        'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
    #        'Complex']),
    #    #'literatureReference': frozenset(['URL', 'Book', 'LiteratureReference']),
    #    # 'physicalEntity': frozenset(['PhysicalEntity']),
    #    'physicalEntity': frozenset([
    #        'CandidateSet', 'DefinedSet',
    #        'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
    #        'Complex', 'OtherEntity', 'Polymer']),
    #}

    def __init__(self):
        super(CatalystActivityReference, self).__init__('CatalystActivityReference')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
