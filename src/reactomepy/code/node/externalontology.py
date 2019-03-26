"""Reactome ExternalOntology Neo4j Node.

  - GO_Term (dcnt=4)
> -- GO_CellularComponent (dcnt=1)
> --- Compartment (dcnt=0)
> -- GO_BiologicalProcess (dcnt=0)
> -- GO_MolecularFunction (dcnt=0)
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class ExternalOntology(DatabaseObject):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ('databaseName', 'identifier', 'name', 'url')
    params_opt = DatabaseObject.params_opt + ('definition', 'synonym')
    prtfmt = '{schemaClass}: {displayName}'
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')
    optstr_dflt = {'div':'', 'formula':'', 'trivial':''}

    relationships = {
        'referenceDatabase': frozenset(['ReferenceDatabase']),
    }

    def __init__(self, name):
        # pylint: disable=useless-super-delegation
        super(ExternalOntology, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
