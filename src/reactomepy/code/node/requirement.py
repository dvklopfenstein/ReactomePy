"""Reactome PhysicalEntity Neo4j Node.

    - Regulation (dcnt=5)
  > -- PositiveRegulation (dcnt=2)
  > --- PositiveGeneExpressionRegulation (dcnt=0)
  > --- Requirement (dcnt=0)
  > -- NegativeRegulation (dcnt=1)
  > --- NegativeGeneExpressionRegulation (dcnt=0)

  5,262 Regulation   1963 PositiveRegulation                   42   1963  0.0214 name
  5,262 Regulation   1963 PositiveRegulation                  373   1963  0.1900 oldStId
  5,262 Regulation   1963 PositiveRegulation                  588   1963  0.2995 stId
  5,262 Regulation   1963 PositiveRegulation                  588   1963  0.2995 stIdVersion

  5,262 Regulation   1835 NegativeRegulation                   37   1835  0.0202 name
  5,262 Regulation   1835 NegativeRegulation                  245   1835  0.1335 oldStId
  5,262 Regulation   1835 NegativeRegulation                  443   1835  0.2414 stId
  5,262 Regulation   1835 NegativeRegulation                  443   1835  0.2414 stIdVersion

  5,262 Regulation    672 PositiveGeneExpressionRegulation     82    672  0.1220 name
  5,262 Regulation    672 PositiveGeneExpressionRegulation    324    672  0.4821 oldStId
  5,262 Regulation    672 PositiveGeneExpressionRegulation    569    672  0.8467 stId
  5,262 Regulation    672 PositiveGeneExpressionRegulation    569    672  0.8467 stIdVersion

  5,262 Regulation    595 Requirement                          12    595  0.0202 name
  5,262 Regulation    595 Requirement                          84    595  0.1412 oldStId
  5,262 Regulation    595 Requirement                         154    595  0.2588 stId
  5,262 Regulation    595 Requirement                         154    595  0.2588 stIdVersion

  5,262 Regulation    197 NegativeGeneExpressionRegulation     53    197  0.2690 name
  5,262 Regulation    197 NegativeGeneExpressionRegulation     34    197  0.1726 oldStId
  5,262 Regulation    197 NegativeGeneExpressionRegulation    151    197  0.7665 stId
  5,262 Regulation    197 NegativeGeneExpressionRegulation    151    197  0.7665 stIdVersion
"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.node.positiveregulation import PositiveRegulation


# pylint: disable=too-few-public-methods
class Requirement(PositiveRegulation):
    """Params seen on all Physical Entities."""

    # params_req: dbId schemaClass displayName
    # params_opt:= oldStId name stId stIdVersion

    relationships = {
        **PositiveRegulation.relationships,
        **{
            'literatureReference': frozenset(['LiteratureReference']),
            'regulator': frozenset(['CandidateSet',
                                    'DefinedSet',
                                    'EntityWithAccessionedSequence',
                                    'Complex',
                                    'SimpleEntity',
                                    ]),
        }
    }

    def __init__(self):
        super(Requirement, self).__init__('Requirement')


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
