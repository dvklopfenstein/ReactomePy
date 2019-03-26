#!/usr/bin/env python3
"""Run Reactome's Pathway Enrichment Analysis using their REST Service.

Usage:
    example_pathway_enrichment.py (<study_ids>| --token=TOKEN) [options]

Options:
  -h --help           Show usage
  -t --token=TOKEN    Provide token representing a completed analysis.
                      Tokens are used to access a previous analysis.
  --pdf=PDF    Write pathway report into pdf file [default: pathway_enrichment.pdf]
  --xlsx=XLSX  Write enrichment analysis into a xlsx file [default: enrichment.xlsx]
  --tsv=TSV    Write enrichment analysis into a tsv file
  --csv=CSV  Write pathway enrichment analysis into a csv file [default: pathway_enrichment.csv]
  --ids0=NF  Write list of identifiers that were not found [default: ids_found.csv]
  --ids1=F   Write list of identifiers that were found [default: ids_notfound.csv]
  -b --base=BASE    Prepend a basename to all output files
  --tokenlog=TOKEN  File containing a log of all new tokens [default: tokens.log]
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
#### # import sys
#### from docopt import docopt
#### #### from reactomepy.code.utils import get_args
from reactomepy.code.rest.service_analysis import AnalysisService
#### from enrichmentanalysis.file_utils import clean_args
#### from enrichmentanalysis.file_utils import prepend
from enrichmentanalysis.file_utils import read_ids

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")


def main():
    """Run Reactome's Pathway Enrichment Analysis UniProt example."""
    fout_token = os.path.join(REPO, 'tokens.log')
    ana = AnalysisService(fout_token)
    args = {
        'study_ids': os.path.join(REPO, 'data/enrich/studyids/1q21o3.txt')
    }
    print(args)
    study_dct = read_ids(args['study_ids'])
    for idx, txt in enumerate(study_dct['ids']):
        print('{N:2} {ID}'.format(N=idx, ID=txt))

    # # Run pathway enrichment analysis example and get the associated identifying token:
    # #     sample_name: GBM Uniprot
    # #     data: P01023 Q99758 O15439 O43184 Q13444 P82987
    # token = ana.get_token(**study_dct, token=args.get('token'))

    # # Write Pathway Enrichment Analysis to a file
    # base = args.get('base')
    # ana.pdf_report(prepend(base, args['pdf']), token)
    # ana.csv_pathways(prepend(base, args['csv']), token, resource='TOTAL')
    # ana.csv_found(prepend(base, args['csv0']), token, resource='TOTAL')
    # ana.csv_notfound(prepend(base, args['csv1']), token)


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
