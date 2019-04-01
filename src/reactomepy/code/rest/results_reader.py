"""Read a Reactome pathway analysis results file. Store in a Python var"""

__copyright__ = "Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import csv
import collections as cx


class ReactomeResultsCsv():
    """Read a Reactome pathway analysis results file. Store in a Python var"""

    chk_flds = {
        'Pathway_name',
        'num_Entities_found', 'num_Entities_total',
        'num_Reactions_found', 'num_Reactions_total',
        'Species_identifier', 'Species_name',
        #'Submitted_entities_found',  # =['Q5K4L6'],
        # Found_reaction_identifiers=['R-HSA-8875077'])
        # Mapped_entities=[''],
        # Entities_pValue=0.9999691890340465, Entities_FDR=0.9999691890340465,
    }

    floats = set(['Entities_pValue', 'Entities_ratio', 'Entities_FDR', 'Reactions_ratio'])
    splits_semicolon = {
        'Submitted_entities_found',
        'Mapped_entities',
        'Found_reaction_identifiers'}

    def __init__(self, fin_csv):
        self.fin_csv = fin_csv
        self.hdrs = None
        self.results = self._init_results()
        assert self.hdrs is not None, "NO HEADERS READ: {CSV}".format(CSV=fin_csv)

    def get_items(self, attrname='Submitted_entities_found'):
        """Return a set of items for all results."""
        items = set()
        assert attrname in self.splits_semicolon, 'ATTR({A}) NOT IN: {S}'.format(
            A=attrname, S=self.splits_semicolon)
        for ntd in self.results:
            items.update(getattr(ntd, attrname))
        return items

    def _init_results(self):
        """Read a Reactome pathway analysis results file. Store in a Python var"""
        with open(self.fin_csv) as ifstrm:
            nts = []
            ntobj = None
            for flds in csv.reader(ifstrm):
                try:
                    if self.hdrs:
                        dct = self._get_dict_flds(flds)
                        # pylint: disable=not-callable
                        nts.append(ntobj(**dct))
                    else:
                        self.hdrs = self._nthdrs(flds)
                        ntobj = cx.namedtuple("ntpw", " ".join(self.hdrs))
                except RuntimeError as inst:
                    import traceback
                    traceback.print_exc()
                    sys.stderr.write("\n  **FATAL: {MSG}\n\n".format(MSG=str(inst)))
                    sys.stderr.write("**FATAL: {F}".format(F=flds))
                    sys.exit(1)
                except ValueError as inst:
                    import traceback
                    traceback.print_exc()
                    sys.stderr.write("\n  **FATAL: {MSG}\n\n".format(FIN=self.fin_csv, MSG=str(inst)))
                    sys.stderr.write("**FATAL: {FIN}: {F}".format(FIN=self.fin_csv, F=flds))
                    sys.exit(1)
            # pylint: disable=superfluous-parens
            print("  {N:6,} results READ: {CSV}".format(N=len(nts), CSV=self.fin_csv))
            return nts

    def _get_dict_flds(self, vals):
        """Get data from a row of csv format, return in a Python dict.

           NOTE: These:
               * Entities_ratio
               * Reactions_ratio
           indicates how big the pathway is, compared to the number of entities in the species.

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
        # print('VVVVV', vals)
        assert len(self.hdrs) == len(vals), "{} {}".format(len(hdrs), len(vals))
        dct = {k:self._get_val(k, v) for k, v in zip(self.hdrs, vals)}
        # print('DDDDD', dct)
        # for i, (k, v) in enumerate(dct.items()):
        #     print("{I:2}) KEY-VAL: {K:20} {V}".format(I=i, K=k, V=v))
        #### assert len(dct['Mapped_entities']) == len(dct['Submitted_entities_found'])
        return dct

    def _get_val(self, key, val):
        """Given string value, return value with correct type."""
        if key in self.floats:
            return float(val)
        if key[:4] == 'num_' or key == 'Species_identifier':
            return int(val)
        if key in self.splits_semicolon:
            values = val.split(';') if val != "" else []
            if values and next(iter(values)).isdigit():
                return [int(v) for v in values]
            return values
        return val

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

# Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
