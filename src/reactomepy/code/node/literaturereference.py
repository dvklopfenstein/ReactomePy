"""Reactome LiteratureReference Neo4j Node.

    - Publication (dcnt=3)
  > -- Book (dcnt=0)
  > -- LiteratureReference (dcnt=0)
  > -- URL  (dcnt=0)

28,896 Publication   28758 LiteratureReference   28758  28758  1.0000 journal
28,896 Publication   28758 LiteratureReference   28584  28758  0.9939 pages
28,896 Publication   28758 LiteratureReference   28744  28758  0.9995 pubMedIdentifier
28,896 Publication   28758 LiteratureReference   28596  28758  0.9944 volume
28,896 Publication   28758 LiteratureReference   28758  28758  1.0000 year

28,896 Publication     117 Book                    101    117  0.8632 ISBN
28,896 Publication     117 Book                     84    117  0.7179 chapterTitle
28,896 Publication     117 Book                     74    117  0.6325 pages
28,896 Publication     117 Book                    117    117  1.0000 year

28,896 Publication      21 URL                      21     21  1.0000 uniformResourceLocator
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomepy.code.node.publication import Publication


# pylint: disable=too-few-public-methods
class LiteratureReference(Publication):
    """Params seen on all LiteratureReference."""

    # params: dbId schemaClass displayName | title
    params_req = Publication.params_req + ('journal', 'year')
    params_opt = Publication.params_opt + ('pubMedIdentifier', 'volume', 'pages')
    prtfmt = '{schemaClass}: {year} ({journal}) {displayName}'
    ntobj = namedtuple('NtObj', ' '.join(params_req) + ' optional')

    def __init__(self):
        super(LiteratureReference, self).__init__('LiteratureReference')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
