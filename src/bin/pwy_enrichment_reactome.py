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
  --pdf=PDF    Write pathway report into pdf file [default: pathway_enrichment.pdf]
  --xlsx=XLSX  Write enrichment analysis into a xlsx file [default: enrichment.xlsx]
  --tsv=TSV    Write enrichment analysis into a tsv file
  --csv=CSV    Write pathway enrichment analysis into a csv file [default: pathway_enrichment.csv]
  --ids0=NF    Write list of identifiers that were not found [default: ids_mapping.csv]
  --ids1=F     Write list of identifiers that were found [default: ids_notfound.csv]
  -p --prefix=PREFIX  Add a prefix to all output files
  --tokenlog=TOKEN    File containing a log of all new tokens [default: tokens.log]
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
#### from reactomepy.code.utils import get_args
from reactomepy.code.rest.service_analysis import AnalysisService
from enrichmentanalysis.file_utils import clean_args
from enrichmentanalysis.file_utils import prepend
from enrichmentanalysis.file_utils import read_ids


def main():
    """Run Reactome's Pathway Enrichment Analysis UniProt example."""
    ana = AnalysisService('tokens.log')
    #### args = get_args(__doc__, {'token', 'pdf', 'csv', 'data', 'sample_name'})
    docargs = docopt(__doc__)
    args = clean_args(docargs)
    print('\n'.join(['{A:12} {V}'.format(A=a, V=v) for a, v in args.items()]))
    study_ids = args.get('study_IDs_file')

    # Run pathway enrichment analysis example and get the associated identifying token:
    to_hsa = 'noProject2human' not in args
    token = ana.get_token(study_ids, args.get('token'), to_hsa, **_get_kws_analyse(args))

    # Write Pathway Enrichment Analysis to a file
    pre = args.get('prefix')
    #ana.pdf_report(prepend(pre, args['pdf']), token)
    ana.csv_pathways(prepend(pre, args['csv']), token, resource='TOTAL')
    ana.csv_found(prepend(pre, args['ids0']), token, resource='TOTAL')
    ana.csv_notfound(prepend(pre, args['ids1']), token)

def _get_kws_analyse(args):
    """Get keyword args used when running a pathway analysis."""
    kws = {}
    if 'interactors' in args and args['interactors']:
        kws['interactors'] = True
    if 'excludeDisease' in args and args['excludeDisease']:
        kws['includeDisease'] = False
    return kws


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
