"""Reactome Figure Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- Figure (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Figure(DatabaseObject):
    """Figure."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ['url']
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    def __init__(self, dbid=None):
        super(Figure, self).__init__('Figure', dbid)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
