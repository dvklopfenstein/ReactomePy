"""Print all species in Reactome."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from reactomepy.code.wrpy.utils import REPO
from reactomepy.code.wrpy.utils import prt_docstr_module
from reactomepy.code.wrpy.utils import prt_namedtuple
from reactomepy.code.wrpy.utils import prt_dict
from reactomepy.code.wrpy.utils import prt_copyright_comment
from reactomepy.code.utils import chk_unique


class Species(object):
    """Print all species in Reactome."""

    QUERY = 'MATCH (node:Species) RETURN node'

    def __init__(self, gdbdr):
        self.gdbdr = gdbdr  # GraphDatabase.driver
        self.dcts = self._init_dcts(set(['name', 'abbreviation', 'displayName', 'taxId']))
        chk_unique(self.dcts, {'taxId':True, 'displayName':True, 'abbreviation':False})

    def wrpy_info(self, fout_py):
        """Print Reactome species main information."""
        fields = ['abc', 'abbreviation', 'taxId', 'displayName']
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt_docstr_module('Species in Reactome', prt)
            prt.write('import collections as cx\n\n')
            prt_namedtuple(self.dcts, 'SPECIES', fields, prt)
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    def wrpy_common_names(self, fout_py):
        """Print species common names."""
        taxid2namesalt = self._get_taxid2commonnames()
        with open(os.path.join(fout_py), 'w') as prt:
            prt_docstr_module('Common name for the species in Reactome', prt)
            prt.write('# pylint: disable=line-too-long\n')
            taxid_names = sorted(taxid2namesalt.items())
            prt_dict(taxid_names, 'TAXID2NAMES', afmt='{A}', bfmt=None, prt=prt)
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    def _get_taxid2commonnames(self):
        """Get the common names for each taxid."""
        taxid2names = {}
        for dct in self.dcts:
            # Do not include the displayName because it is already stored
            name_official = dct['displayName']
            names = [n for n in dct['name'] if n != name_official]
            if names:
                taxid2names[dct['taxId']] = names
        return taxid2names

    def _init_dcts(self, fields_keep):
        """Read species information in Reactome."""
        species = []
        with self.gdbdr.session() as session:
            flds_exp = set(['name', 'schemaClass', 'abbreviation', 'displayName', 'taxId', 'dbId'])
            res = session.run(self.QUERY)
            for rec in res.data():
                node = rec['node']
                assert node.keys() == flds_exp
                assert node.get('schemaClass') == 'Species'
                key2val = {f:node.get(f) for f in fields_keep}
                key2val['taxId'] = int(key2val['taxId'])
                key2val['abc'] = key2val['abbreviation'].lower()
                species.append(key2val)
        species = sorted(species, key=lambda d: [d['abc'], d['taxId']])
        return species


# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
