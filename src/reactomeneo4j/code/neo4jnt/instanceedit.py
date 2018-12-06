"""Reactome InstanceEdit Neo4j Node.

  - DatabaseObject(dcnt=80)
> -- InstanceEdit(dcnt=0)

   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 dbId
   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 schemaClass
   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 displayName
   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 dateTime
   88,579 InstanceEdit  88579 InstanceEdit    348  88579  0.0039 note
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
import datetime
from reactomeneo4j.code.neo4jnt.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class InstanceEdit(DatabaseObject):
    """Report the dates that a pathway was edited."""

    params_req = ['dateTime']
    params_opt = ['note']
    timefmt = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        super(InstanceEdit, self).__init__()
        self.nted = namedtuple('NtEd', ' '.join(self.get_fields_namedtuple()))

    def get_nt(self, node):
        """Query Reactome database for all edit dates."""
        date = datetime.datetime.strptime(node['dateTime'].split('.')[0], self.timefmt)
        return self.nted(
            dbId=node['dbId'],
            displayName=node['displayName'],
            schemaClass=node['schemaClass'],
            dateTime=date,
            optional=self._get_pwy_optional(node))

    def get_fields_namedtuple(self):
        """Get fields to store Reactome Neo4j Node properties in a namedtuple."""
        return self.get_params_required() + ['optional']

    def get_params_required(self):
        """Get parameters seen on all Reactome Neo4j Node instances."""
        return DatabaseObject.params_req + self.params_req

    def get_params_optional(self):
        """Get parameters seen on some, but not all Reactome Neo4j Node instances."""
        return self.params_opt

    @staticmethod
    def _get_pwy_optional(node):
        """Get optional data members."""
        ret = {}
        if 'note' in node:
            ret['note'] = node['note']
        return ret


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
