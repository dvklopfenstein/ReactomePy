"""Manage data in schemaClass, LiteratureReference."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# pylint: disable=too-few-public-methods
class LiteratureReference(object):
    """Manage data in schemaClass, LiteratureReference."""

    def __init__(self, node):
        assert node['schemaClass'] == 'LiteratureReference'
        assert node['displayName'] == node['title']
        # pylint: disable=bad-whitespace
        self.volume  = node['volume']           # 207
        self.journal = node['journal']          # Immunol Rev
        self.pages   = node['pages']            # 166-83
        self.year    = node['year']             # 2005
        self.db_id   = node['dbId']             # 1500889
        self.pmid    = node['pubMedIdentifier'] # 16181335
        self.title   = node['title']            # Cross-presentation: ...

    def __str__(self):
        return "{PMID:9} {YEAR} {TITLE}".format(
            PMID=self.pmid, YEAR=self.year, TITLE=self.title)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
