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

from reactomeneo4j.code.neo4j.go_term import GOTerm


# pylint: disable=too-few-public-methods
class GO_BiologicalProcess(GOTerm):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | accession databaseName definition name url

    relationships = {
        **GOTerm.relationships,
        **{
            'regulate': set(['GO_MolecularFunction', 'GO_BiologicalProcess']),
            'negativelyRegulate': set(['GO_MolecularFunction', 'GO_BiologicalProcess']),
            'positivelyRegulate': set(['GO_MolecularFunction', 'GO_BiologicalProcess']),
        }
    }

    def __init__(self):
        super(GO_BiologicalProcess, self).__init__('GO_BiologicalProcess')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
