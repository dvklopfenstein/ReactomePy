"""Lists parameters seen on all ReferenceMolecule..

Hier: ReferenceEntity:ReferenceMolecule

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)

1,031,812 ReferenceEntity   1978 ReferenceMolecule   1978 1978  1.0000 dbId
1,031,812 ReferenceEntity   1978 ReferenceMolecule   1978 1978  1.0000 schemaClass
1,031,812 ReferenceEntity   1978 ReferenceMolecule   1978 1978  1.0000 displayName

1,031,812 ReferenceEntity   1978 ReferenceMolecule   1978 1978  1.0000 databaseName
1,031,812 ReferenceEntity   1978 ReferenceMolecule   1978 1978  1.0000 identifier
1,031,812 ReferenceEntity   1978 ReferenceMolecule   1978 1978  1.0000 name
1,031,812 ReferenceEntity   1978 ReferenceMolecule   1978 1978  1.0000 url

1,031,812 ReferenceEntity   1978 ReferenceMolecule   1948 1978  0.9848 trivial
1,031,812 ReferenceEntity   1978 ReferenceMolecule   1835 1978  0.9277 formula
1,031,812 ReferenceEntity   1978 ReferenceMolecule     30 1978  0.0152 geneName
1,031,812 ReferenceEntity   1978 ReferenceMolecule     30 1978  0.0152 secondaryIdentifier
1,031,812 ReferenceEntity   1978 ReferenceMolecule      1 1978  0.0005 otherIdentifier
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.code.node.referenceentity import ReferenceEntity

# pylint: disable=too-few-public-methods
class ReferenceMolecule(ReferenceEntity):
    """Lists parameters seen on all ReferenceMolecule."""

    # req: dbId schemaClass displayName | databaseName identifier url
    params_req = ReferenceEntity.params_req + ['name']
    params_opt = ReferenceEntity.params_opt + [
        'secondaryIdentifier', 'otherIdentifier', 'formula', 'trivial', 'geneName']
    prtfmt = ('{dbId:7} {schemaClass:32} {abc}{databaseName}:{identifier} {firstName}'
              '{div}{formula}{trivial}')
    optstr_dflt = {'div':'', 'formula':'', 'trivial':''}

    ntobj = namedtuple('NtOpj', ' '.join(params_req) + ' firstName' + ReferenceEntity.flds_last)

    def __init__(self):
        super(ReferenceMolecule, self).__init__('ReferenceMolecule')

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = ReferenceEntity.get_dict(self, node)
        k2v['firstName'] = k2v['name'][0]
        return k2v

    def get_optstr(self, optional_dct):
        """Given optional dictionary, return printable strings."""
        k2v = dict(self.optstr_dflt)
        # pylint: disable=no-member
        if not self.optstr_dflt.keys().isdisjoint(optional_dct):
            k2v['div'] = ' |'
        if 'formula' in optional_dct:
            k2v['formula'] = ' {F}'.format(F=optional_dct['formula'])
        if 'trivial' in optional_dct:
            k2v['trivial'] = ' trivial={T}'.format(T=int(optional_dct['trivial']))
        return k2v

    def get_nt(self, node):
        """Given a Neo4j Node, return a namedtuple containing parameters."""
        return self.ntobj(**self.get_dict(node))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
