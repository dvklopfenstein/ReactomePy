"""Reactome EntityWithAccessionedSequence Neo4j Node.
   Defn EntityWithAccessionedSequence: Proteins and nucleic acids with known sequences.

    - GenomeEncodedEntity (dcnt=13)
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

  574,228 GenomeEncodedEntity   6094 GenomeEncodedEntity                  3   6094 0.0005 definition
  574,228 GenomeEncodedEntity   6094 GenomeEncodedEntity               6094   6094 1.0000 speciesName

  574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence       12 363352 0.0000 definition
  574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence   356700 363352 0.9817 endCoordinate
  574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence   363352 363352 1.0000 referenceType
  574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence   363352 363352 1.0000 speciesName
  574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence   356088 363352 0.9800 startCoordinate
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.genomeencodedentity import GenomeEncodedEntity


# pylint: disable=too-few-public-methods
class EntityWithAccessionedSequence(GenomeEncodedEntity):
    """Reactome EntityWithAccessionedSequence Neo4j Node."""

    # dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name | speciesName
    params_req = GenomeEncodedEntity.params_req + ['referenceType']
    # oldStId definition
    params_opt = GenomeEncodedEntity.params_opt + ['startCoordinate', 'endCoordinate', 'definition']

    relationships = {
        **GenomeEncodedEntity.relationships,
        **{
            'inferredTo': set(['EntityWithAccessionedSequence', 'GenomeEncodedEntity', 'DefinedSet']),
            'hasModifiedResidue': set(['AbstractModifiedResidue']),
            'referenceEntity': set(['ReferenceSequence']),
            'goCellularComponent': set(['GO_CellularComponent', 'Compartment']),
        }
    }

    def __init__(self):
        super(EntityWithAccessionedSequence, self).__init__('EntityWithAccessionedSequence')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
