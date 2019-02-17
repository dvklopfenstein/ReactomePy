"""Read IDs and associations from files."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os


def read_ids(file_txt):
    """Read study or population IDs. Return set of IDs."""
    ids = set()
    if not os.path.exists(file_txt):
        return ids
    with open(file_txt) as ifstrm:
        for line in ifstrm:
            print(line)
        print('  {N:5,} IDs READ: {FILE}'.format(N=len(ids), FILE=file_txt))
    return ids

def read_associations(file_txt):
    """Read associations. Return a dict."""
    id2items = {}
    if not os.path.exists(file_txt):
        return id2items
    with open(file_txt) as ifstrm:
        for line in ifstrm:
            print(line)
    return id2items


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
