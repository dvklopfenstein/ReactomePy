"""Reactome Species Neo4j Node.

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

from reactomeneo4j.code.neo4j.taxon import Taxon


# pylint: disable=too-few-public-methods
class Species(Taxon):
    """Species."""

    # req: dbId schemaClass displayName 
    # opt: taxId name
    params_opt = Taxon.params_opt + ['abbreviation']

    def __init__(self):
        super(Species, self).__init__('Species')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
