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
class GO_MolecularFunction(GOTerm):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | accession databaseName definition name url
    params_opt = GOTerm.params_opt + ['ecNumber']

    relationships = {
        **GOTerm.relationships,
        **{
            'hasPart': set(['GO_MolecularFunction']),
            'componentOf': set(['GO_BiologicalProcess']),
            'instanceOf': set(['GO_MolecularFunction']),
            'regulate': set(['GO_MolecularFunction']),
            'negativelyRegulate': set(['GO_MolecularFunction']),
            'positivelyRegulate': set(['GO_MolecularFunction']),
        }
    }

    def __init__(self):
        super(GO_MolecularFunction, self).__init__('GO_MolecularFunction')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
