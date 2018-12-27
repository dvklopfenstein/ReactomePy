"""Lists parameters seen on all ReferenceGeneProduct

Hier: ReferenceEntity:ReferenceSequence:ReferenceGeneProduct:ReferenceIsoform

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

from collections import namedtuple
from reactomeneo4j.code.node.referencegeneproduct import ReferenceGeneProduct

# pylint: disable=too-few-public-methods
class ReferenceIsoform(ReferenceGeneProduct):
    """Lists parameters seen on all ReferenceGeneProduct."""

    # req: dbId schemaClass displayName | databaseName identifier url
    # opt: description name geneName | sequenceLength chain checksum comment isSequenceChanged
    #                                  keyword secondaryIdentifier otherIdentifier
    params_req = ReferenceGeneProduct.params_req + ['variantIdentifier']
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    relationships = {
        **ReferenceGeneProduct.relationships,
        **{
            'isoformParent': set(['ReferenceGeneProduct']),
        }
    }

    def __init__(self, dbid=None):
        super(ReferenceIsoform, self).__init__('ReferenceIsoform', dbid)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
