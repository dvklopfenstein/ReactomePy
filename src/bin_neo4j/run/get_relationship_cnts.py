#!/usr/bin/env python
"""Report counts of all relationships related to a schemaName for a single species.

Usage: get_relationship_cnts.py <neo4j_password> [--schemaClass=CLS] [--species=S] [-o] [-r]

Options:
  -h --help
  -c --schemaClass=CLS  Examples: Complex, Pathway, etc. [default: Complex]
  -s --species=S        Species [default: Homo sapiens]
  -o                    Write results into a file rather than to the screen
  -r                    Report lower-level source schema

"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from docopt import docopt
from reactomeneo4j.code.run.get_relationship_cnts import RelationshipCnt


def main():  # password, schemaclass='Complex', species='Homo sapiens'):
    """Report counts of all relationships related to all Complexes in one species."""
    args = docopt(__doc__)
    obj = RelationshipCnt(args['<neo4j_password>'])
    obj.set_query(args['--schemaClass'], args['--species'])

    # Collect counts of leaf-level schemaClass or from higher-level user-specified schemaClass
    src_schemaclass = None if args['-r'] else args['--schemaClass']
    obj.run_query(src_schemaclass)

    # Write results
    if args['-o']:
        fout_txt = obj.get_fout(args['--schemaClass'], args['--species'], args['-r'])
        obj.wrtxt(fout_txt)
    else:
        obj.prt(sys.stdout)


if __name__ == '__main__':
    main()  # *_get_args())

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
