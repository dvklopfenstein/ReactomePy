"""Given a schemaClass string, return the associated class instance."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4jnt.instanceedit import Neo4jInstanceEdit


def get_schemaclass(schemaclass):
    """Given a schemaClass string, return the associated class instance."""
    if schemaclass == 'InstanceEdit':
        return Neo4jInstanceEdit()
    assert False, 'UNRECOGNIZED schemaClass({S})'.format(S=schemaclass)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
