"""Reactome RegulationReference Neo4j Node.

Hier: RegulationReference

  - DatabaseObject (dcnt=80)
  -- ControlReference (dcnt=2)
  --- RegulationReference
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.controlreference import ControlReference


# pylint: disable=too-few-public-methods
class RegulationReference(ControlReference):
    """Report the dates that a pathway was edited."""

    # params: dbId schemaName displayName

    relationships = {
        **ControlReference.relationships,
        **{
            #'regulation': 'Regulation',
            'regulation': frozenset([
                'NegativeRegulation',
                'NegativeGeneExpressionRegulation',
                'PositiveRegulation',
                'PositiveGeneExpressionRegulation',
                'Requirement',
            ]),
        #     'catalystActivity': frozenset(['CatalystActivity']),
        #     'literatureReference': frozenset(['LiteratureReference']),
        },
    }
    #relationships = {
    #    'activity': frozenset(['GO_MolecularFunction']),

    #    'activeUnit': frozenset([
    #        'CandidateSet', 'DefinedSet',
    #        'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
    #        'Complex']),
    #    #'literatureReference': frozenset(['URL', 'Book', 'LiteratureReference']),
    #    'literatureReference': frozenset(['LiteratureReference']),
    #    # 'physicalEntity': frozenset(['PhysicalEntity']),
    #    'physicalEntity': frozenset([
    #        'CandidateSet', 'DefinedSet',
    #        'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
    #        'Complex', 'OtherEntity', 'Polymer']),
    #}

    def __init__(self):
        super(RegulationReference, self).__init__('RegulationReference')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
