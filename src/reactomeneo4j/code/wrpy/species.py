"""Print all species in Reactome."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from neo4j import GraphDatabase
from reactomeneo4j.code.wrpy.utils import REPO
from reactomeneo4j.code.wrpy.utils import prt_docstr_module
from reactomeneo4j.code.wrpy.utils import prt_namedtuple
from reactomeneo4j.code.wrpy.utils import prt_dict
from reactomeneo4j.code.wrpy.utils import prt_copyright_comment


class Species(object):
    """Print all species in Reactome."""

    QUERY = 'MATCH (s:Species) RETURN s'

    def __init__(self, password):
        self.gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
        self.dcts = self._init_dcts(set(['name', 'abbreviation', 'displayName', 'taxId']))

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
            for rec in res.records():
                node = rec['s']
                assert node.keys() == flds_exp
                assert node.get('schemaClass') == 'Species'
                key2val = {f:node.get(f) for f in fields_keep}
                key2val['taxId'] = int(key2val['taxId'])
                key2val['abc'] = key2val['abbreviation'].lower()
                species.append(key2val)
        self._chk_cnts(species)
        species = sorted(species, key=lambda d: [d['abc'], d['taxId']])
        return species

    @staticmethod
    def _chk_cnts(species):
        """Expect that taxIds and displayNames are unique while abbreviation is not."""
        num_species = len(species)
        taxids = set()     # 9940
        display = set()    # 'Ovis aries'
        abc = set()        # 'OAR'
        for dct in species:
            taxids.add(dct['taxId'])
            display.add(dct['displayName'])
            abc.add(dct['abbreviation'])
        assert len(taxids) == num_species
        assert len(display) == num_species
        assert len(abc) != num_species


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
