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
class GOMolecularFunction(GOTerm):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | accession databaseName definition name url
    params_opt = GOTerm.params_opt + ('ecNumber',)

    relationships = {
        **GOTerm.relationships,
        **{
            'hasPart': frozenset(['GO_MolecularFunction']),
            'componentOf': frozenset(['GO_BiologicalProcess']),
            'instanceOf': frozenset(['GO_MolecularFunction']),
            # Removed in v69:
            ##   'regulate': frozenset(['GO_MolecularFunction']),
            ##   'negativelyRegulate': frozenset(['GO_MolecularFunction']),
            ##   'positivelyRegulate': frozenset(['GO_MolecularFunction']),
        }
    }

    def __init__(self):
        super(GOMolecularFunction, self).__init__('GO_MolecularFunction')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
