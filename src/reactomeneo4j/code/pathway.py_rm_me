"""Manage data in schemaClass, Pathway."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from datetime import date

# pylint: disable=too-few-public-methods,too-many-instance-attributes
class Pathway(object):
    """Manage data in schemaClass, Pathway."""

    def __init__(self, node):
        _st_id = node['stId']
        _st_id_len = len(_st_id)
        assert node['schemaClass'] == 'Pathway'
        assert _st_id == node['stIdVersion'][:_st_id_len]
        # pylint: disable=bad-whitespace
        self.species_name = node['speciesName']  # Homo sapiens
        self.in_disease   = node['isInDisease']  # False
        _dt = node['releaseDate']
        self.release_date = date(int(_dt[:4]), int(_dt[5:7]), int(_dt[8:])) # 2011-09-20
        self.display_name = node['displayName']  # Antigen processing-Cross presentation
        self.st_id_ver    = node['stIdVersion'][_st_id_len:]  # R-HSA-1236975.1
        self.name         = node['name']         # ['Antigen processing-Cross presentation']
        self.st_id        = _st_id               # R-HSA-1236975
        self.has_diagram  = node['hasDiagram']   # False
        self.is_inferred  = node['isInferred']   # False

    def __str__(self):
        return "PW {ID:9} {DATE} {NAME}".format(
            ID=self.st_id, DATE=self.release_date, NAME=self.display_name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
