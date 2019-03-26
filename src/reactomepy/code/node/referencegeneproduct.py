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
from reactomepy.code.node.referenceentity import ReferenceEntity
from reactomepy.code.node.referencesequence import ReferenceSequence

# pylint: disable=too-few-public-methods
class ReferenceGeneProduct(ReferenceSequence):
    """Lists parameters seen on all ReferenceGeneProduct."""

    # req: dbId schemaClass displayName | databaseName identifier url
    # opt: geneName otherIdentifier description name comment sequenceLength keyword
    params_opt = ReferenceSequence.params_opt + \
        ('chain', 'checksum', 'isSequenceChanged', 'secondaryIdentifier')  # params_opt =

    prtfmt_gene = '{div}{sequenceLength}{checksum}{chain}'
    prtfmt = '{dbId:8} {schemaClass} {abc} {aart} {displayName}' + prtfmt_gene
    optstr_dflt = {'div':'', 'sequenceLength':'', 'checksum':'', 'chain':''}

    relationships = {
        **ReferenceSequence.relationships,
        **{
            'referenceTranscript': frozenset(['ReferenceRNASequence']),
        }
    }

    flds_last = ' aart' + ReferenceEntity.flds_last
    #### ntobj = namedtuple('NtOpj', ' '.join(ReferenceSequence.params_req) + flds_last)
    ntobj = namedtuple('NtObj', ' '.join(ReferenceEntity.params_req) + flds_last)

    def __init__(self, name="ReferenceGeneProduct"):
        super(ReferenceGeneProduct, self).__init__(name)

    def get_nt(self, node):
        """Given a Neo4j Node, return a namedtuple containing parameters."""
        return self.ntobj(**self.get_dict(node))

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = ReferenceEntity.get_dict(self, node)
        self.set_dict(k2v)
        return k2v

    def get_optstr(self, optional_dct):
        """Given optional dictionary, return printable strings."""
        k2v = dict(self.optstr_dflt)
        # pylint: disable=no-member
        if not self.optstr_dflt.keys().isdisjoint(optional_dct):
            k2v['div'] = ' |'
        if 'sequenceLength' in optional_dct:
            k2v['sequenceLength'] = ' {BPs} bps'.format(BPs=optional_dct['sequenceLength'])
        if 'checksum' in optional_dct:
            k2v['checksum'] = ' checksum={C}'.format(C=optional_dct['checksum'])
        if 'chain' in optional_dct:
            chain = optional_dct['chain']
            k2v['chain'] = ' chain[{N}]=[{C}]'.format(N=len(chain), C='; '.join(chain))
        return k2v

    def set_dict(self, k2v):
        """Add additional required namedtuple fields not found in the Neo4j Node parameters."""
        _opt = k2v['optional']
        assert 'aart' not in k2v
        k2v['aart'] = self._get_issequencechanged(_opt)

    def _get_issequencechanged(self, k2vopt):
        if 'isSequenceChanged' not in k2vopt:
            return '.'
        return self.P2A['isSequenceChanged'] if k2vopt['isSequenceChanged'] else 'n'


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
