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
from datetime import datetime
from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class InstanceEdit(DatabaseObject):
    """Report the dates that a pathway was edited."""

    # params: dbId schemaName displayName
    params_req = DatabaseObject.params_req + ('dateTime',)
    params_opt = DatabaseObject.params_opt + ('note',)
    timefmt = '%Y-%m-%d %H:%M:%S'
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')
    prtfmt = '{dbId:8} {schemaClass:32} {dateTime} {displayName}'

    relationships = {
        'created' : frozenset(['DatabaseObject']),
        'modified': frozenset(['DatabaseObject']),
        'authored': frozenset(['PhysicalEntity', 'Event']),
        'edited'  : frozenset(['PhysicalEntity', 'Event']),
        'reviewed': frozenset(['PhysicalEntity', 'Event']),
        'revised' : frozenset(['PhysicalEntity', 'Event']),


    }

    def __init__(self):
        super(InstanceEdit, self).__init__('InstanceEdit')

    def get_nt(self, node):
        """Query Reactome database for all edit dates."""
        k2v = DatabaseObject.get_dict(self, node)
        k2v['dateTime'] = datetime.strptime(k2v['dateTime'].split('.')[0], self.timefmt)
        return self.ntobj(**k2v)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
