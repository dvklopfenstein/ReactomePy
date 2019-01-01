"""Reactome GenomeEncodedEntity Neo4j Node.
   Defn GenomeEncodedEntity: A species-specific protein or nucleic acid whose sequence is unknown,
   Defn GenomeEncodedEntity: such as an enzyme that has been characterized functionally
   Defn GenomeEncodedEntity: but not yet purified and sequenced.
   Defn GenomeEncodedEntity:   Example: cytosolic 15-HEDH enzyme

   Hier: PhysicalEntity:GenomeEncodedEntity

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

  574,228 PhysicalEntity    6094 GenomeEncodedEntity                 3   6094 0.0005 definition
  574,228 PhysicalEntity    6094 GenomeEncodedEntity              6094   6094 1.0000 speciesName

  574,228 PhysicalEntity  363352 EntityWithAccessionedSequence      12 363352 0.0000 definition
  574,228 PhysicalEntity  363352 EntityWithAccessionedSequence  356700 363352 0.9817 endCoordinate
  574,228 PhysicalEntity  363352 EntityWithAccessionedSequence  363352 363352 1.0000 referenceType
  574,228 PhysicalEntity  363352 EntityWithAccessionedSequence  363352 363352 1.0000 speciesName
  574,228 PhysicalEntity  363352 EntityWithAccessionedSequence  356088 363352 0.9800 startCoordinate
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.code.node.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class GenomeEncodedEntity(PhysicalEntity):
    """Reactome GenomeEncodedEntity Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_req = PhysicalEntity.params_req + ('speciesName',)
    params_opt = PhysicalEntity.params_opt + ('definition',)
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' aart abc optional')

    relationships = {
        **PhysicalEntity.relationships,
        **{
            'literatureReference': set(['LiteratureReference']),
            'species': set(['Species']),
            'inferredTo': set(['GenomeEncodedEntity']),
            'goCellularComponent': set(['GO_CellularComponent', 'Compartment']),
        }
    }

    def __init__(self, name='GenomeEncodedEntity'):
        super(GenomeEncodedEntity, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
