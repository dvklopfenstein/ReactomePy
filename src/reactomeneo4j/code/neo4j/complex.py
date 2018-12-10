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

  574,228 PhysicalEntity  103000 Complex      9654 103000  0.0937 isChimeric
  574,228 PhysicalEntity  103000 Complex    102974 103000  0.9997 speciesName
  574,228 PhysicalEntity  103000 Complex         7 103000  0.0001 systematicName
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class Complex(PhysicalEntity):
    """Params seen on all Complexes."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_opt = PhysicalEntity.params_opt + ['speciesName', 'isChimeric', 'systematicName']

    relationships = {
        **PhysicalEntity.relationships, 
        **{
            'hasComponent': set(['PhysicalEntity']),
            'entityOnOtherCell': set(['PhysicalEntity']),
            'includedLocation': set(['Compartment']),
        }
    }

    def __init__(self):
        super(Complex, self).__init__('Complex')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
