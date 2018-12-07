"""Given a schemaClass string, return the associated class instance."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.instanceedit import InstanceEdit


def get_schemaclass(schemaclass):
    """Given a schemaClass string, return the associated class instance."""
    if schemaclass == 'InstanceEdit':
        return InstanceEdit()
    assert False, 'UNRECOGNIZED schemaClass({S})'.format(S=schemaclass)
    return None


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
