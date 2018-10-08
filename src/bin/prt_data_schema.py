#!/usr/bin/env python
"""Print Reactome Graph Database data schema hierarchy."""
# https://reactome.org/content/schema/DatabaseObject

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.schema.hier import DataSchemaHier


if __name__ == '__main__':
    DataSchemaHier().prt_data_schema()


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
