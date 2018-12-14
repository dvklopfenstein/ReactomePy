"""Reactome ChemicalDrug Neo4j Node.

    - PhysicalEntity (dcnt=13)
    -- Drug (dcnt=3)
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
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.drug import Drug


# pylint: disable=too-few-public-methods
class ChemicalDrug(Drug):
    """ChemicalDrug."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    # params: oldStId 

    relationships = {
        **Drug.relationships, 
        **{
            'referenceEntity': set(['referenceMolecule']),
        }
    }

    def __init__(self):
        super(ChemicalDrug, self).__init__('ChemicalDrug')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
