"""Reactome Summation Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- Summation (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Summation(DatabaseObject):
    """Summation."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ('text',)
    prtfmt = '{schemaClass}: {text}'
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    relationships = {
        'literatureReference': frozenset(['LiteratureReference', 'Book', 'URL']),
    }

    def __init__(self):
        super(Summation, self).__init__('Summation')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
