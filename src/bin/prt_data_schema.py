#!/usr/bin/env python
"""Print Reactome Graph Database data schema hierarchy."""
# https://reactome.org/content/schema/DatabaseObject

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.schema.hier import DataSchemaHier


def main():
    """Print Reactome data schema."""
    fout_txt = 'log/reactome_data_schema.txt'
    obj = DataSchemaHier()
    with open(fout_txt, 'w') as prt:
        obj.prt_data_schema_all(prt)
        print('  WROTE: {TXT}'.format(TXT=fout_txt))


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
