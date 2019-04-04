"""Reactome AbstractModifiedResidue Neo4j Node.

  - AbstractModifiedResidue (dcnt=12)
  -- GeneticallyModifiedResidue (dcnt=5)
  --- FragmentModification (dcnt=3)
> ---- FragmentDeletionModification (dcnt=0)
> ---- FragmentInsertionModification (dcnt=0)
> ---- FragmentReplacedModification (dcnt=0)
> --- ReplacedResidue (dcnt=0)
  -- TranslationalModification (dcnt=5)
  --- CrosslinkedResidue (dcnt=2)
> ---- InterChainCrosslinkedResidue (dcnt=0)
> ---- IntraChainCrosslinkedResidue (dcnt=0)
> --- GroupModifiedResidue (dcnt=0)
> --- ModifiedResidue (dcnt=0)

78,581 AbstractModifiedResidue:
3006 InterChainCrosslinkedResidue  388 3006  0.1291 secondCoordinate
 329 IntraChainCrosslinkedResidue   49  329  0.1489 secondCoordinate

  95 FragmentReplacedModification   86   95  0.9053 alteredAminoAcidFragment
  95 FragmentReplacedModification   95   95  1.0000 endPositionInReferenceSequence
  95 FragmentReplacedModification   95   95  1.0000 startPositionInReferenceSequence

  63 FragmentInsertionModification  63   63  1.0000 endPositionInReferenceSequence
  63 FragmentInsertionModification  63   63  1.0000 startPositionInReferenceSequence

  46 FragmentDeletionModification   46   46  1.0000 endPositionInReferenceSequence
  46 FragmentDeletionModification   46   46  1.0000 startPositionInReferenceSequence
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.translationalmodification import TranslationalModification


# pylint: disable=too-few-public-methods
class GroupModifiedResidue(TranslationalModification):
    """GroupModifiedResidue."""

    # params_req: dbId schemaClass displayName
    params_req = TranslationalModification.params_req + ('label',)
    # params_opt: coordinate

    relationships = {
        **TranslationalModification.relationships,
        **{
            'modification': frozenset(['Polymer', 'ReferenceGroup', 'DefinedSet']),
            'referenceSequence': frozenset(['ReferenceGeneProduct', 'ReferenceIsoform']),
        }
    }

    def __init__(self):
        super(GroupModifiedResidue, self).__init__('GroupModifiedResidue')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
