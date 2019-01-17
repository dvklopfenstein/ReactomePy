#!/usr/bin/env python
"""Run Reactome's Pathway Enrichment Analysis using their REST Service.

Usage:
    example_pathway_enrichment.py [options]

Options:
  -h --help           Show usage
  -d --data=FILE      File containing a list of identifiers
  --name=SAMPLE_NAME  Sample name
  -t --token=TOKEN    Provide token representing a completed analysis.
                      Tokens are used to access a previous analysis.
  --pdf=PDF  Write pathway report into pdf file [default: pathway_enrichment.pdf]
  --csv=CSV  Write pathway enrichment analysis into a csv file [default: pathway_enrichment.csv]
  --csv0=NF  Write list of identifiers that were not found [default: ids_found.csv]
  --csv1=F   Write list of identifiers that were found [default: ids_notfound.csv]

"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
#### from reactomeneo4j.code.utils import get_args
from reactomeneo4j.code.rest.service_analysis import AnalysisService
from reactomeneo4j.code.ex.uniprot_accession_list import SAMPLE_NAME
from reactomeneo4j.code.ex.uniprot_accession_list import DATA


def main():
    """Run Reactome's Pathway Enrichment Analysis UniProt example."""
    ana = AnalysisService()
    #### args = get_args(__doc__, {'token', 'pdf', 'csv', 'data', 'sample_name'})
    args = docopt(__doc__)
    print(args)

    # Run pathway enrichment analysis example and get the associated identifying token:
    #     sample_name: GBM Uniprot
    #     data: P01023 Q99758 O15439 O43184 Q13444 P82987
    token = _get_token(DATA, SAMPLE_NAME, args.get('--token'), ana)

    # Write Pathway Enrichment Analysis to a file
    ana.pdf_report(args['--pdf'], token)
    ana.csv_pathways(args['--csv'], token, resource='TOTAL')
    ana.csv_found(args['--csv0'], token, resource='TOTAL')
    ana.csv_notfound(args['--csv1'], token)


def _get_token(data, sample_name, token, ana):
    """Return a token associated with a Pathway enrichment analysis."""
    # If user provides no token, then run a Pathway enrichemtn analysis. Return token
    if token is None:
        rsp = ana.post_ids(data, sample_name)
        print(rsp)
        assert 'summary' in rsp, rsp
        token = rsp['summary']['token']
        print('TOKEN: {T}'.format(T=token))
        return token
    return token


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
