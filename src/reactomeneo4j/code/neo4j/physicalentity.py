"""Reactome PhysicalEntity Neo4j Node.

    - PhysicalEntity(dcnt=13)
    -- EntitySet(dcnt=3)
  > --- CandidateSet(dcnt=0)
  > --- DefinedSet(dcnt=0)
  > --- OpenSet(dcnt=0)
    -- Drug(dcnt=2)
  > --- ChemicalDrug(dcnt=0)
  > --- ProteinDrug(dcnt=0)
  > -- GenomeEncodedEntity(dcnt=1)
  > --- EntityWithAccessionedSequence(dcnt=0)
  > -- Complex(dcnt=0)
  > -- OtherEntity(dcnt=0)
  > -- Polymer(dcnt=0)
  > -- SimpleEntity(dcnt=0)

  574,228 PhysicalEntity   6094 GenomeEncodedEntity                  3   6094 0.0005 definition
  574,228 PhysicalEntity   6094 GenomeEncodedEntity               6094   6094 1.0000 speciesName

  574,228 PhysicalEntity 363352 EntityWithAccessionedSequence       12 363352 0.0000 definition
  574,228 PhysicalEntity 363352 EntityWithAccessionedSequence   356700 363352 0.9817 endCoordinate
  574,228 PhysicalEntity 363352 EntityWithAccessionedSequence   363352 363352 1.0000 referenceType
  574,228 PhysicalEntity 363352 EntityWithAccessionedSequence   363352 363352 1.0000 speciesName
  574,228 PhysicalEntity 363352 EntityWithAccessionedSequence   356088 363352 0.9800 startCoordinate

  574,228 PhysicalEntity  87271 DefinedSet                          74  87271 0.0008 isOrdered
  574,228 PhysicalEntity  87271 DefinedSet                       86795  87271 0.9945 speciesName
  574,228 PhysicalEntity  87271 DefinedSet                           9  87271 0.0001 systematicName

  574,228 PhysicalEntity   9003 CandidateSet                         1   9003 0.0001 definition
  574,228 PhysicalEntity   9003 CandidateSet                        33   9003 0.0037 isOrdered
  574,228 PhysicalEntity   9003 CandidateSet                      8997   9003 0.9993 speciesName
  574,228 PhysicalEntity   9003 CandidateSet                         5   9003 0.0006 systematicName

  574,228 PhysicalEntity     19 OpenSet                             19     19 1.0000 referenceType
  574,228 PhysicalEntity     19 OpenSet                             18     19 0.9474 speciesName

  574,228 PhysicalEntity 103000 Complex                           9654 103000 0.0937 isChimeric
  574,228 PhysicalEntity 103000 Complex                         102974 103000 0.9997 speciesName
  574,228 PhysicalEntity 103000 Complex                              7 103000 0.0001 systematicName

  574,228 PhysicalEntity   1677 Polymer                              1   1677 0.0006 definition
  574,228 PhysicalEntity   1677 Polymer                              9   1677 0.0054 maxUnitCount
  574,228 PhysicalEntity   1677 Polymer                             65   1677 0.0388 minUnitCount
  574,228 PhysicalEntity   1677 Polymer                           1661   1677 0.9905 speciesName

  574,228 PhysicalEntity    311 OtherEntity                          6    311 0.0193 definition

  574,228 PhysicalEntity   3362 SimpleEntity                         8   3362 0.0024 definition
  574,228 PhysicalEntity   3362 SimpleEntity                      3362   3362 1.0000 referenceType
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class PhysicalEntity(DatabaseObject):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_req = DatabaseObject.params_req + ['stId', 'stIdVersion', 'isInDisease', 'name']
    params_opt = ['oldStId']

    def __init__(self):
        super(PhysicalEntity, self).__init__()


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
