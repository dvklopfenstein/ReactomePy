"""Reactome PhysicalEntity Neo4j Node.

    - PhysicalEntity (dcnt=13)
    -- EntitySet (dcnt=3)
  > --- CandidateSet (dcnt=0)
  > --- DefinedSet (dcnt=0)
  > --- OpenSet (dcnt=0)
    -- Drug (dcnt=2)
  > --- ChemicalDrug (dcnt=0)
  > --- ProteinDrug (dcnt=0)
  > -- GenomeEncodedEntity (dcnt=1)
  > --- EntityWithAccessionedSequence (dcnt=0)
  > -- Complex (dcnt=0)
  > -- OtherEntity (dcnt=0)
  > -- Polymer (dcnt=0)
  > -- SimpleEntity (dcnt=0)

  574,228 PhysicalEntity  87271 DefinedSet         74  87271  0.0008 isOrdered
  574,228 PhysicalEntity  87271 DefinedSet      86795  87271  0.9945 speciesName
  574,228 PhysicalEntity  87271 DefinedSet          9  87271  0.0001 systematicName

  574,228 PhysicalEntity   9003 CandidateSet        1   9003  0.0001 definition
  574,228 PhysicalEntity   9003 CandidateSet       33   9003  0.0037 isOrdered
  574,228 PhysicalEntity   9003 CandidateSet     8997   9003  0.9993 speciesName
  574,228 PhysicalEntity   9003 CandidateSet        5   9003  0.0006 systematicName

  574,228 PhysicalEntity     19 OpenSet            19     19  1.0000 referenceType
  574,228 PhysicalEntity     19 OpenSet            18     19  0.9474 speciesName
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class EntitySet(PhysicalEntity):
    """Params seen on all EntitySets."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    # params: oldStId
    params_opt = PhysicalEntity.params_opt + ['speciesName', 'isOrdered', 'systematicName']

    relationships = {
        **PhysicalEntity.relationships,
        **{
            'species': set(['Species']),
            'relatedSpecies': set(['Species']),
            'hasMember': set(['PhysicalEntity']),
            'inferredTo': set(['PhysicalEntity']),
        }
    }

    def __init__(self, name='EntitySet'):
        super(EntitySet, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
