"""Reactome PhysicalEntity Neo4j Node.

    - PhysicalEntity(dcnt=13)
    -- EntitySet(dcnt=3)
  > --- CandidateSet(dcnt=0)
  > --- DefinedSet(dcnt=0)
    -- Drug(dcnt=2)
  > --- ChemicalDrug(dcnt=0)
  > --- ProteinDrug(dcnt=0)
  > -- GenomeEncodedEntity(dcnt=1)
  > --- EntityWithAccessionedSequence(dcnt=0)
  > -- Complex(dcnt=0)
  > -- OtherEntity(dcnt=0)
  > -- Polymer(dcnt=0)
  > -- SimpleEntity(dcnt=0)

  574,228 PhysicalEntity    311 OtherEntity     6  311 0.0193 definition
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class OtherEntity(PhysicalEntity):
    """Params seen on all Physical Entities."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_opt = PhysicalEntity.params_opt + ('definition',)

    relationships = {
        **PhysicalEntity.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference']),
        }
    }

    def __init__(self):
        super(OtherEntity, self).__init__('OtherEntity')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
