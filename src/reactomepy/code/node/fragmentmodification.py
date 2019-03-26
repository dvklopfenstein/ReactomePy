"""Reactome AbstractModifiedResidue Neo4j Node.

  - AbstractModifiedResidue (dcnt=12)
  -- GeneticallyModifiedResidue (dcnt=5)
  --- FragmentModification (dcnt=3)
> ---- FragmentDeletionModification (dcnt=0)
> ---- FragmentInsertionModification (dcnt=0)
> ---- FragmentReplacedModification (dcnt=0)
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

from collections import namedtuple
from reactomepy.code.node.geneticallymodifiedresidue import GeneticallyModifiedResidue


# pylint: disable=too-few-public-methods
class FragmentModification(GeneticallyModifiedResidue):
    """FragmentModification."""

    # params: dbId schemaClass displayName | coordinate
    params_req = GeneticallyModifiedResidue.params_req + (
        'startPositionInReferenceSequence',
        'endPositionInReferenceSequence')
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    # relationships = {
    #     **GeneticallyModifiedResidue.relationships,
    #     **{
    #     }
    # }

    def __init__(self, name):
        # pylint: disable=useless-super-delegation
        super(FragmentModification, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
