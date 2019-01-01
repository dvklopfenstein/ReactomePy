"""Reactome Complex Neo4j Node.
   Defn Complex: A complex of two of more PhysicalEntities

   Hier: PhysicalEntity:Complex

    - PhysicalEntity (dcnt=13)
    -- EntitySet (dcnt=3)
  > --- CandidateSet (dcnt=0)
  > --- DefinedSet (dcnt=0)
  > --- OpenSet (dcnt=0)
    -- Drug (dcnt=2)
  > --- ChemicalDrug (dcnt=0)
  > --- ProteinDrug (dcnt=0)
  > -- GenomeEncodedEntity (dcnt=1)
  > --- EntityWithAccessionedSequence (dcnt=0)
  > -- Complex (dcnt=0)
  > -- OtherEntity (dcnt=0)
  > -- Polymer (dcnt=0)
  > -- SimpleEntity (dcnt=0)

  574,228 PhysicalEntity  103000 Complex      9654 103000  0.0937 isChimeric
  574,228 PhysicalEntity  103000 Complex    102974 103000  0.9997 speciesName
  574,228 PhysicalEntity  103000 Complex         7 103000  0.0001 systematicName
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.physicalentity import PhysicalEntity


# pylint: disable=too-few-public-methods
class Complex(PhysicalEntity):
    """Reactome Complex Neo4j Node."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    params_opt = PhysicalEntity.params_opt + ('speciesName', 'isChimeric', 'systematicName')

    relationships = {
        **PhysicalEntity.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference', 'Book']),
            'figure': frozenset(['Figure']),
            'species': frozenset(['Species']),
            'relatedSpecies': frozenset(['Species']),
            'inferredTo': frozenset(['Complex']),
            'hasComponent': frozenset([
                'CandidateSet', 'DefinedSet', 'OpenSet',
                'ChemicalDrug',
                'GenomeEncodedEntity', 'EntityWithAccessionedSequence',
                'Complex', 'OtherEntity', 'Polymer', 'SimpleEntity']),
            'entityOnOtherCell': frozenset([
                'DefinedSet', 'OpenSet',
                'EntityWithAccessionedSequence',
                'Complex', 'OtherEntity', 'Polymer', 'SimpleEntity']),
            'includedLocation': frozenset(['Compartment']),
            'goCellularComponent': frozenset(['GO_CellularComponent', 'Compartment']),
        }
    }

    def __init__(self):
        super(Complex, self).__init__('Complex')

    def get_nt(self, node):
        """Given a Neo4j Node, return a namedtuple containing parameters."""
        return self.ntobj(**PhysicalEntity.get_dict(self, node))

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = PhysicalEntity.get_dict(self, node)
        _opt = k2v['optional']
        k2v['aart'] = k2v['aart'] + self._get_ischimeric(_opt)
        return k2v

    def _get_ischimeric(self, k2vopt):
        if 'isChimeric' not in k2vopt:
            return '.'
        return self.P2A['isChimeric'] if k2vopt['isChimeric'] else 'n'


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
