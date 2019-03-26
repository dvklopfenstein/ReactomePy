"""Reactome PhysicalEntity Neo4j Node.

  - DatabaseObject (dcnt=80)
> -- Affiliation (dcnt=0)

      266 Affiliation  266 Affiliation   206 266  0.7744 address
      266 Affiliation  266 Affiliation   266 266  1.0000 name
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Affiliation(DatabaseObject):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName
    params_opt = ('name', 'address')

    def __init__(self):
        super(Affiliation, self).__init__('Affiliation')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
