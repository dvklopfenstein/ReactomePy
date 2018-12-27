"""Lists parameters seen on all ReferenceEntity.

   Hier: ReferenceEntity

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
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13353 155709  0.0858 description
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    19144 155709  0.1229 geneName
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13174 155709  0.0846 isSequenceChanged
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13474 155709  0.0865 keyword
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13501 155709  0.0867 name
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct   134749 155709  0.8654 otherIdentifier
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    18872 155709  0.1212 secondaryIdentifier
1,031,812 ReferenceEntity  155709 ReferenceGeneProduct    13380 155709  0.0859 sequenceLength

1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 chain
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 checksum
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 comment
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 description
1,031,812 ReferenceEntity    1593 ReferenceIsoform         1549   1593  0.9724 geneName
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 isSequenceChanged
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 keyword
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 name
1,031,812 ReferenceEntity    1593 ReferenceIsoform          305   1593  0.1915 otherIdentifier
1,031,812 ReferenceEntity    1593 ReferenceIsoform         1466   1593  0.9203 secondaryIdentifier
1,031,812 ReferenceEntity    1593 ReferenceIsoform          315   1593  0.1977 sequenceLength
1,031,812 ReferenceEntity    1593 ReferenceIsoform         1593   1593  1.0000 variantIdentifier

1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 comment
1,031,812 ReferenceEntity  733929 ReferenceDNASequence   147076 733929  0.2004 geneName
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 keyword
1,031,812 ReferenceEntity  733929 ReferenceDNASequence    11356 733929  0.0155 name
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        1 733929  0.0000 otherIdentifier
1,031,812 ReferenceEntity  733929 ReferenceDNASequence        3 733929  0.0000 sequenceLength
1,031,812 ReferenceEntity  138365 ReferenceRNASequence        8 138365  0.0001 description
1,031,812 ReferenceEntity  138365 ReferenceRNASequence    37415 138365  0.2704 geneName
1,031,812 ReferenceEntity  138365 ReferenceRNASequence       99 138365  0.0007 name

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

from collections import namedtuple
from reactomeneo4j.code.node.databaseobject import DatabaseObject

# pylint: disable=too-few-public-methods
class ReferenceEntity(DatabaseObject):
    """Lists parameters seen on all ReferenceEntity."""

    # req: dbId schemaClass displayName
    params_req = DatabaseObject.params_req + ['databaseName', 'identifier', 'url']
    prtfmt = '{dbId:7} {schemaClass:32} {abc} {databaseName}:{identifier} {displayName}'

    relationships = {
        'referenceDatabase': set(['ReferenceDatabase']),
        'crossReference'   : set(['DatabaseIdentifier']),
        'species'          : set(['Taxon']),
    }

    flds_last = ' abc optional'
    ntobj = namedtuple('NtOpj', ' '.join(params_req) + flds_last)

    def __init__(self, name='ReferenceEntity', dbid=None):
        super(ReferenceEntity, self).__init__(name, dbid)

    def get_dict(self, node):
        """Given a Neo4j Node, return a dict containing parameters."""
        k2v = DatabaseObject.get_dict(self, node)
        # speciesName is not a param, but species may be found through relationship
        k2v['abc'] = '...'
        return k2v

    def get_nt(self, node):
        """Given a Neo4j Node, return a namedtuple containing parameters."""
        # print('FMTFFFFFFFFFFFFFF', self.prtfmt)
        # print('NTFLDSNNNNNNNNNNN', self.ntobj._fields)
        # print('DICTDDDDDDDDDDDDD', self.get_dict(node))
        return self.ntobj(**self.get_dict(node))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
