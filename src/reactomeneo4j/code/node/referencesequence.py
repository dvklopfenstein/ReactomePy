"""Lists parameters seen on all ReferenceSequence.

Hier: ReferenceEntity:ReferenceSequence:...

  - ReferenceEntity (dcnt=8)
  -- ReferenceSequence (dcnt=4)
> --- ReferenceGeneProduct (dcnt=1)
> ---- ReferenceIsoform (dcnt=0)
> --- ReferenceDNASequence (dcnt=0)
> --- ReferenceRNASequence (dcnt=0)
> -- ReferenceGroup (dcnt=0)
> -- ReferenceMolecule (dcnt=0)
> -- ReferenceTherapeutic (dcnt=0)

1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13174 155709  0.0846 chain
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13174 155709  0.0846 checksum
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13293 155709  0.0854 comment
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13174 155709  0.0846 isSequenceChanged
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13474 155709  0.0865 keyword
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct   134749 155709  0.8654 otherIdentifier
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    18872 155709  0.1212 secondaryIdentifier
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13380 155709  0.0859 sequenceLength

1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 chain
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 checksum
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 comment
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 isSequenceChanged
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 keyword
1,031,812 ReferenceEntity    1593 ReferenceIsoform          305   1593  0.1915 otherIdentifier
1,031,812 ReferenceEntity    1593 ReferenceIsoform         1466   1593  0.9203 secondaryIdentifier
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 sequenceLength
1,031,812 ReferenceEntity    1593 ReferenceIsoform         1593   1593  1.0000 variantIdentifier

1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 comment
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 keyword
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 otherIdentifier
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        3 733929  0.0000 sequenceLength

"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.neo4j.referenceentity import ReferenceEntity

# pylint: disable=too-few-public-methods
class ReferenceSequence(ReferenceEntity):
    """Lists parameters seen on all ReferenceSequence."""

    params_opt = ReferenceEntity.params_opt + ['description', 'name', 'geneName']

    relationships = {
        **ReferenceEntity.relationships, 
        **{
            'referenceGene': set(['ReferenceDNASequence']),
        }
    }

    def __init__(self, name):
        super(ReferenceSequence, self).__init__(name)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
