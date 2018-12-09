"""Lists parameters seen on all ReferenceDNASequence.

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.referencesequence import ReferenceSequence

# pylint: disable=too-few-public-methods
class ReferenceDNASequence(ReferenceSequence):
    """Lists parameters seen on all ReferenceDNASequence."""

    params_opt = ReferenceSequence.params_opt + [
        'sequenceLength', 'otherIdentifier', 'keyword', 'comment']

    def __init__(self):
        super(ReferenceDNASequence, self).__init__('ReferenceDNASequence')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
