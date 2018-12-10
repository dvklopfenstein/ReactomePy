"""Reactome PhysicalEntity Neo4j Node.

    - Event(dcnt=8)
    -- ReactionLikeEvent(dcnt=5)
  > --- BlackBoxEvent(dcnt=0)
  > --- Depolymerisation(dcnt=0)
  > --- FailedReaction(dcnt=0)
  > --- Polymerisation(dcnt=0)
  > --- Reaction(dcnt=0)
  > -- Pathway(dcnt=1)
  > --- TopLevelPathway(dcnt=0)

  113,854 Event      7702 BlackBoxEvent         1703   7702  0.2211 isChimeric
  113,854 Event      7702 BlackBoxEvent           10   7702  0.0013 systematicName

  113,854 Event        36 Depolymerisation         4     36  0.1111 isChimeric

  113,854 Event       345 FailedReaction         309    345  0.8957 isChimeric
  113,854 Event       345 FailedReaction          72    345  0.2087 systematicName

  113,854 Event       227 Polymerisation          32    227  0.1410 isChimeric
  113,854 Event       227 Polymerisation           2    227  0.0088 systematicName

  113,854 Event     82024 Reaction                 1  82024  0.0000 definition
  113,854 Event     82024 Reaction              7253  82024  0.0884 isChimeric
  113,854 Event     82024 Reaction               137  82024  0.0017 systematicName

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

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Event(DatabaseObject):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_req = DatabaseObject.params_req + \
        ['stId', 'stIdVersion', 'name', 'isInDisease', 'isInferred', 'releaseDate', 'speciesName']
    params_opt = ['oldStId', 'releaseStatus']

    relationships = {
        'literatureReference': set(['Publication']),
        'precedingEvent': set(['Event']),
    }

    def __init__(self, name):
        super(Event, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
