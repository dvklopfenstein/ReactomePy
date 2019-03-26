"""Reactome ProteinDrug Neo4j Node.

    - PhysicalEntity (dcnt=13)
    -- Drug (dcnt=3)
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
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.drug import Drug


# pylint: disable=too-few-public-methods
class ProteinDrug(Drug):
    """ProteinDrug."""

    # params: dbId schemaClass displayName | stId stIdVersion oldStId isInDisease name
    # params: oldStId
    params_opt = Drug.params_opt + ('definition',)
    prtfmt = Drug.prtfmt + '{div}{definition}'
    optstr_dflt = {'div':'', 'definition':''}

    # relationships = {
    #     **Drug.relationships,
    #     **{
    #         'literatureReference': frozenset(['LiteratureReference']),
    #         'referenceEntity': frozenset(['ReferenceMolecule']),
    #     }
    # }

    def __init__(self):
        super(ProteinDrug, self).__init__('ProteinDrug')

    def get_optstr(self, optional_dct):
        """Given optional dictionary, return printable strings."""
        k2v = dict(self.optstr_dflt)
        # pylint: disable=no-member
        if not self.optstr_dflt.keys().isdisjoint(optional_dct):
            k2v['div'] = ' |'
        if 'definition' in optional_dct:
            k2v['definition'] = ' {DEFN}'.format(DEFN=optional_dct['definition'])
        return k2v


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
