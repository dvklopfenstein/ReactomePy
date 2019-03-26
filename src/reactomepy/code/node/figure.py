"""Reactome Figure Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- Figure (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Figure(DatabaseObject):
    """Figure."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ('url',)
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    def __init__(self):
        super(Figure, self).__init__('Figure')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
