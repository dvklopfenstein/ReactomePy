"""Lists parameters seen on all DatabaseObjects."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple

# pylint: disable=too-few-public-methods
class DatabaseObject():
    """Lists parameters seen on all DatabaseObjects."""

    params_req = ['dbId', 'schemaClass', 'displayName']
    params_opt = []

    def __init__(self, name):
        self.name = name
        self.ntobj = namedtuple('NtOpj', ' '.join(self.params_req + ['optional']))

    def get_nt(self, node):
        """Query Reactome database for all edit dates."""
        k2v = {p:node[p] for p in self.params_req}
        k2v['optional'] = {o:node[o] for o in self.params_opt if o in node}
        return self.ntobj(**k2v)

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
