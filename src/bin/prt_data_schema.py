#!/usr/bin/env python
"""Print Reactome Graph Database data schema hierarchy."""
# https://reactome.org/content/schema/DatabaseObject

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomeneo4j.code.schema.hier import DataSchemaHier


def main():
    """Print Reactome data schema."""
    prt = sys.stdout
    obj = DataSchemaHier()
    obj.prt_data_schema('DatabaseObject', prt, max_indent=2)
    print(sorted([o.item_id for o in obj.name2obj.values() if o.dcnt==1], key=obj.sortby))

if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
