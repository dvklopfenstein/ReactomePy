"""Lists parameters seen on all ReferenceDNASequence.

  Hier: ReferenceEntity:ReferenceSequence:ReferenceDNASequence

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)

1,031,812 ReferenceEntity  733929 ReferenceDNASequence   733929 733929  1.0000 dbId
1,031,812 ReferenceEntity  733929 ReferenceDNASequence   733929 733929  1.0000 schemaClass
1,031,812 ReferenceEntity  733929 ReferenceDNASequence   733929 733929  1.0000 displayName

1,031,812 ReferenceEntity  733929 ReferenceDNASequence   733929 733929  1.0000 databaseName
1,031,812 ReferenceEntity  733929 ReferenceDNASequence   733929 733929  1.0000 identifier
1,031,812 ReferenceEntity  733929 ReferenceDNASequence   733929 733929  1.0000 url

1,031,812 ReferenceEntity  733929 ReferenceDNASequence    11356 733929  0.0155 name
1,031,812 ReferenceEntity  733929 ReferenceDNASequence   147076 733929  0.2004 geneName
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 comment
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 keyword
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 otherIdentifier
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        3 733929  0.0000 sequenceLength
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.referencesequence import ReferenceSequence

# pylint: disable=too-few-public-methods
class ReferenceDNASequence(ReferenceSequence):
    """Lists parameters seen on all ReferenceDNASequence."""

    # req: dbId schemaClass displayName | databaseName identifier url
    # opt: geneName otherIdentifier description name comment sequenceLength keyword

    def __init__(self):
        super(ReferenceDNASequence, self).__init__('ReferenceDNASequence')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
