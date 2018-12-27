"""Reactome Pathway Neo4j Node.
Defn Pathway: grouping of related Events

Hier: Event:Pathway

    - Event (dcnt=8)
    -- ReactionLikeEvent (dcnt=5)
  > --- BlackBoxEvent (dcnt=0)
  > --- Depolymerisation (dcnt=0)
  > --- FailedReaction (dcnt=0)
  > --- Polymerisation (dcnt=0)
  > --- Reaction (dcnt=0)
  > -- Pathway (dcnt=1)
  > --- TopLevelPathway (dcnt=0)

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

from collections import namedtuple
from reactomeneo4j.code.node.event import Event


# pylint: disable=too-few-public-methods
class Pathway(Event):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    #         stId stIdVersion name isInDisease isInferred releaseDate speciesName
    params_req = Event.params_req + ['hasDiagram']
    # params: oldStId releaseStatus
    params_opt = Event.params_opt + ['doi', 'diagramHeight', 'diagramWidth', 'definition']
    ntobj = namedtuple('NtObj', ' '.join(params_req) + Event.flds_last)

    relationships = {
        **Event.relationships,
        **{
            'literatureReference': set(['LiteratureReference', 'Book', 'URL']),
            'inferredTo': set(['Pathway']),
            'figure': set(['Figure']),
            'relatedSpecies': set(['Species']),
            'crossReference': set(['DatabaseIdentifier']),
            'hasEvent': set(['Pathway', 'Reaction', 'FailedReaction', 'BlackBoxEvent', 'Depolymerisation', 'Polymerisation']),
            'precedingEvent': set(['Pathway', 'Reaction', 'BlackBoxEvent']),
            'hasEncapsulatedEvent': set(['Pathway']),
            'normalPathway': set(['Pathway']),
            'goBiologicalProcess': set(['GO_BiologicalProcess']),
            'evidenceType': set(['EvidenceType']),
        }
    }

    def __init__(self):
        super(Pathway, self).__init__('Pathway')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
