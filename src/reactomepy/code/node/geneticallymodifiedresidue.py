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
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.abstractmodifiedresidue import AbstractModifiedResidue


# pylint: disable=too-few-public-methods
class GeneticallyModifiedResidue(AbstractModifiedResidue):
    """GeneticallyModifiedResidue."""

    # params: dbId schemaClass displayName | coordinate
    # params_req = AbstractModifiedResidue.params_req + [
    #     'startPositionInReferenceSequence', 'endPositionInReferenceSequence']

    #relationships = {
    #    **AbstractModifiedResidue.relationships,
    #    **{
    #    }
    #}

    def __init__(self, name):
        super(GeneticallyModifiedResidue, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
