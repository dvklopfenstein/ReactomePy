"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


def get_version(gdbdr):
    """Get Reactome version."""
    version = None
    query = 'MATCH (v:DBInfo) RETURN v'
    with gdbdr.session() as session:
        for rec in session.run(query).records():
            dbinfo = rec['v']
            assert dbinfo.get('name') == 'reactome'
            version = dbinfo.get('version')
    assert version is not None
    return version


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
