#!/usr/bin/env python
"""Report counts of all relationships related to a schemaName for a single species.

Usage: get_relationship_cnts.py <neo4j_password> [--schemaClass=CLS] [--species=S]

Options:
  -h --help
  -c --schemaClass=CLS  Examples: Complex, Pathway, etc. [default: Complex]
  -s --species=S        Species [default: Homo sapiens]


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
    # https://reactome.org/content/schema/Complex

    qry = "".join([
        'MATCH (src:{--schemaClass}{{speciesName:"{--species}"}})-'.format(**args),
        '[rel]->(dst) RETURN src, rel, dst'])

    complex2rel2cnt = cx.defaultdict(cx.Counter)
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', args['<neo4j_password>']))
    with gdbdr.session() as session:
        ctr = cx.Counter()
        for rec in session.run(qry).records():
            rel = rec['rel']
            stid_complex = rec['src'].get('stId')
            rel_type = rel.type
            dst_cls = rec['dst']['schemaClass']
            key = (rel_type, dst_cls)
            complex2rel2cnt[stid_complex][key] += 1
            # print(stid_complex, rel_type, rec['dst']['schemaClass'])
            ctr[key] += 1

    print('\n{N:6} {--schemaClass} for {--species}'.format(
        N=len(complex2rel2cnt), **args))
        # N=len(complex2rel2cnt), schemaClass=schemaclass, species=species))
    print('\n Total  num/ID Relationship')
    print(' ----- ------- -------------------------')
    for typ, tot in sorted(ctr.items(), key=lambda t: [t[0][0], -1*t[1]]):
        #### mean = _get_mean_cnt(typ, complex2rel2cnt)
        mean = statistics.mean(c for r2c in complex2rel2cnt.values() for r, c in r2c.items() if r==typ)
        # mean = 0
        print('{N:6} {MEAN:7.4f} {TYPE}'.format(TYPE=typ, N=tot, MEAN=mean))


if __name__ == '__main__':
    main()  # *_get_args())

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
