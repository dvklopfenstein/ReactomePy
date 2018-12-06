"""Lists parameters seen on all DatabaseObjects."""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple


# pylint: disable=too-few-public-methods
class Neo4jDatabaseObject():
    """Lists parameters seen on all DatabaseObjects."""

    params_req = ['dbId', 'schemaClass', 'displayName']


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
