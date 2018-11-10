"""Report counts of all relationships related to a schemaName for a single species."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import statistics
import collections as cx
from neo4j import GraphDatabase


class RelationshipCnt(object):
    """Report the relationships found on an item."""

    def __init__(self, password):
        self.gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
        # Set by set_query
        self.query = None
        # Set by set_data:
        self.ctr = None
        self.id2rel2cnt = None

    def run_query(self, src_schemaclass):
        """Count relationships for all Nodes returned by query."""
        id2rel2cnt = cx.defaultdict(cx.Counter)
        ctr = cx.Counter()
        print('QUERY: {Q}'.format(Q=self.query))
        with self.gdbdr.session() as session:
            for idx, rec in enumerate(session.run(self.query).records()):
                stid_complex = rec['src'].get('stId')
                key = self._get_key(rec, src_schemaclass)
                id2rel2cnt[stid_complex][key] += 1
                ctr[key] += 1
                if idx%5000 == 0:
                    print('    record: {I:7} {ID:13} {SRC:30} {TYPE:20} {DST} ...'.format(
                        I=idx, ID=stid_complex, TYPE=rec['rel'].type,
                        SRC=rec['src']['schemaClass'],
                        DST=rec['dst']['schemaClass']))
        self.ctr = ctr
        self.id2rel2cnt = id2rel2cnt

    def set_query(self, schemaclass, species):
        """Create a query and store it."""
        node_species = '{{speciesName:"{species}"}}'.format(species=species) if species else ''
        self.query = "".join([
            'MATCH (src:{schemaClass}{S})-'.format(S=node_species, schemaClass=schemaclass),
            '[rel]->(dst) RETURN src, rel, dst'])

    @staticmethod
    def _get_key(rec, src_schemaclass):
        """Get key."""
        if src_schemaclass:
            return (src_schemaclass, rec['rel'].type, rec['dst']['schemaClass'])
        return (rec['src']['schemaClass'], rec['rel'].type, rec['dst']['schemaClass'])

    @staticmethod
    def get_fout(schemaclass, species, recursive):
        """Return an automatically generated filename to store results."""
        fout_txt = ['relationship_r{REL}_'.format(REL=int(recursive))]
        if species != '':
            fout_txt.append('{ORG}_'.format(ORG=species.replace(' ', '_')))
        fout_txt.append(schemaclass)
        fout_txt.append('.txt')
        return ''.join(fout_txt)

    def wrtxt(self, fout_txt):
        """Write results to a file or to the screen."""
        if self.ctr:
            with open(fout_txt, 'w') as prt:
                self.prt(prt)
                print('  WROTE: {TXT}'.format(TXT=fout_txt))

    def prt(self, prt):
        """Write results."""
        # pylint: disable=line-too-long
        title = '{N} schemaClasses'.format(N=len(self.id2rel2cnt))
        prt.write('{QUERY}\n'.format(QUERY=self.query))
        prt.write('\n{TITLE}\n'.format(TITLE=title))
        prt.write('\n Total  num/ID Source Type                    Relationship           Destination Type\n')
        prt.write(' ----- ------- ------------------------------ ---------------------- ----------------\n')
        for typ, tot in sorted(self.ctr.items(), key=lambda t: [t[0][0], t[0][1], -1*t[1]]):
            mean = statistics.mean(c for r2c in self.id2rel2cnt.values() for r, c in r2c.items() if r == typ)
            prt.write('{N:6} {MEAN:7.4f} {SRC:30} {REL:22} {DST}\n'.format(
                SRC=typ[0], REL=typ[1], DST=typ[2], N=tot, MEAN=mean))
        print(title)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
