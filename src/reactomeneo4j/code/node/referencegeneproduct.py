"""Lists parameters seen on all ReferenceGeneProduct

   Hier: ReferenceEntity:ReferenceSequence:ReferenceGeneProduct

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)


1,031,812 ReferenceEntity    1593 ReferenceIsoform         1593   1593  1.0000 variantIdentifier
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.referencesequence import ReferenceSequence

# pylint: disable=too-few-public-methods
class ReferenceGeneProduct(ReferenceSequence):
    """Lists parameters seen on all ReferenceGeneProduct."""

    params_opt = ReferenceSequence.params_opt + [
        'sequenceLength', 'chain', 'checksum', 'comment', 'isSequenceChanged',
        'keyword', 'secondaryIdentifier', 'otherIdentifier']

    relationships = {
        **ReferenceSequence.relationships, 
        **{
            'referenceTranscript': set(['ReferenceRNASequence']),
        }
    }

    def __init__(self, name="ReferenceGeneProduct"):
        super(ReferenceGeneProduct, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
