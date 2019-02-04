#!/usr/bin/env python
"""Does this repo have the current version of the Reactome Knowledgebase?

Usage: compare_reactome_version.py <neo4j_password> [options]

Options:
  -h --help  Show usage
  -u --neo4j_username=USER  Neo4j Reactome username [default: neo4j]
  --url=URL                 Neo4j Reactome local url [default: bolt://localhost:7687]
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.rest.service_content import ContentService
from reactomeneo4j.code.utils import get_gdbdr
from reactomeneo4j.code.query.functions import get_version
from reactomeneo4j.data.reactome_version import VERSION


def main():
    """Does this repo have the current version of the Reactome Knowledgebase?"""
    # Reactome version from Content Service
    obj = ContentService()
    ver_curr = obj.get_version()
    # Reactome version from locally loaded Reactome DAG
    ver_local = get_version(get_gdbdr(__doc__))
    print('\n  Current Reactome Knowledgebase Version:')
    print('    {VER:3} <- Latest version from Content Service'.format(VER=ver_curr))
    print('    {VER:3} <- version from locally loaded DAG'.format(VER=ver_local))
    print('    {VER:3} <- Version in this repo\n\n'.format(VER=VERSION))
    assert ver_local == ver_curr, 'VERSION FROM CONTENT SERVICE != LOCAL DAG'
    assert VERSION == ver_curr, 'PLEASE DOWNLOAD THE MOST RECENT REACTOME KNOWLEDGEBASE'
    assert obj.get_databasename() == 'reactome', 'UNEXPECTED DATABASE NAME'
    assert isinstance(ver_curr, int), 'BAD VERSION VALUE'


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
