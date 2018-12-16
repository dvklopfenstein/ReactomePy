"""Reactome Summation Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- Summation (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Summation(DatabaseObject):
    """Summation."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ['text']
    fmtpat = '{schemaClass}: {text}'

    relationships = {
        'literatureReference': set(['Publication']),
    }

    def __init__(self):
        super(Summation, self).__init__('Summation')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
