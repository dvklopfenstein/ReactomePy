"""Reactome PhysicalEntity Neo4j Node.

    - PhysicalEntity (dcnt=13)
    -- EntitySet (dcnt=3)
  > --- CandidateSet (dcnt=0)
  > --- DefinedSet (dcnt=0)
    -- Drug (dcnt=2)
  > --- ChemicalDrug (dcnt=0)
  > --- ProteinDrug (dcnt=0)
  > -- GenomeEncodedEntity (dcnt=1)
  > --- EntityWithAccessionedSequence (dcnt=0)
  > -- Complex (dcnt=0)
  > -- OtherEntity (dcnt=0)
  > -- Polymer (dcnt=0)
  > -- SimpleEntity (dcnt=0)

  574,228 PhysicalEntity  87271 DefinedSet         74  87271  0.0008 isOrdered
  574,228 PhysicalEntity  87271 DefinedSet      86795  87271  0.9945 speciesName
  574,228 PhysicalEntity  87271 DefinedSet          9  87271  0.0001 systematicName

  574,228 PhysicalEntity   9003 CandidateSet        1   9003  0.0001 definition
  574,228 PhysicalEntity   9003 CandidateSet       33   9003  0.0037 isOrdered
  574,228 PhysicalEntity   9003 CandidateSet     8997   9003  0.9993 speciesName
  574,228 PhysicalEntity   9003 CandidateSet        5   9003  0.0006 systematicName
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class EntitySet(PhysicalEntity):
    """Params seen on all EntitySets."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    # params: oldStId
    params_opt = PhysicalEntity.params_opt + ('isOrdered', 'systematicName', 'speciesName')

    relationships = {
        **PhysicalEntity.relationships,
        **{
            'species': frozenset(['Species']),
            'relatedSpecies': frozenset(['Species']),
        }
    }

    def __init__(self, name='EntitySet'):
        super(EntitySet, self).__init__(name)

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = PhysicalEntity.get_dict(self, node)
        _opt = k2v['optional']
        k2v['aart'] = k2v['aart'] + self._get_isordered(_opt)
        return k2v

    def _get_isordered(self, k2vopt):
        if 'isOrdered' not in k2vopt:
            return '.'
        return self.P2A['isOrdered'] if k2vopt['isOrdered'] else 'n'

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
