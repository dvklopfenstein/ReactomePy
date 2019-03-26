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

from reactomepy.code.node.event import Event


# pylint: disable=too-few-public-methods
class ReactionLikeEvent(Event):
    """Reactome ReactionLikeEvent Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name |
    #         stId stIdVersion name isInDisease isInferred releaseDate speciesName
    # params_opt: oldStId releaseStatus
    params_opt = Event.params_opt + ('isChimeric', 'systematicName')

    relationships = {
        **Event.relationships,
        **{
            #'precedingEvent': frozenset(['Event']),
            'relatedSpecies': frozenset(['Species']),
            #'input': frozenset(['PhysicalEntity']),
            #'output': frozenset(['PhysicalEntity']),
            #'requiredInputComponent': frozenset(['PhysicalEntity']),
            'catalystActivity': frozenset(['CatalystActivity']),
            #'entityFunctionalStatus': frozenset(['EntityFunctionalStatus']),
            #'regulatedBy': frozenset(['Regulation']),
            #'entityOnOtherCell': frozenset(['PhysicalEntity']),
            #'normalReaction': frozenset(['ReactionLikeEvent']),
        }
    }

    def __init__(self, name):
        super(ReactionLikeEvent, self).__init__(name)

    def get_nt(self, node):
        """Given a Neo4j Node, return a namedtuple containing parameters."""
        return self.ntobj(**Event.get_dict(self, node))

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = Event.get_dict(self, node)
        _opt = k2v['optional']
        k2v['aart'] = k2v['aart'] + self._get_ischimeric(_opt)
        return k2v

    def _get_ischimeric(self, k2vopt):
        if 'isChimeric' not in k2vopt:
            return '.'
        return self.P2A['isChimeric'] if k2vopt['isChimeric'] else 'n'

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
