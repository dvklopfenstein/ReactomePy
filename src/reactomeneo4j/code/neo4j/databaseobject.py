"""Lists parameters seen on all DatabaseObjects."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.data.species import SPECIES


# pylint: disable=too-few-public-methods
class DatabaseObject():
    """Lists parameters seen on all DatabaseObjects."""

    params_req = ['dbId', 'schemaClass', 'displayName']
    params_opt = []
    fmtpat = '{dbId:7} {schemaClass:32} {displayName}'
    species2nt = {nt.displayName:nt for nt in SPECIES}

    def __init__(self, name):
        self.name = name
        self.ntobj = namedtuple('NtOpj', ' '.join(self.params_req + ['optional']))

    def get_dict(self, node):
        """Return a Python dict containing all Neo4j Node parameters."""
        k2v = {p:node[p] for p in self.params_req}
        k2v['optional'] = {o:node[o] for o in self.params_opt if o in node}
        return k2v

    def get_nt(self, node):
        """Return a Python namedtuple containing all Neo4j Node parameters."""
        return self.ntobj(**self.get_dict(node))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
