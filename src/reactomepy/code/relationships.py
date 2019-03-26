"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import sys
# import timeit
# import collections as cx
# from reactomepy.code.neo4jnodebasic import Neo4jNodeBasic
# from reactomepy.code.utils import get_hms
# from reactomepy.code.query.relationship_agg import RelationshipCollapse
# from reactomepy.code.node.schemaclass_factory import SCHEMACLASS2CONSTRUCTOR
# from reactomepy.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class Relationships():
    """Create, collect, and report a Node hierarchy."""

    pathway_hier = {
        'hasEncapsulatedEvent',
        'hasEvent',
        'normalPathway',
        'precedingEvent',
    }

    physicalentity_hier = {
        'hasCandidate',
        'repeatedUnit',
        'hasComponent',
        'hasMember',
        'entityOnOtherCell',
    }

    other = {
        'hasModifiedResidue',
        'hasPart',
        'compartment',
        'componentOf',
        'crossReference',
        'disease',
        'entityOnOtherCell',
        'equivalentTo',
        'figure',
        'goCellularComponent',
        'includedLocation',
        'instanceOf',
        'isoformParent',
        'modification',
        'psiMod',
        'repeatedUnit',
        'publisher',
        'literatureReference',
        'superTaxon',
        'species',
        'referenceDatabase',
        'referenceEntity',
        'referenceGene',
        'referenceSequence',
        'referenceTherapeutic',
        'referenceTranscript',
        'relatedSpecies',
        'secondReferenceSequence',
        'summation',
    }



# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
