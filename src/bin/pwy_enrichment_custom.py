#!/usr/bin/env python
"""Pathway enrichment analysis with user-provided population and associations.

Usage:
    example_pathway_enrichment.py <study_ids> <population_ids> <pathway_associations> [options]

Options:
  -h --help             Show usage
  --csv=CSV  Write pathway enrichment analysis into a csv file [default: pw_pathway_enrichment_custom.csv]
  --csv0=NF  Write list of identifiers that were not found [default: pw_ids_found.csv]
  --csv1=F   Write list of identifiers that were found [default: pw_ids_notfound.csv]
  -b --base  Prepend a basename to all output files [default: pw]
"""


__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
from docopt import docopt
from reactomeneo4j.code.enrich.file_utils import read_ids
from reactomeneo4j.code.enrich.file_utils import read_associations
from reactomeneo4j.code.enrich.enrich_pwy import PathwayEnrichment


def main():
    """Pathway enrichment analysis with user-provided population and associations."""
    args = docopt(__doc__)
    print(args)

    stu_ids = read_ids(args['<study_ids>'])
    pop_ids = read_ids(args['<population_ids>'])
    assc = read_associations(args['<pathway_associations>'])
    obj = PathwayEnrichment(pop_ids, assc)
    results = obj.run_study(stu_ids)
    # Write Pathway Enrichment Analysis to a file
    # ana.csv_pathways(args['--csv'], token, resource='TOTAL')
    # ana.csv_found(args['--csv0'], token, resource='TOTAL')
    # ana.csv_notfound(args['--csv1'], token)


if __name__ == '__main__':
    main()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
