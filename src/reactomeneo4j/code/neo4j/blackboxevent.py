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

from reactomeneo4j.code.neo4j.reactionlikeevent import ReactionLikeEvent


# pylint: disable=too-few-public-methods
class BlackBoxEvent(ReactionLikeEvent):
    """Reactome ReactionLikeEvent Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name |
    #         stId stIdVersion name isInDisease isInferred releaseDate speciesName
    # params_opt: oldStId releaseStatus | isChimeric systematicName
    # params_opt = ReactionLikeEvent.params_opt + ['definition']

    relationships = {
        **ReactionLikeEvent.relationships, 
        **{
            'figure': set(['Figure']),
            'entityFunctionalStatus': set(['EntityFunctionalStatus']),
            'requiredInputComponent': set(['Complex', 'EntityWithAccessionedSequence']),
            'entityOnOtherCell': set(['PhysicalEntity']),
            'normalReaction': set(['Reaction', 'BlackBoxEvent']),
            'goBiologicalProcess': set(['GO_BiologicalProcess']),
            'regulatedBy': set(['Regulation']),
            'evidenceType'       : set(['EvidenceType']),
        }
    }

    def __init__(self):
        super(BlackBoxEvent, self).__init__('BlackBoxEvent')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.