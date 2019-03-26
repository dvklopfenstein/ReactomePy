"""Reactome Polymer Neo4j Node.

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

  574,228 PhysicalEntity  1677 Polymer      1   1677  0.0006 definition
  574,228 PhysicalEntity  1677 Polymer      9   1677  0.0054 maxUnitCount
  574,228 PhysicalEntity  1677 Polymer     65   1677  0.0388 minUnitCount
  574,228 PhysicalEntity  1677 Polymer   1661   1677  0.9905 speciesName
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class Polymer(PhysicalEntity):
    """Params seen on all Polymers."""

    # pe params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_opt = PhysicalEntity.params_opt + \
        ('speciesName', 'minUnitCount', 'maxUnitCount', 'definition')

    relationships = {
        **PhysicalEntity.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference']),
            'species': frozenset(['Species']),
            'inferredTo': frozenset(['Polymer']),
            # 'repeatedUnit': frozenset(['PhysicalEntity']),
            'repeatedUnit': frozenset([
                'CandidateSet', 'DefinedSet',
                'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
                'Complex', 'Polymer', 'SimpleEntity']),
            'goCellularComponent': frozenset(['GO_CellularComponent', 'Compartment']),
        }
    }

    def __init__(self):
        super(Polymer, self).__init__('Polymer')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
