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
  --csv=CSV      Write pathway enrichment analysis into a csv file [default: pathway_enrichment.csv]
  --ids0=NF      Write list of identifiers that were not found [default: ids_mapping.csv]
  --ids1=F       Write list of identifiers that were found [default: ids_notfound.csv]
  --prefix=PREFIX  Add a prefix to all output files
  --tokenlog=TOKEN    File containing a log of all new tokens [default: tokens.log]

  --resource=STR  Resources like TOTAL, UNIPROT, ENSEMBL, etc. [default: TOTAL]
  --sortBy=STR    Sort pathway enrichment results [default: ENTITIES_PVALUE]
  --order=STR     order by ASC or DESC [default: ASC]
  --pValue=FLOAT  Keep values with pvalues [default: 1.0]
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from docopt import docopt
from reactomepy.code.rest.service_analysis import AnalysisService
from reactomepy.code.rest.token_mgr import TokenManager
from enrichmentanalysis.file_utils import clean_args
from enrichmentanalysis.file_utils import prepend
from enrichmentanalysis.file_utils import get_fout_pdf


def main():
    """Run Reactome's Pathway Enrichment Analysis UniProt example."""
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
        tok.pdf_report(prepend(pre, fout_pdf), resource=args['resource'])
    tok.csv_pathways(prepend(pre, args['csv']), resource=args['resource'])
    tok.csv_found(prepend(pre, args['ids0']), resource=args['resource'])
    tok.csv_notfound(prepend(pre, args['ids1']))

def get_kws_analyse(args):
    """Get keyword args used when running a pathway analysis."""
    kws = {}
    if 'interactors' in args and args['interactors']:
        kws['interactors'] = True
    if 'excludeDisease' in args and args['excludeDisease']:
        kws['includeDisease'] = False
    kws['pValue'] = float(args['pValue'])
    for key in set(['sortBy', 'order', 'resource']).intersection(args.keys()):
        kws[key] = args[key]
    return kws


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
