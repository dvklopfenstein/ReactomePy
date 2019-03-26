"""Reactome PsiMod Neo4j Node.

  - ExternalOntology (dcnt=3)
> -- Disease (dcnt=0)
> -- PsiMod (dcnt=0)
> -- SequenceOntology (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomepy.code.node.externalontology import ExternalOntology


# pylint: disable=too-few-public-methods
class PsiMod(ExternalOntology):
    """Params seen on all Physical Entities."""

    # req: dbId schemaClass displayName
    params_opt = ExternalOntology.params_opt + ('abbreviation',)
    prtfmt = '{schemaClass}: {abbreviation}{div}{displayName}'
    optstr_dflt = {'div':'', 'abbreviation':''}
    # ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    # relationships = {
    #     'referenceDatabase': frozenset(['ReferenceDatabase']),
    # }

    def __init__(self):
        # pylint: disable=useless-super-delegation
        super(PsiMod, self).__init__('PsiMod')

    def get_optstr(self, optional_dct):
        """Given optional dictionary, return printable strings."""
        k2v = dict(self.optstr_dflt)
        # pylint: disable=no-member
        if not self.optstr_dflt.keys().isdisjoint(optional_dct):
            k2v['div'] = ' '
        if 'abbreviation' in optional_dct:
            k2v['abbreviation'] = 'abbrev({T})'.format(T=optional_dct['abbreviation'])
        return k2v

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
