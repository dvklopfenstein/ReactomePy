"""Print all referencedatabase in Reactome."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import collections as cx
from reactomepy.code.wrpy.utils import prt_id2nt
from reactomepy.code.wrpy.utils import REPO
from reactomepy.code.wrpy.utils import prt_docstr_module
from reactomepy.code.wrpy.utils import prt_copyright_comment
from reactomepy.code.node.referencedatabase import ReferenceDatabase


# pylint: disable=too-few-public-methods
class ReferenceDatabases():
    """Print all referencedatabase in Reactome."""

    qry = 'MATCH (node:ReferenceDatabase) RETURN node'
    #### flds_keep = ['dbId', 'displayName', 'accessUrl', 'url']

    def __init__(self, gdbdr):
        self.gdr = gdbdr  # GraphDatabase.driver
        self.referencedatabases = self._init_data()
        #chk_unique(self.referencedatabases, {'displayName':True})
        self.num_dis = len(self.referencedatabases)

    def wrpy_referencedatabase_nts(self, fout_py):
        """Print referencedatabase common names."""
        # Find all referencedatabases which have definitions
        id_nt_lst = sorted(self.referencedatabases.items(), key=lambda t: t[1].displayName)
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            docstr = '{N} ReferenceDatabases in Reactome'.format(N=len(id_nt_lst))
            prt_docstr_module(docstr, prt)
            prt.write('from collections import namedtuple\n\n')
            prt.write('# pylint: disable=line-too-long\n')
            prt_id2nt(id_nt_lst, prt)
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    def _init_data(self):
        """Query for all referencedatabases."""
        id2nt = {}
        ntobj = cx.namedtuple('NtObj', 'displayName accessUrl url')
        with self.gdr.session() as session:
            for rec in session.run(self.qry):
                node = rec['node']
                assert set(node.keys()) == set(ReferenceDatabase.params_req), \
                    'EXP({})\nACT({})'.format(
                        sorted(node.keys()), sorted(ReferenceDatabase.params_req))
                assert node.get('schemaClass') == 'ReferenceDatabase'
                # assert node.get('databaseName') == 'DOID'
                #### key2val = {f:node.get(f) for f in keep}
                ####print(key2val)
                id2nt[node.get('dbId')] = ntobj(
                    displayName=node.get('displayName'),
                    accessUrl=node.get('accessUrl'),
                    url=node.get('url'))
        return id2nt


# Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
