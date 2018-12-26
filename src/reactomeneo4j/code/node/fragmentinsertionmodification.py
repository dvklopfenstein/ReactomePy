"""Reactome AbstractModifiedResidue Neo4j Node.

  - AbstractModifiedResidue (dcnt=12)
  -- GeneticallyModifiedResidue (dcnt=5)
  --- FragmentModification (dcnt=3)
> ---- FragmentDeletionModification (dcnt=0)
> ---- FragmentInsertionModification (dcnt=0)
> ---- FragmentInsertionModification (dcnt=0)
> --- ReplacedResidue (dcnt=0)
  -- TranslationalModification (dcnt=5)
  --- FragmentModification (dcnt=2)
> ---- InterChainFragmentModification (dcnt=0)
> ---- IntraChainFragmentModification (dcnt=0)
> --- GroupModifiedResidue (dcnt=0)
> --- ModifiedResidue (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.fragmentmodification import FragmentModification


# pylint: disable=too-few-public-methods
class FragmentInsertionModification(FragmentModification):
    """FragmentInsertionModification."""

    # params: dbId schemaClass displayName | coordinate |
    #     startPositionInReferenceSequence endPositionInReferenceSequence
    #### params_opt = FragmentModification.params_opt + ['alteredAminoAcidFragment']

    relationships = {
        **FragmentModification.relationships,
        **{
            'referenceSequence': set(['ReferenceGeneProduct', 'ReferenceIsoform']),
        }
    }

    def __init__(self, dbid=None):
        super(FragmentInsertionModification, self).__init__('FragmentInsertionModification', dbid)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
