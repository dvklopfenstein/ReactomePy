#!/usr/bin/env python
"""Retrieving the particpants of a Reaction."""
# https://reactome.org/dev/graph-database/extract-participating-molecules#retrieving-participants

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from neo4j import GraphDatabase

# pylint: disable=line-too-long
def main(password, prt=sys.stdout):
    """Retrieving the particpants of a Reaction."""

    # Reactions have inputs, outputs, catalysts and regulations, so to know
    # the participants of a reaction, all these slots have to be taken into account.
    # Please note that the physical entity acting as catalyst is
    # stored in the "physicalEntity" slot of the class "CatalystActivity"
    # and the one belonging to the regulation is stored in the "regulator"
    # slot of the "Regulation" class.
    #
    # First level paticipating molecules for reaction R-HSA-8863895
    qry = ('MATCH (r:ReactionLikeEvent{stId:"R-HSA-8863895"})'
           '-[:input|output|catalystActivity|regulatedBy|regulator|physicalEntity*]'
           '->(pe:PhysicalEntity)'
           'RETURN DISTINCT r.stId AS Reaction, pe.stId as Participant, pe.displayName AS DisplayName')

    data = _get_data(qry, password)
    _prt_data(data, prt)

def _prt_data(data, prt):
    """Print the Participating molecules for a pathway."""
    msg = '{N} participants in Reaction(R-HSA-8863895)'.format(N=len(data))
    prt.write("{MSG}\n\n".format(MSG=msg))
    prt.write('Reaction Participant DisplayName\n')
    prt.write('-------- ----------- -----------\n')
    for dct in sorted(data, key=lambda d: [d['Reaction'], d['Participant']]):
        prt.write('{Reaction:13} {Participant:13} {DisplayName}\n'.format(**dct))
    print(msg)

def _get_data(qry, password):
    """Get the Participating molecules for a pathway."""
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        return [rec.data() for rec in session.run(qry).records()]


if __name__ == '__main__':
    assert len(sys.argv) != 1, 'First arg must be your Neo4j database password'
    main(sys.argv[1])

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
