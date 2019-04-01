#!/usr/bin/env python
"""Test the Pathway Analysis Service: Get Reactome database name and version."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


from reactomepy.code.rest.service_content import ContentService


def test_analysis_database():
    """Test the Pathway Analysis Service: Get Reactome database name and version."""
    obj = ContentService()
    ver = obj.get_version()
    assert isinstance(ver, int), 'VERSION({V}) IS NOT AN INT'.format(V=ver)
    name = obj.get_databasename()
    assert name == 'reactome', 'DATABASE NAME({N}) IS NOT reactome'.format(N=name)
    print('{NAME} version {VER}'.format(NAME=name, VER=ver))


if __name__ == '__main__':
    test_analysis_database()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
