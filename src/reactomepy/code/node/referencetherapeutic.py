"""Lists parameters seen on all ReferenceTherapeutic..

Hier: ReferenceEntity:ReferenceTherapeutic

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)

1,031,812 ReferenceEntity     139 ReferenceTherapeutic      139    139  1.0000 name
1,031,812 ReferenceEntity     139 ReferenceTherapeutic      139    139  1.0000 approved

1,031,812 ReferenceEntity     139 ReferenceTherapeutic        1    139  0.0072 abbreviation
1,031,812 ReferenceEntity     139 ReferenceTherapeutic       84    139  0.6043 approvalSource
1,031,812 ReferenceEntity     139 ReferenceTherapeutic      111    139  0.7986 inn
1,031,812 ReferenceEntity     139 ReferenceTherapeutic      131    139  0.9424 type
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomepy.code.node.referenceentity import ReferenceEntity

# pylint: disable=too-few-public-methods
class ReferenceTherapeutic(ReferenceEntity):
    """Lists parameters seen on all ReferenceTherapeutic."""

    # req: dbId schemaClass displayName | databaseName identifier url
    params_req = ReferenceEntity.params_req + ('name', 'approved')
    params_opt = ReferenceEntity.params_opt + ('approvalSource', 'type', 'inn', 'abbreviation')
    prtfmt = ('{dbId:7} {schemaClass:32} {abc}{databaseName}:{identifier} {firstName}'
              '{abbreviation}{type}{approvalSource}')
    optstr_dflt = {'abbreviation': '', 'type':'', 'approvalSource':''}

    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' firstName' + ReferenceEntity.flds_last)

    def __init__(self):
        super(ReferenceTherapeutic, self).__init__('ReferenceTherapeutic')

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = ReferenceEntity.get_dict(self, node)
        # speciesName is not a param, but species may be found through relationship
        k2v['firstName'] = self._get_firstname(k2v['optional'], k2v)
        return k2v

    @staticmethod
    def _get_firstname(optional, k2v):
        """Get first name to be used as the display name."""
        if 'inn' in optional:
            return optional['inn']
        return k2v['name'][0]

    def get_optstr(self, optional_dct):
        """Given optional dictionary, return printable strings."""
        k2v = dict(self.optstr_dflt)
        if 'abbreviation' in optional_dct:
            k2v['abbreviation'] = ' ({ABC})'.format(ABC=optional_dct['abbreviation'])
        if 'type' in optional_dct:
            k2v['type'] = ' ({TYPE})'.format(TYPE=optional_dct['type'])
        if 'approvalSource' in optional_dct:
            k2v['approvalSource'] = ' Approved[{SRC}]'.format(
                SRC=', '.join(optional_dct['approvalSource']))
        else:
            k2v['approvalSource'] = ' Approved[-]'
        return k2v

    def get_nt(self, node):
        """Given a Neo4j Node, return a namedtuple containing parameters."""
        return self.ntobj(**self.get_dict(node))

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
