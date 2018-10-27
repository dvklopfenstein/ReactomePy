"""Node functions."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class Record(object):
    """Node functions."""

    def __init__(self, record):
        self.record = record

    def prt_traverse(self, keys_prt, sortby=None, prt=sys.stdout):
        """Traverse and print items."""
        for idx, item in enumerate(self.get_traverse_items(sortby)):
            prt.write('TRAVERSE[{I:2}]: '.format(I=idx))
            for key in keys_prt:
                prt.write('{KEY} {VAL}'.format(KEY=key, VAL=item[key]))
            prt.write('\n')

    def get_traverse_items(self, sortby):
        """Get items in traverse(). Sort if requested by user."""
        if sortby is None:
            return self.node.traverse()
        return sorted(self.node.traverse(), key=sortby)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
