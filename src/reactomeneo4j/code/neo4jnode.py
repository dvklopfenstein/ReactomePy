"""Holds information for one data schema item."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
from reactomeneo4j.code.neo4j.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Neo4jNode():
    """Holds data extracted from Neo4j."""

    def __init__(self, neo4jnode, prtfmt=None):
        _sch = neo4jnode['schemaClass']
        assert _sch in SCHEMACLASS2CONSTRUCTOR, '**FATAL: BAD schemaClass({S})'.format(S=_sch)
        self.objsch = SCHEMACLASS2CONSTRUCTOR[_sch]
        self.ntp = self.objsch.get_nt(neo4jnode)
        self.fmtpat = self.objsch.fmtpat if prtfmt is None else prtfmt

    def __str__(self):
        return self.fmtpat.format(**self.ntp._asdict())


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
