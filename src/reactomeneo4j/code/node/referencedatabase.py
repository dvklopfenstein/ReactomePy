"""Lists parameters seen on all ReferenceEntity.

  - DatabaseObject (dcnt=80)
> -- ReferenceDatabase (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.code.node.databaseobject import DatabaseObject

# pylint: disable=too-few-public-methods
class ReferenceDatabase(DatabaseObject):
    """Lists parameters seen on all ReferenceEntity."""

    # req: dbId displayName schemaClass
    params_req = DatabaseObject.params_req + ['accessUrl', 'name', 'url']
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    def __init__(self, dbid=None):
        super(ReferenceDatabase, self).__init__('ReferenceDatabase', dbid)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
