"""Reactome Person Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- Person (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Person(DatabaseObject):
    """Person."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ['surname', 'initial']
    params_opt = DatabaseObject.params_opt + ['firstname', 'orcidId', 'project']

    relationships = {
        'author'         : set(['Publication', 'InstanceEdit']),
        'crossReference' : set(['DatabaseIdentifier']),
        'affiliation'    : set(['Affiliation']),
    }

    def __init__(self):
        super(Person, self).__init__('Person')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
