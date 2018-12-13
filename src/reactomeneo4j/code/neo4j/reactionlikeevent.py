"""Reactome ReactionLikeEvent Neo4j Node.
Defn ReactionLikeEvent: converts inputs into outputs

Hier: Event:ReactionLikeEvent(5)

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

from reactomeneo4j.code.neo4j.event import Event


# pylint: disable=too-few-public-methods
class ReactionLikeEvent(Event):
    """Reactome ReactionLikeEvent Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name |
    #         stId stIdVersion name isInDisease isInferred releaseDate speciesName
    # params_opt: oldStId releaseStatus
    params_opt = Event.params_opt + ['isChimeric', 'systematicName']

    relationships = {
        **Event.relationships,
        **{
            'input': set(['PhysicalEntity']),
            'output': set(['PhysicalEntity']),
            'requiredInputComponent': set(['PhysicalEntity']),
            'catalystActivity': set(['CatalystActivity']),
            'entityFunctionalStatus': set(['EntityFunctionalStatus']),
            'regulatedBy': set(['Regulation']),
            'entityOnOtherCell': set(['PhysicalEntity']),
            'normalReaction': set(['ReactionLikeEvent']),
        }
    }

    def __init__(self, name):
        super(ReactionLikeEvent, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
