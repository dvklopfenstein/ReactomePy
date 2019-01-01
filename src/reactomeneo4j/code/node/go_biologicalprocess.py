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

from reactomeneo4j.code.node.go_term import GOTerm


# pylint: disable=too-few-public-methods
class GOBiologicalProcess(GOTerm):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | accession databaseName definition name url

    relationships = {
        **GOTerm.relationships,
        **{
            'hasPart': frozenset(['GO_BiologicalProcess', 'GO_MolecularFunction']),
            'componentOf': frozenset(['GO_BiologicalProcess']),
            'instanceOf': frozenset(['GO_BiologicalProcess']),
            'regulate': frozenset(['GO_MolecularFunction', 'GO_BiologicalProcess']),
            'negativelyRegulate': frozenset(['GO_MolecularFunction', 'GO_BiologicalProcess']),
            'positivelyRegulate': frozenset(['GO_MolecularFunction', 'GO_BiologicalProcess']),
        }
    }

    def __init__(self):
        super(GOBiologicalProcess, self).__init__('GO_BiologicalProcess')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
