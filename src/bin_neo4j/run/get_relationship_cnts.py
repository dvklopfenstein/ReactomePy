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

# Example for relationships for human complexes:
#
#  11772 Complex for Homo sapiens
#
#  Total num/ID  Relationship
#  ----- ------- -------------------------
#  90665 10.0560 inferredTo
#  28759  2.4430 hasComponent
#  11964  1.0163 species
#  11792  1.0017 compartment
#   4404  1.2437 includedLocation
#   3559  1.5414 literatureReference
#    915  1.8119 disease
#    538  1.5964 relatedSpecies
#    331  1.0061 summation
#    298  1.1418 crossReference
#    239  1.1065 entityOnOtherCell
#    164  1.0000 goCellularComponent
#      1  1.0000 figure

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import statistics
import collections as cx
from docopt import docopt
from neo4j import GraphDatabase


def main():  # password, schemaclass='Complex', species='Homo sapiens'):
    """Report counts of all relationships related to all Complexes in one species."""
    args = docopt(__doc__)
    print(args)

    species = '{{speciesName:"{--species}"}}'.format(**args) if args['--species'] else ''
    qry = "".join([
        'MATCH (src:{--schemaClass}{SPECIES})-'.format(SPECIES=species, **args),
        '[rel]->(dst) RETURN src, rel, dst'])

    id2rel2cnt = cx.defaultdict(cx.Counter)
    ctr = cx.Counter()
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', args['<neo4j_password>']))
    print('QUERY: {Q}'.format(Q=qry))
    with gdbdr.session() as session:
        for idx, rec in enumerate(session.run(qry).records()):
            stid_complex = rec['src'].get('stId')
            key = _get_key(rec, args)
            id2rel2cnt[stid_complex][key] += 1
            ctr[key] += 1
            if idx%5000 == 0:
                print('{I:7} {ID:13} {SRC:30} {TYPE:20} {DST} ...'.format(
                    I=idx, ID=stid_complex, TYPE=rec['rel'].type,
                    SRC=rec['src']['schemaClass'],
                    DST=rec['dst']['schemaClass']))
    _write(ctr, id2rel2cnt, args)

def _get_key(rec, args):
    """Get key."""
    if args['-r']:
        return (rec['src']['schemaClass'], rec['rel'].type, rec['dst']['schemaClass'])
    else:
        return (args['--schemaClass'], rec['rel'].type, rec['dst']['schemaClass'])

def _write(ctr, id2rel2cnt, args):
    """Write results to a file or to the screen."""
    if ctr:
        if args['-o']:
            fout_txt = _get_fout(args)
            with open(fout_txt, 'w') as prt:
                _prt(ctr, id2rel2cnt, args, prt)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))
        else:
            _prt(ctr, id2rel2cnt, args, sys.stdout)

def _get_fout(args):
    """Return an automatically generated filename to store results."""
    fout_txt = ['relationship_r{REL}_'.format(REL=int(args['-r']))]
    if args['--species'] != '':
        fout_txt.append('{ORG}_'.format(ORG=args['--species'].replace(' ', '_')))
    fout_txt.append(args['--schemaClass'])
    fout_txt.append('.txt')
    return ''.join(fout_txt)

def _prt(ctr, id2rel2cnt, args, prt):
    """Write results."""
    title = '{N} {--schemaClass} for species({--species})'.format(N=len(id2rel2cnt), **args)
    prt.write('\n{TITLE}\n'.format(TITLE=title))
    prt.write('\n Total  num/ID Source Type                    Relationship           Destination Type\n')
    prt.write(  ' ----- ------- ------------------------------ ---------------------- ----------------\n')
    for typ, tot in sorted(ctr.items(), key=lambda t: [t[0][0], t[0][1], -1*t[1]]):
        mean = statistics.mean(c for r2c in id2rel2cnt.values() for r, c in r2c.items() if r == typ)
        prt.write('{N:6} {MEAN:7.4f} {SRC:30} {REL:22} {DST}\n'.format(
            SRC=typ[0], REL=typ[1], DST=typ[2], N=tot, MEAN=mean))
    print(title)


if __name__ == '__main__':
    main()  # *_get_args())

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
