"""Reactome FailedReaction Neo4j Node.

Hier: Event:ReactionLikeEvent:FailedReaction

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

from reactomeneo4j.code.node.reactionlikeevent import ReactionLikeEvent


# pylint: disable=too-few-public-methods
class FailedReaction(ReactionLikeEvent):
    """Reactome FailedReaction Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name |
    #         stId stIdVersion name isInDisease isInferred releaseDate speciesName
    # params_opt: oldStId releaseStatus | isChimeric systematicName

    relationships = {
        **ReactionLikeEvent.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference']),
            'inferredTo': frozenset(['FailedReaction']),
            'entityFunctionalStatus': frozenset(['EntityFunctionalStatus']),
            'normalReaction': frozenset(['Reaction', 'BlackBoxEvent']),

            # 'entityOnOtherCell': frozenset(['PhysicalEntity']),
            'entityOnOtherCell': frozenset(['EntityWithAccessionedSequence']),
            'input': frozenset([
                'CandidateSet', 'DefinedSet',
                'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
                'SimpleEntity', 'Complex', 'OtherEntity', 'Polymer']),
            'output': frozenset(['Complex', 'EntityWithAccessionedSequence']),
            'precedingEvent': frozenset(['Reaction']),
            # 'regulatedBy': frozenset(['Regulation']),
            'regulatedBy': frozenset(['NegativeRegulation']),
        }
    }

    def __init__(self):
        super(FailedReaction, self).__init__('FailedReaction')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
