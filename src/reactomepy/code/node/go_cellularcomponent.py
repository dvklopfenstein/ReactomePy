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

from reactomepy.code.node.go_term import GOTerm


# pylint: disable=too-few-public-methods
class GOCellularComponent(GOTerm):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | accession databaseName definition name url

    relationships = {
        **GOTerm.relationships,
        **{
            'hasPart': frozenset(['Compartment', 'GO_CellularComponent']),
            'componentOf': frozenset(['Compartment', 'GO_CellularComponent']),
            'instanceOf': frozenset(['Compartment', 'GO_CellularComponent']),
            'surroundedBy': frozenset(['Compartment', 'GO_CellularComponent']),
        }
    }

    def __init__(self, name='GO_CellularComponent'):
        super(GOCellularComponent, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
