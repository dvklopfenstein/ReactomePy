"""Reactome AbstractModifiedResidue Neo4j Node.

  - AbstractModifiedResidue (dcnt=12)
  -- GeneticallyModifiedResidue (dcnt=5)
  --- TranslationalModification (dcnt=3)
> ---- FragmentDeletionModification (dcnt=0)
> ---- FragmentInsertionModification (dcnt=0)
> ---- FragmentReplacedModification (dcnt=0)
> --- ReplacedResidue (dcnt=0)
  -- TranslationalModification (dcnt=5)
  --- TranslationalModification (dcnt=2)
> ---- InterChainTranslationalModification (dcnt=0)
> ---- IntraChainTranslationalModification (dcnt=0)
> --- GroupModifiedResidue (dcnt=0)
> --- ModifiedResidue (dcnt=0)

78,581 AbstractModifiedResidue 95 FragmentReplacedModification 86 95 0.9053 alteredAminoAcidFragment
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.abstractmodifiedresidue import AbstractModifiedResidue


# pylint: disable=too-few-public-methods
class TranslationalModification(AbstractModifiedResidue):
    """TranslationalModification."""

    # params: dbId schemaClass displayName | coordinate
    # params_req = AbstractModifiedResidue.params_req + [
    #     'startPositionInReferenceSequence', 'endPositionInReferenceSequence']

    relationships = {
        **AbstractModifiedResidue.relationships,
        **{
            'psiMod': set(['PsiMod']),
        }
    }

    def __init__(self, name):
        # pylint: disable=useless-super-delegation
        super(TranslationalModification, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
