#!/usr/bin/env python3
"""Run Reactome's Pathway Enrichment Analysis using their REST Service.

Usage:
    example_pathway_enrichment.py (<study_IDs_file>| --token=TOKEN) [options]

Options:
  -h --help         Show usage
  -t --token=TOKEN  Provide token representing a completed analysis.
                    Tokens are used to access a previous analysis.
  --noProject2human  Do not convert all non-human identifiers to their human equivalents
  --interactors     Include interactors
  --excludeDisease  Exclude disease pathways
  --pdf          Write pathway report into pathway_enrichment.pdf
  --pdfname=PDF  Specify pathway report name
  --xlsx=XLSX    Write enrichment analysis into a xlsx file [default: enrichment.xlsx]
  --tsv=TSV      Write enrichment analysis into a tsv file
  --csv=CSV      Write pathway enrichment analysis into a csv file [default: pathway_enrichment.csv]
  --ids0=NF      Write list of identifiers that were not found [default: ids_mapping.csv]
  --ids1=F       Write list of identifiers that were found [default: ids_notfound.csv]
  -p --prefix=PREFIX  Add a prefix to all output files
  --tokenlog=TOKEN    File containing a log of all new tokens [default: tokens.log]
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
from reactomepy.code.rest.service_analysis import AnalysisService
from reactomepy.code.rest.token_mgr import TokenManager
from enrichmentanalysis.file_utils import clean_args
from enrichmentanalysis.file_utils import prepend
from enrichmentanalysis.file_utils import get_fout_pdf
from enrichmentanalysis.file_utils import get_kws_analyse


def main():
    """Run Reactome's Pathway Enrichment Analysis UniProt example."""
    #### args = get_args(__doc__, {'token', 'pdf', 'csv', 'data', 'sample_name'})
    docargs = docopt(__doc__)
    args = clean_args(docargs)
    ana = AnalysisService(args['tokenlog'])
    print('\n'.join(['{A:12} {V}'.format(A=a, V=v) for a, v in args.items()]))
    study_ids = args.get('study_IDs_file')

    # Run pathway enrichment analysis example and get the associated identifying token:
    to_hsa = 'noProject2human' not in args
    token = ana.get_token(study_ids, args.get('token'), to_hsa, **get_kws_analyse(args))

    # Write Pathway Enrichment Analysis to a file
    tok = TokenManager(token)
    pre = args.get('prefix')
    if 'pdf' in args or 'pdfname' in args:
        fout_pdf = get_fout_pdf(args)
        tok.pdf_report(prepend(pre, fout_pdf))
    tok.csv_pathways(prepend(pre, args['csv']), resource='TOTAL')
    tok.csv_found(prepend(pre, args['ids0']), resource='TOTAL')
    tok.csv_notfound(prepend(pre, args['ids1']))


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
