"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"


def get_dbids(gdbdr, nodestr='Complex{stId:"R-HSA-167199"}'):
    """Get DatabaseObject dbId, which is present on all Nodes."""
    dbids = set()
    query = 'MATCH (n:NODESTR) RETURN n'.format(NODESTR=nodestr)
    with gdbdr.session() as session:
        for rec in session.run(query).records():
            dbids.add(rec['n']['dbId'])
    return dbids

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
