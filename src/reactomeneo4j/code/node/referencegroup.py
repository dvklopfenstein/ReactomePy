"""Lists parameters seen on all ReferenceGroup.

Hier: ReferenceEntity:ReferenceGroup

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)

1,031,812 ReferenceEntity      99 ReferenceGroup              1     99  0.0101 formula
1,031,812 ReferenceEntity      99 ReferenceGroup             99     99  1.0000 name

1,031,812 ReferenceEntity    1978 ReferenceMolecule        1835   1978  0.9277 formula
1,031,812 ReferenceEntity    1978 ReferenceMolecule          30   1978  0.0152 geneName
1,031,812 ReferenceEntity    1978 ReferenceMolecule        1978   1978  1.0000 name
1,031,812 ReferenceEntity    1978 ReferenceMolecule           1   1978  0.0005 otherIdentifier
1,031,812 ReferenceEntity    1978 ReferenceMolecule          30   1978  0.0152 secondaryIdentifier
1,031,812 ReferenceEntity    1978 ReferenceMolecule        1948   1978  0.9848 trivial

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
class ReferenceGroup(ReferenceEntity):
    """Lists parameters seen on all ReferenceGroup."""

    params_opt = ReferenceEntity.params_opt + ['name', 'formula']

    def __init__(self):
        super(ReferenceGroup, self).__init__('ReferenceGroup')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
