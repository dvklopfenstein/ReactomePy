#!/usr/bin/env python
"""Report counts of all relationships related to all Complexes in one species.

 11772 Complex for Homo sapiens

 Total num/ID  Relationship
 ----- ------- -------------------------
 90665 10.0560 inferredTo
 28759  2.4430 hasComponent
 11964  1.0163 species
 11792  1.0017 compartment
  4404  1.2437 includedLocation
  3559  1.5414 literatureReference
   915  1.8119 disease
   538  1.5964 relatedSpecies
   331  1.0061 summation
   298  1.1418 crossReference
   239  1.1065 entityOnOtherCell
   164  1.0000 goCellularComponent
     1  1.0000 figure
"""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import statistics
import collections as cx
from neo4j import GraphDatabase


def main(password, schemaclass='Complex', species='Homo sapiens'):
    """Report counts of all relationships related to all Complexes in one species."""
    # https://reactome.org/content/schema/Complex

    qry = "".join([
        'MATCH (src:{schemaClass}{{speciesName:"{species}"}})-'.format(
            schemaClass=schemaclass, species=species),
        '[rel]->(dst) RETURN src, rel, dst'])

    complex2rel2cnt = cx.defaultdict(cx.Counter)
    gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    with gdbdr.session() as session:
        ctr = cx.Counter()
        for rec in session.run(qry).records():
            rel = rec['rel']
            stid_complex = rec['src'].get('stId')
            rel_type = rel.type
            complex2rel2cnt[stid_complex][rel_type] += 1
            # print(stid_complex, rel_type, rel)
            ctr[rel_type] += 1

    print('\n{N:6} {schemaClass} for {species}'.format(
        N=len(complex2rel2cnt), schemaClass=schemaclass, species=species))
    print('\n Total  num/ID Relationship')
    print(' ----- ------- -------------------------')
    for typ, tot in ctr.most_common():
        mean = _get_mean_cnt(typ, complex2rel2cnt)
        print('{N:6} {MEAN:7.4f} {TYPE}'.format(TYPE=typ, N=tot, MEAN=mean))

def _get_mean_cnt(typ, complex2rel2cnt):
    """Get the mean count of a relationship count."""
    cnts = []
    for rel2cnt in complex2rel2cnt.values():
        for rel, cnt in rel2cnt.items():
            if rel == typ:
                cnts.append(cnt)
    return statistics.mean(cnts)

def _get_args():
    """Get args."""
    num_args = len(sys.argv)
    assert num_args != 1, 'First arg must be your Neo4j database password'
    return [sys.argv[1],
            sys.argv[2] if num_args == 3 else 'Complex',
            sys.argv[3] if num_args == 4 else 'Homo sapiens']


if __name__ == '__main__':
    main(*_get_args())

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
