"""Reactome SimpleEntity Neo4j Node.
   Defn SimpleEntity: Other fully characterized molecules
   Defn SimpleEntity:   Example: 'nucleoplasmic ATP' or 'cytosolic glutathione'

   Hier: PhysicalEntity:SimpleEntity

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

  574,228 SimpleEntity   3362 SimpleEntity       8   3362  0.0024 definition
  574,228 SimpleEntity   3362 SimpleEntity    3362   3362  1.0000 referenceType
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class SimpleEntity(PhysicalEntity):
    """Reactome SimpleEntity Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_req = PhysicalEntity.params_req + ['referenceType']
    params_opt = PhysicalEntity.params_opt + ['definition']

    relationships = {
        **PhysicalEntity.relationships, 
        **{
            'figure': set(['Figure']),
            'referenceEntity': set(['ReferenceMolecule']),
            'goCellularComponent': set(['GO_CellularComponent', 'Compartment']),
        }
    }

    def __init__(self):
        super(SimpleEntity, self).__init__('SimpleEntity')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
