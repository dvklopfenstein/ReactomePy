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

from reactomeneo4j.code.node.go_cellularcomponent import GO_CellularComponent


# pylint: disable=too-few-public-methods
class Compartment(GO_CellularComponent):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | accession databaseName definition name url

    relationships = {
        **GO_CellularComponent.relationships,
        **{
            'hasPart': set(['GO_CellularComponent']),
        }
    }

    def __init__(self):
        super(Compartment, self).__init__('Compartment')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
