"""Print all disease in Reactome."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from reactomepy.code.wrpy.utils import REPO
from reactomepy.code.wrpy.utils import prt_docstr_module
# from reactomepy.code.wrpy.utils import prt_namedtuple
from reactomepy.code.wrpy.utils import prt_dict
from reactomepy.code.wrpy.utils import prt_copyright_comment
from reactomepy.code.neo4jnode import Neo4jNode


class Diseases(object):
    """Print all disease in Reactome."""

    dis_qry = 'MATCH (node:Disease) RETURN node'
    dis_keep = set(['displayName', 'definition', 'synonym', 'name'])

    def __init__(self, gdbdr):
        self.gdr = gdbdr  # GraphDatabase.driver
        self.diseases = self._init_disease()
        self.num_dis = len(self.diseases)

    def wrpy_disease2fld(self, fout_py, field, varname):
        """Print disease common names."""
        # Find all diseases which have definitions
        dis2val = self._get_dis2fldval(field)
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            docstr = '{N} of {M} diseases in Reactome have definitions'.format(
                M=self.num_dis, N=len(dis2val))
            prt_docstr_module(docstr, prt)
            prt.write('# pylint: disable=line-too-long\n')
            disease_names = sorted(dis2val.items())
            prt_dict(disease_names, varname, afmt='"{A}"', bfmt='"{B}"', prt=prt)
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    def _get_dis2fldval(self, field):
        """Get all diseases that have definitions."""
        dis2val = {}
        for dct in self.diseases:
            val = dct[field]
            if val is not None:
                dis2val[dct['displayName']] = val
        return dis2val

    def _init_disease(self):
        """Query for all diseases."""
        disease = []
        # fields_exp = set(['name', 'schemaClass', 'abbreviation', 'displayName', 'taxId', 'dbId'])
        passed = True
        with self.gdr.session() as session:
            for rec in session.run(self.dis_qry):
                node = rec['node']
                assert node.get('schemaClass') == 'Disease'
                assert node.get('databaseName') == 'DOID'
                key2val = {f:node.get(f) for f in self.dis_keep}
                disease.append(key2val)
        disease = sorted(disease, key=lambda d: d['displayName'])
        if not passed:
            raise RuntimeError('**FATAL: NOT UNIQUE: displayName')
        return disease


# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
