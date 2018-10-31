"""Manages Publications: Research papers, books, and URLs."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomeneo4j.data.species import SPECIES
# from reactomeneo4j.data.species_commonnames import TAXID2NAMES


class Species(object):
    """Manages a list of taxids for various species."""

    # nt: abc abbreviation taxId displayName
    taxid2nt = {nt.taxId:nt for nt in SPECIES}
    pat = '{taxId:7} {abc} {displayName}\n'

    def prt_taxids(self, taxids, prt=sys.stdout, sortby=None):
        """Print a list of taxids, including their species name and abbreviation."""
        taxid2nt = self.get_taxid2nt(taxids)
        for taxid, ntd in self._get_sorted(taxid2nt, sortby):
            prt.write(self.pat.format(**ntd._asdict()))
        for taxid in set(taxids).difference(set(taxid2nt)):
            prt.write('**WARNING: TAXID NOT FOUND: {TAXID}\n'.format(TAXID=taxid))

    def get_taxid2nt(self, taxids):
        """Get a list of taxids, including their species name and abbreviation."""
        taxid2nt = {}
        for taxid in taxids:
            if taxid in self.taxid2nt:
                taxid2nt[taxid] = self.taxid2nt[taxid]
        return taxid2nt

    @staticmethod
    def _get_sorted(taxid2nt, sortby):
        """Sort taxids."""
        if sortby is None:
            return sorted(taxid2nt.items(), key=lambda t: [t[1].abc, t[1].taxId])
        elif sortby:
            return sorted(taxid2nt.items(), key=sortby)
        else:
            return taxid2nt.items()


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
