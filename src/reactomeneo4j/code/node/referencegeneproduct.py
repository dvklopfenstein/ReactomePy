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

from collections import namedtuple
from reactomeneo4j.code.node.referencesequence import ReferenceSequence

# pylint: disable=too-few-public-methods
class ReferenceGeneProduct(ReferenceSequence):
    """Lists parameters seen on all ReferenceGeneProduct."""

    # req: dbId schemaClass displayName | databaseName identifier url
    # opt: description | name | geneName
    params_opt = ReferenceSequence.params_opt + [
        'sequenceLength', 'chain', 'checksum', 'comment', 'isSequenceChanged',
        'keyword', 'secondaryIdentifier', 'otherIdentifier']

    prtfmt = '{schemaClass:17} {aart} {displayName}'

    relationships = {
        **ReferenceSequence.relationships,
        **{
            'referenceTranscript': set(['ReferenceRNASequence']),
        }
    }

    ntobj = namedtuple('NtOpj', ' '.join(ReferenceSequence.params_req) + ' aart optional')

    def __init__(self, name="ReferenceGeneProduct", dbid=None):
        super(ReferenceGeneProduct, self).__init__(name, dbid)

    def get_nt(self, node):
        """Given a Neo4j Node, return a namedtuple containing parameters."""
        return self.ntobj(**self.get_dict(node))

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = ReferenceSequence.get_dict(self, node)
        _opt = k2v['optional']
        assert 'aart' not in k2v
        # k2v['aart'] = k2v['aart'] + self._get_ischimeric(_opt)
        k2v['aart'] = self._get_ischimeric(_opt)
        return k2v

    def _get_ischimeric(self, k2vopt):
        if 'isSequenceChanged' not in k2vopt:
            return '.'
        return self.P2A['isSequenceChanged'] if k2vopt['isSequenceChanged'] else 'n'


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
