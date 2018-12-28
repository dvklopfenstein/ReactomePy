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
    # opt: geneName otherIdentifier description name comment sequenceLength keyword |
    #      chain checksum isSequenceChanged secondaryIdentifier
    params_req = ReferenceGeneProduct.params_req + ['variantIdentifier']

    ntobj = namedtuple('NtObj', ' '.join(params_req) + ReferenceGeneProduct.flds_last)

    relationships = {
        **ReferenceGeneProduct.relationships,
        **{
            'isoformParent': set(['ReferenceGeneProduct']),
        }
    }

    def __init__(self):
        super(ReferenceIsoform, self).__init__('ReferenceIsoform')

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        return ReferenceGeneProduct.get_dict(self, node)

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
