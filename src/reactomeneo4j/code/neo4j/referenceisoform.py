"""Lists parameters seen on all ReferenceGeneProduct

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

from reactomeneo4j.code.neo4j.referencegeneproduct import ReferenceGeneProduct

# pylint: disable=too-few-public-methods
class ReferenceIsoform(ReferenceGeneProduct):
    """Lists parameters seen on all ReferenceGeneProduct."""

    params_req = ReferenceGeneProduct.params_req + ['variantIdentifier']

    def __init__(self):
        super(ReferenceIsoform, self).__init__('ReferenceIsoform')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
