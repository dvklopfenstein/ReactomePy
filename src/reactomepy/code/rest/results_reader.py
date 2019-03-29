"""Read a Reactome pathway analysis results file. Store in a Python var"""

__copyright__ = "Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
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
    splits_semicolon = set([
        'Submitted_entities_found',
        'Mapped_entities',
        'Found_reaction_identifiers'])

    def __init__(self, fin_csv):
        self.fin_csv = fin_csv
        self.hdrs = None
        self.results = self._init_results()
        assert self.hdrs is not None, "NO HEADERS READ: {CSV}".format(CSV=fin_csv)

    def compare(self, obj_exp):
        """Compare namedtuples."""
        stid2nt_act = {nt.Pathway_identifier:nt for nt in self.results}
        stid2nt_exp = {nt.Pathway_identifier:nt for nt in obj_exp.results}
        act_only = []
        errors = []
        for stid, ntact in stid2nt_act.items():
            if stid in stid2nt_exp:
                ntexp = stid2nt_exp[stid]
                self._chk_result_nt(errors, ntact, ntexp)
                self._chk_reactions_ratio(errors, ntact, 'ACT')
                self._chk_reactions_ratio(errors, ntexp, 'EXP')
                self._chk_entities_ratio(errors, ntact, 'ACT')
                self._chk_entities_ratio(errors, ntexp, 'EXP')
            else:
                act_only.append(stid)
        exp_only = set(stid2nt_exp).difference(stid2nt_act)
        self._chk_results_only(errors, act_only, exp_only)
        self._chk_results_none(self.results, obj_exp.results)
        if errors:
            self._wrerrs(errors)
            assert False, '{N} ERRORS IN RESULTS'.format(N=len(errors))

    def _wrerrs(self, errors):
        """Write errors to a log file."""
        base = os.path.splitext(os.path.basename(self.fin_csv))[0]
        fout_log = "{BASE}.errors".format(BASE=base)
        with open(fout_log, 'w') as prt:
            for err in sorted(errors):
                prt.write('{ERR}\n'.format(ERR=err))
        print('  {N} Errors WROTE: {TXT}'.format(N=len(errors), TXT=fout_log))

    @staticmethod
    def _chk_entities_ratio(errors, ntd, desc):
        """Check that the ratio matches the calculated ratio for reactions."""
        pat = ('PATHWAY {P:13} {DESC} ENTITY   RATIO MISMATCH: '
               'NT({NT:7.5f}) != CALC({C:7.5f}) = {N}/{T}')
        ratio_calc = float(ntd.num_Entities_found)/ntd.num_Entities_total
        if abs(ratio_calc - ntd.Entities_ratio) > .001:
            errors.append(pat.format(
                DESC=desc, P=ntd.Pathway_identifier, NT=ntd.Entities_ratio,
                C=ratio_calc, N=ntd.num_Entities_found, T=ntd.num_Entities_total))

    @staticmethod
    def _chk_reactions_ratio(errors, ntd, desc):
        """Check that the ratio matches the calculated ratio for reactions."""
        pat = ('PATHWAY {P:13} {DESC} REACTION RATIO MISMATCH: '
               'NT({NT:7.5f}) != CALC({C:7.5f}) = {N}/{T}')
        ratio_calc = float(ntd.num_Reactions_found)/ntd.num_Reactions_total
        if abs(ratio_calc - ntd.Reactions_ratio) > .001:
            errors.append(pat.format(
                DESC=desc, P=ntd.Pathway_identifier, NT=ntd.Reactions_ratio,
                C=ratio_calc, N=ntd.num_Reactions_found, T=ntd.num_Reactions_total))

    def _chk_result_nt(self, errors, nt_act, nt_exp):
        """Check if the actual and expected namedtuple values match"""
        assert nt_act.Pathway_identifier is not None
        assert nt_exp.Pathway_identifier is not None
        pat = 'PATHWAY {P:13} MISMATCH ON {FLD}: ACT({A}) != EXP({E})'
        if nt_act == nt_exp:
            return
        for fld, val_act, val_exp in zip(self.hdrs, list(nt_act), list(nt_exp)):
            if fld in self.chk_flds:
                if val_act != val_exp:
                    msg = pat.format(P=nt_act.Pathway_identifier, FLD=fld, A=val_act, E=val_exp)
                    errors.append(msg)

    @staticmethod
    def _chk_results_none(nts_act, nts_exp):
        """Check if any pathway IDs are None in the actual or expected results."""
        bad_act = [nt for nt in nts_act if nt.Pathway_identifier is None]
        bad_exp = [nt for nt in nts_exp if nt.Pathway_identifier is None]
        assert not bad_act or not bad_exp, 'PATHWAY IDs ARE NONE: {A} ACTUAL, {E} EXPECTED'.format(
            A=len(bad_act), E=len(bad_exp))

    @staticmethod
    def _chk_results_only(errors, act_only, exp_only):
        """Check if any results were found in only the actual or expected results."""
        if act_only:
            print('{N} PATHWAYS FOUND IN ACTUAL RESULTS ONLY'.format(N=len(act_only)))
            for stid in act_only:
                errors.append('PATHWAY {P:13} IN ACTUAL ONLY'.format(P=stid))
        if exp_only:
            print('{N} PATHWAYS FOUND IN EXPECTED RESULTS ONLY'.format(N=len(exp_only)))
            for stid in exp_only:
                errors.append('PATHWAY {P:13} IN ACTUAL ONLY'.format(P=stid))


    def _init_results(self):
        """Read a Reactome pathway analysis results file. Store in a Python var"""
        with open(self.fin_csv) as ifstrm:
            nts = []
            ntobj = None
            for flds in csv.reader(ifstrm):
            ## for line in ifstrm:
                ## flds = line.split(',')
                ## flds[-1] = flds[-1].rstrip()
                if self.hdrs:
                    # print('FFFFF', flds)
                    dct = self._get_dict_flds(flds)
                    # pylint: disable=not-callable
                    nts.append(ntobj(**dct))
                else:
                    self.hdrs = self._nthdrs(flds)
                    ntobj = cx.namedtuple("ntpw", " ".join(self.hdrs))
                    # print('HHHHH', ' '.join(self.hdrs))
            # pylint: disable=superfluous-parens
            print("  {N:6,} results READ: {CSV}".format(N=len(nts), CSV=self.fin_csv))
            return nts

    def _get_dict_flds(self, vals):
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
            return val.split(';')
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
