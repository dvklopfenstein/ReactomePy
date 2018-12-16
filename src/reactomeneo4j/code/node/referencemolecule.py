"""Lists parameters seen on all ReferenceMolecule..

Hier: ReferenceEntity:ReferenceMolecule

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)

1,031,812 ReferenceEntity     139 ReferenceTherapeutic        1    139  0.0072 abbreviation
1,031,812 ReferenceEntity     139 ReferenceTherapeutic       84    139  0.6043 approvalSource
1,031,812 ReferenceEntity     139 ReferenceTherapeutic      139    139  1.0000 approved
1,031,812 ReferenceEntity     139 ReferenceTherapeutic      111    139  0.7986 inn
1,031,812 ReferenceEntity     139 ReferenceTherapeutic      139    139  1.0000 name
1,031,812 ReferenceEntity     139 ReferenceTherapeutic      131    139  0.9424 type
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.referenceentity import ReferenceEntity

# pylint: disable=too-few-public-methods
class ReferenceMolecule(ReferenceEntity):
    """Lists parameters seen on all ReferenceMolecule."""

    params_opt = ReferenceEntity.params_opt + [
        'secondaryIdentifier', 'otherIdentifier', 'name', 'formula', 'trivial', 'geneName']

    def __init__(self):
        super(ReferenceMolecule, self).__init__('ReferenceMolecule')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
