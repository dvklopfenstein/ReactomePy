"""Reactome ExternalOntology Neo4j Node.

  - GO_Term (dcnt=4)
> -- GO_CellularComponent (dcnt=1)
> --- Compartment (dcnt=0)
> -- GO_BiologicalProcess (dcnt=0)
> -- GO_MolecularFunction (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class ExternalOntology(DatabaseObject):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ['databaseName', 'identifier', 'name', 'url']
    params_opt = DatabaseObject.params_opt + ['definition', 'synonym']
    fmtpat = '{schemaClass}: {displayName}'

    relationships = {
        'referenceDatabase': set(['ReferenceDatabase']),
    }

    def __init__(self, name):
        super(ExternalOntology, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
