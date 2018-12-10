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

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class GOTerm(DatabaseObject):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + [
        'accession', 'databaseName', 'definition', 'name', 'url']

    relationships = {
        'referenceDatabase': set(['ReferenceDatabase']),
        'hasPart': set(['GO_Term']),
        'componentOf': set(['GO_Term']),
        'instanceOf': set(['GO_Term']),
        'regulate': set(['GO_Term']),
        'negativelyRegulate': set(['GO_Term']),
        'positivelyRegulate': set(['GO_Term']),
    }

    def __init__(self, name):
        super(GOTerm, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
