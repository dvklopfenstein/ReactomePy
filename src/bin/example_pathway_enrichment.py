#!/usr/bin/env python
"""Run Reactome's Pathway Enrichement Analysis UniProt example.

Usage: example_pathway_enrichment.py [token]

Options:
  -h --help  Show usage
  -t --token  Provide token representing a completed analysis
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
# from reactomeneo4j.code.utils import get_args
from reactomeneo4j.code.rest.service_analysis import AnalysisService
from reactomeneo4j.code.ex.uniprot_accession_list import SAMPLE_NAME
from reactomeneo4j.code.ex.uniprot_accession_list import DATA


def main():
    """Run Reactome's Pathway Enrichement Analysis UniProt example."""
    obj = _Run()

    # Run pathway enrichment analysis example and get the associated identifying token:
    #     sample_name: GBM Uniprot
    #     data: P01023 Q99758 O15439 O43184 Q13444 P82987
    token = obj.get_token(DATA, SAMPLE_NAME)


class _Run():
    """Run Reactome's Pathway Enrichement Analysis UniProt example."""

    def __init__(self):
        self.objana = AnalysisService()

    def get_token(self, data, sample_name):
        """Return a token associated with a Pathway enrichment analysis."""
        args = docopt(__doc__)
        # If user provides no token, then run a Pathway enrichemtn analysis. Return token
        if not args['token']:
            rsp = self.objana.post_ids(data, sample_name)
            assert 'summary' in rsp, rsp
            token = rsp['summary']['token']
            print(token)
            return token
        return args['token']


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
