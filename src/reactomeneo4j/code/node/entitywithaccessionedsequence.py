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

574,228 GenomeEncodedEntity   6094 GenomeEncodedEntity                3   6094 0.0 definition
574,228 GenomeEncodedEntity   6094 GenomeEncodedEntity             6094   6094 1.0 speciesName

574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence     12 363352 0.0 definition
574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence 356700 363352 0.9 endCoordinate
574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence 363352 363352 1.0 referenceType
574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence 363352 363352 1.0 speciesName
574,228 GenomeEncodedEntity 363352 EntityWithAccessionedSequence 356088 363352 0.9 startCoordinate
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.code.node.genomeencodedentity import GenomeEncodedEntity


# pylint: disable=too-few-public-methods
class EntityWithAccessionedSequence(GenomeEncodedEntity):
    """Reactome EntityWithAccessionedSequence Neo4j Node."""

    # dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name | speciesName
    params_req = GenomeEncodedEntity.params_req + ('referenceType',)
    # oldStId definition
    params_opt = GenomeEncodedEntity.params_opt + ('startCoordinate', 'endCoordinate', 'definition')
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' aart abc optional')

    relationships = {
        **GenomeEncodedEntity.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference', 'Book']),
            'inferredTo': frozenset(['DefinedSet',
                                     'GenomeEncodedEntity', 'EntityWithAccessionedSequence']),
            'goCellularComponent': frozenset(['GO_CellularComponent', 'Compartment']),
            # 'hasModifiedResidue': frozenset(['AbstractModifiedResidue']),
            'hasModifiedResidue': frozenset([
                'FragmentDeletionModification',
                'FragmentInsertionModification',
                'FragmentReplacedModification',
                'ReplacedResidue',
                'InterChainCrosslinkedResidue',
                'IntraChainCrosslinkedResidue',
                'GroupModifiedResidue',
                'ModifiedResidue']),
            # 'referenceEntity': frozenset(['ReferenceSequence']),
            'referenceEntity': frozenset([
                'ReferenceGeneProduct',
                'ReferenceIsoform',
                'ReferenceDNASequence',
                'ReferenceRNASequence']),
        }
    }

    def __init__(self):
        super(EntityWithAccessionedSequence, self).__init__('EntityWithAccessionedSequence')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
