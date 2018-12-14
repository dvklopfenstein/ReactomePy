"""Reactome Pathway Neo4j Node.

    - Event (dcnt=8)
    -- ReactionLikeEvent (dcnt=5)
  > --- BlackBoxEvent (dcnt=0)
  > --- Depolymerisation (dcnt=0)
  > --- FailedReaction (dcnt=0)
  > --- Polymerisation (dcnt=0)
  > --- Reaction (dcnt=0)
  > -- Pathway (dcnt=0)
  > -- TopLevelPathway (dcnt=0)

  113,854 Event     23080 Pathway                 15  23080  0.0006 definition
  113,854 Event     23080 Pathway               7915  23080  0.3429 diagramHeight
  113,854 Event     23080 Pathway               7915  23080  0.3429 diagramWidth
  113,854 Event     23080 Pathway                414  23080  0.0179 doi
  113,854 Event     23080 Pathway              23080  23080  1.0000 hasDiagram

  113,854 Event       440 TopLevelPathway        440    440  1.0000 diagramHeight
  113,854 Event       440 TopLevelPathway        440    440  1.0000 diagramWidth
  113,854 Event       440 TopLevelPathway          5    440  0.0114 doi
  113,854 Event       440 TopLevelPathway        440    440  1.0000 hasDiagram
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.event import Event


# pylint: disable=too-few-public-methods
class TopLevelPathway(Event):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    #         stId stIdVersion name isInDisease isInferred releaseDate speciesName
    params_req = Event.params_req + ['hasDiagram', 'diagramHeight', 'diagramWidth']
    # params: oldStId releaseStatus
    params_opt = Event.params_opt + ['doi']

    relationships = {
        **Event.relationships, 
        **{
            'figure': set(['Figure']),
            'hasEvent': set(['ReactionLikeEvent', 'Pathway']),
            'hasEncapsulatedEvent': set(['Pathway', 'TopLevelPathway']),
            'goBiologicalProcess': set(['GO_BiologicalProcess']),
            'evidenceType': set(['EvidenceType']),
        }
    }

    def __init__(self):
        super(TopLevelPathway, self).__init__('TopLevelPathway')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
