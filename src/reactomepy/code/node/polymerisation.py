"""Reactome Polymerisation Neo4j Node.

Hier: Event:ReactionLikeEvent:Polymerisation

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
class Polymerisation(ReactionLikeEvent):
    """Reactome ReactionLikeEvent Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name |
    #         isInferred releaseDate speciesName category
    # params_opt: oldStId releaseStatus | isChimeric systematicName

    relationships = {
        **ReactionLikeEvent.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference']),
            'inferredTo': frozenset(['Polymerisation', 'BlackBoxEvent']),
            'requiredInputComponent': frozenset(['Complex', 'EntityWithAccessionedSequence']),
            'evidenceType': frozenset(['EvidenceType']),
            'input': frozenset(['CandidateSet', 'DefinedSet',
                                'EntityWithAccessionedSequence',
                                'Complex', 'SimpleEntity', 'Polymer']),
            'output': frozenset(['CandidateSet', 'DefinedSet',
                                 'Complex', 'SimpleEntity', 'Polymer']),
            'precedingEvent': frozenset(['Polymerisation', 'BlackBoxEvent', 'Reaction']),
            'regulatedBy' : frozenset(['PositiveRegulation', 'NegativeRegulation']),
        }
    }

    def __init__(self):
        super(Polymerisation, self).__init__('Polymerisation')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
