"""Reactome GOTerm Neo4j Node.

    - GO_Term (dcnt=4)
  > -- GO_CellularComponent (dcnt=1)
  > --- Compartment (dcnt=0)
  > -- GO_BiologicalProcess (dcnt=0)
  > -- GO_MolecularFunction (dcnt=0)

    5,532 GO_Term  2038 GO_MolecularFunction  1232   2038  0.6045 ecNumber
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.go_cellularcomponent import GOCellularComponent


# pylint: disable=too-few-public-methods
class Compartment(GOCellularComponent):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | accession databaseName definition name url

    relationships = {
        **GOCellularComponent.relationships,
        **{
            'hasPart': frozenset(['GO_CellularComponent']),
        }
    }

    def __init__(self):
        super(Compartment, self).__init__('Compartment')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
