"""Reactome ReactionLikeEvent Neo4j Node.

Hier: Event:ReactionLikeEvent:Reaction

    - Event (dcnt=8)
    -- ReactionLikeEvent (dcnt=5)
  > --- BlackBoxEvent (dcnt=0)
  > --- Depolymerisation (dcnt=0)
  > --- FailedReaction (dcnt=0)
  > --- Polymerisation (dcnt=0)
  > --- Reaction (dcnt=0)
  > -- Pathway (dcnt=1)
  > --- TopLevelPathway (dcnt=0)

  113,854 Event     82024 Reaction                 1  82024  0.0000 definition
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.reactionlikeevent import ReactionLikeEvent


# pylint: disable=too-few-public-methods
class BlackBoxEvent(ReactionLikeEvent):
    """Reactome ReactionLikeEvent Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name |
    #         isInferred releaseDate speciesName category
    # params_opt: oldStId releaseStatus | isChimeric systematicName
    # params_opt = ReactionLikeEvent.params_opt + ['definition']

    relationships = {
        **ReactionLikeEvent.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference', 'Book']),
            'inferredTo': frozenset(['BlackBoxEvent', 'Reaction']),
            'figure': frozenset(['Figure']),
            'entityFunctionalStatus': frozenset(['EntityFunctionalStatus']),
            'requiredInputComponent': frozenset(['Complex', 'EntityWithAccessionedSequence']),
            'normalReaction': frozenset(['Reaction', 'BlackBoxEvent']),
            'goBiologicalProcess': frozenset(['GO_BiologicalProcess']),
            'evidenceType'       : frozenset(['EvidenceType']),

            # 'entityOnOtherCell': frozenset(['PhysicalEntity']),
            'entityOnOtherCell': frozenset(['DefinedSet',
                                            'EntityWithAccessionedSequence',
                                            'SimpleEntity', 'Polymer']),
            'input': frozenset(['CandidateSet', 'DefinedSet',
                                'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
                                'Complex', 'SimpleEntity', 'OtherEntity', 'Polymer']),
            'output': frozenset(['CandidateSet', 'DefinedSet',
                                 'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
                                 'Complex', 'SimpleEntity', 'OtherEntity', 'Polymer']),
            'precedingEvent': frozenset(['Polymerisation', 'Pathway', 'BlackBoxEvent', 'Reaction']),
            # 'regulatedBy': frozenset(['Regulation']),
            'regulatedBy': frozenset(['NegativeRegulation', 'PositiveGeneExpressionRegulation',
                                      'Requirement',
                                      'PositiveRegulation', 'NegativeGeneExpressionRegulation']),
        }
    }

    def __init__(self):
        super(BlackBoxEvent, self).__init__('BlackBoxEvent')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
