#!/usr/bin/env python
"""Does this repo have the current version of the Reactome Knowledgebase?"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.rest.service_content import ContentService
from reactomeneo4j.data.reactome_version import VERSION


def main():
    """Does this repo have the current version of the Reactome Knowledgebase?"""
    obj = ContentService()
    ver_curr = obj.get_version()
    print('\n  Current Reactome Knowledgebase Version:')
    print('    {VER:3} <- Latest version'.format(VER=ver_curr))
    print('    {VER:3} <- Version in this repo\n\n'.format(VER=VERSION))
    assert VERSION == ver_curr, 'PLEASE DOWNLOAD THE MOST RECENT REACTOME KNOWLEDGEBASE'
    assert obj.get_databasename() == 'reactome', 'UNEXPECTED DATABASE NAME'
    assert isinstance(ver_curr, int), 'BAD VERSION VALUE'


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
