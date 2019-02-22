"""Read a Reactome pathway analysis results file. Store in a Python var"""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
import csv
import collections as cx


class ReactomeCsv(object):
    """Read a Reactome pathway analysis results file. Store in a Python var"""

    floats = set(['Entities_pValue', 'Entities_ratio', 'Entities_FDR', 'Reactions_ratio'])
    splits_semicolon = set([
        'Submitted_entities_found',
        'Mapped_entities',
        'Found_reaction_identifiers'])

    def __init__(self, fin_csv):
        self.fin_csv = fin_csv
        self.hdrs = None
        self.results = self._init_results()
        assert self.hdrs is not None, "NO HEADERS READ: {CSV}".format(CSV=fin_csv)

    def _init_results(self):
        """Read a Reactome pathway analysis results file. Store in a Python var"""
        with open(self.fin_csv) as ifstrm:
            nts = []
            ntobj = None
            for flds in csv.reader(ifstrm):
                if self.hdrs:
                    dct = self._get_dict_flds(flds)
                    # pylint: disable=not-callable
                    nts.append(ntobj(**dct))
                else:
                    self.hdrs = self._nthdrs(flds)
                    ntobj = cx.namedtuple("ntpw", " ".join(self.hdrs))
            # pylint: disable=superfluous-parens
            print("  READ: {CSV}".format(CSV=self.fin_csv))
            return nts

    def _get_dict_flds(self, flds):
        """Get data from a row of csv format, return in a Python dict.
               Entities_pValue      0.976271665748
               num_Entities_found   1
               Mapped_entities      ['P28070']
               Entities_ratio       0.0852216304053
               Pathway_name         Adaptive Immune System
               num_Reactions_total  252
               Entities_FDR         0.976271665748
               Pathway_identifier   R-HSA-1280218
               num_Reactions_found  5
               Reactions_ratio      0.0221967761825
               num_Entities_total   944
               Found_reaction_identifiers ['R-HSA-983150', 'R-HSA-1168640', ...]
               Species_name         Homo sapiens
               Submitted_entities_found ['6700']
               Species_identifier   9606
        """
        # pylint: disable=undefined-variable
        assert len(self.hdrs) == len(flds), "{} {}".format(len(hdrs), len(flds))
        dct = {k:self._get_val(k, v) for k, v in zip(self.hdrs, flds)}
        # for k, v in dct.items():
        #   print("{K:20} {V}".format(K=k, V=v))
        #### assert len(dct['Mapped_entities']) == len(dct['Submitted_entities_found'])
        return dct

    def _get_val(self, key, val):
        """Given string value, return value with correct type."""
        if key in self.floats:
            return float(val)
        if key[:4] == 'num_' or key == 'Species_identifier':
            return int(val)
        if key in self.splits_semicolon:
            return val.split(';')

    @staticmethod
    def _nthdrs(hdrs):
        """Turn csv headers into legal namedtuple field names."""
        ntflds = []
        for hdr in hdrs:
            hdr = hdr.replace(' ', '_')
            if hdr[0] == '#':
                hdr = 'num_' + hdr[1:]
            ntflds.append(hdr)
        return ntflds

# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
