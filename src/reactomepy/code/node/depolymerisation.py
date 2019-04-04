"""Reactome Depolymerisation Neo4j Node.

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
class Depolymerisation(ReactionLikeEvent):
    """Reactome Depolymerisation Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name |
    #         isInferred releaseDate speciesName category
    # params_opt: oldStId releaseStatus | isChimeric systematicName

    relationships = {
        **ReactionLikeEvent.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference']),
            'inferredTo': frozenset(['Depolymerisation']),
            'evidenceType': frozenset(['EvidenceType']),

            'input': frozenset(['SimpleEntity', 'Complex', 'Polymer']),
            'output': frozenset([
                'CandidateSet', 'DefinedSet',
                'EntityWithAccessionedSequence',
                'SimpleEntity', 'Complex', 'Polymer']),
            'precedingEvent': frozenset(['Reaction']),
        }
    }

    def __init__(self):
        super(Depolymerisation, self).__init__('Depolymerisation')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
