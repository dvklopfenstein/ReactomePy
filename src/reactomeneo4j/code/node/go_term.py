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

from collections import namedtuple
from reactomeneo4j.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class GOTerm(DatabaseObject):
    """Params seen on all Physical Entities."""

    sch2ns = {
        'GO_CellularComponent': 'CC',
        'Compartment': 'CC',
        'GO_BiologicalProcess': 'BP',
        'GO_MolecularFunction': 'MF'
    }

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + (
        'accession', 'databaseName', 'definition', 'name', 'url')

    prtfmt = '{NS} {databaseName}:{accession} {name} -> {definition}'

    relationships = {
        'referenceDatabase': set(['ReferenceDatabase']),
        #'hasPart': set(['GO_Term']),
        #'componentOf': set(['GO_Term']),
        #'instanceOf': set(['GO_Term']),
        #'regulate': set(['GO_Term']),
        #'negativelyRegulate': set(['GO_Term']),
        #'positivelyRegulate': set(['GO_Term']),
    }

    ntobj = namedtuple('NtOpj', ' '.join(params_req) + ' NS optional')

    def __init__(self, name):
        # pylint: disable=useless-super-delegation
        super(GOTerm, self).__init__(name)

    def get_dict(self, node):
        """Return a Python dict containing all Neo4j Node parameters."""
        k2v = DatabaseObject.get_dict(self, node)
        k2v['NS'] = self.sch2ns[k2v['schemaClass']]
        return k2v

    def get_nt(self, node):
        """Return a Python namedtuple containing all Neo4j Node parameters."""
        return self.ntobj(**self.get_dict(node))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
