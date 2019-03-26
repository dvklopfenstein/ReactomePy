"""Print all species in Reactome."""
# TBD: Not complete.

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import collections as cx
import timeit
import datetime
from reactomepy.code.wrpy.utils import REPO
from reactomepy.code.wrpy.utils import prt_docstr_module
from reactomepy.code.wrpy.utils import prt_namedtuple
from reactomepy.code.wrpy.utils import prt_dict
from reactomepy.code.wrpy.utils import prt_copyright_comment
from reactomepy.code.utils import chk_unique


class InferredFrom(object):
    """Print to Python all inferred Pathways and the Pathway that they are inferred from."""

    QUERY = 'MATCH (hi:Pathway)<-[inferredTo]-(lo:Pathway{speciesName:"Mus musculus"}) RETURN hi, lo'

    def __init__(self, gdbdr):
        self.gdbdr = gdbdr  # GraphDatabase.driver
        self.dcts = self._init_dcts(set(['name', 'abbreviation', 'displayName', 'taxId']))
        # chk_unique(self.dcts, {'taxId':True, 'displayName':True, 'abbreviation':False})

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
        """Determine pathways that are determined from another species."""
        org2plo2phi = cx.defaultdict(lambda: cx.defaultdict(set))
        tic = timeit.default_timer()
        with self.gdbdr.session() as session:
            res = session.run(self.QUERY)
            for rec in res.records():
                assert rec['lo']['isInferred']
                # if not rec['hi']['isInferred']:
                print(rec['hi'])
                pidlo = rec['lo']['stId']
                abc = pidlo.split('-')[1].lower()
                org2plo2phi[abc][pidlo].add(rec['hi']['stId'])
        print('{N} species pathways are inferred from other species'.format(N=len(org2plo2phi)))
        print(sorted(org2plo2phi.keys()))
        self.chk_cnts(org2plo2phi)
        hms = str(datetime.timedelta(seconds=(timeit.default_timer()-tic)))
        print('HMS {HMS} {N} species'.format(HMS=hms, N=len(org2plo2phi)))
        return org2plo2phi

    def chk_cnts(self, org2plo2phi):
        """Test if each Pathway was inferred from a single species in another species."""
        ctr = cx.Counter()
        for org, plo2phi in org2plo2phi.items():
            for plo, phi in plo2phi.items():
                ctr['all'] += 1
                if len(phi) != 1:
                    ctr['mult'] += 1
                    # if 'HSA' in plo:
                    #     print('{LO} inferred from {HI}'.format(LO=plo, HI=phi))
        print(ctr.most_common())


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
