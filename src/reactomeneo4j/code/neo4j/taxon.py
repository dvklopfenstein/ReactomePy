"""Reactome Taxon Neo4j Node.

> - Taxon (dcnt=1)
> -- Species (dcnt=0)

      396 Taxon   315 Taxon    315 315  1.0000 name
      396 Taxon   315 Taxon    314 315  0.9968 taxId

      396 Taxon    81 Species   81  81  1.0000 abbreviation
      396 Taxon    81 Species   81  81  1.0000 name
      396 Taxon    81 Species   81  81  1.0000 taxId
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Taxon(DatabaseObject):
    """Params seen on all Taxon."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_opt = DatabaseObject.params_opt + ['taxId', 'name']

    relationships = {
        'crossReference' : set(['Taxon']),
        'superTaxon'     : set(['Taxon']),
    }

    def __init__(self, name="Taxon"):
        super(Taxon, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
