"""Reactome InstanceEdit Neo4j Node.

  - DatabaseObject(dcnt=80)
> -- InstanceEdit(dcnt=0)

   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 dbId
   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 displayName
   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 schemaClass
   88,579 InstanceEdit  88579 InstanceEdit  88579  88579  1.0000 dateTime
   88,579 InstanceEdit  88579 InstanceEdit    348  88579  0.0039 note
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
import datetime


# pylint: disable=too-few-public-methods
class Neo4jInstanceEdit():
    """Report the dates that a pathway was edited."""

    nted = namedtuple('NtEd', 'dbId displayName schemaClass dateTime optional')
    timefmt = '%Y-%m-%d %H:%M:%S'

    def get_nt(self, node):
        """Query Reactome database for all edit dates."""
        date = datetime.datetime.strptime(node['dateTime'].split('.')[0], self.timefmt)
        return self.nted(
            dbId=node['dbId'],
            displayName=node['displayName'],
            schemaClass=node['schemaClass'],
            dateTime=date,
            optional=self._get_pwy_optional(node))

    @staticmethod
    def _get_pwy_optional(node):
        """Get optional data members."""
        ret = {}
        if 'note' in node:
            ret['note'] = node['note']
        return ret


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
