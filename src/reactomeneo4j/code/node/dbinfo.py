"""Lists DBInfo parameters."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple


# pylint: disable=too-few-public-methods
class DBInfo():
    """Lists DBInfo parameters."""

    params_req = ('dbId', 'schemaClass', 'name', 'checksum', 'version')
    params_opt = ()
    prtfmt = '{schemaClass} {name} {version} checksum={checksum}'

    ntobj = namedtuple('NtOpj', ' '.join(params_req + ('optional',)))

    def __init__(self):
        self.name = 'DBInfo'

    def get_dict(self, node):
        """Return a Python dict containing all Neo4j Node parameters."""
        k2v = {p:node[p] for p in self.params_req}
        k2v['schemaClass'] = 'DBInfo'
        k2v['dbId'] = -1
        k2v['optional'] = {}
        assert set(self.params_req).difference(set(node.keys())) == {'dbId', 'schemaClass'}, node
        return k2v

    def get_nt(self, node):
        """Return a Python namedtuple containing all Neo4j Node parameters."""
        return self.ntobj(**self.get_dict(node))

    # pylint: disable=unused-argument
    @staticmethod
    def get_optstr(optional_dct):
        """Given optional dictionary, return printable strings."""
        return {}

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
