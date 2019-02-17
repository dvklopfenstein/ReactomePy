"""Multiple test correction."""

import sys
import random
import numpy as np
import collections as cx
from statsmodels.sandbox.stats.multicomp import multipletests

__copyright__ = "Copyright (C) 2015-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

class Methods(object):
    """Class to manage multipletest methods from both local and remote sources."""

    # https://github.com/statsmodels/statsmodels/blob/master/statsmodels/stats/multitest.py
    all_methods = [
        ("statsmodels", (
            'bonferroni',     #  0) Bonferroni one-step correction
            'sidak',          #  1) Sidak one-step correction
            'holm-sidak',     #  2) Holm-Sidak step-down method using Sidak adjustments
            'holm',           #  3) Holm step-down method using Bonferroni adjustments
            'simes-hochberg', #  4) Simes-Hochberg step-up method  (independent)
            'hommel',         #  5) Hommel closed method based on Simes tests (non-negative)
            'fdr_bh',         #  6) FDR Benjamini/Hochberg  (non-negative)
            'fdr_by',         #  7) FDR Benjamini/Yekutieli (negative)
            'fdr_tsbh',       #  8) FDR 2-stage Benjamini-Hochberg (non-negative)
            'fdr_tsbky',      #  9) FDR 2-stage Benjamini-Krieger-Yekutieli (non-negative)
            'fdr_gbs',        # 10) FDR adaptive Gavrilov-Benjamini-Sarkar
            )),

    ]
    prefixes = {'statsmodels':'sm_'}
    NtMethodInfo = cx.namedtuple("NtMethodInfo", "source method fieldname")

    def __init__(self, usr_methods=None):
        self._srcmethod2fieldname = self._init_srcmethod2fieldname()
        self.statsmodels_multicomp = None
        if usr_methods is None:
            usr_methods = ['fdr_bh']
        self._init_methods(usr_methods)

    def _init_methods(self, usr_methods):
        """From the methods list, set list of methods to be used during GOEA."""
        self.methods = []
        for usr_method in usr_methods:
            self._add_method(usr_method)

    def _add_method(self, method, method_source=None):
        """Determine method source if needed. Add method to list."""
        try:
            if method_source is not None:
                self._add_method_src(method_source, method)
            else:
                self._add_method_nosrc(method)
        except Exception as inst:
            raise Exception("{ERRMSG}".format(ERRMSG=inst))

    def _add_method_nosrc(self, usr_method):
        """Add method source, method, and fieldname to list of methods."""
        for method_source, available_methods in self.all_methods:
            if usr_method in available_methods:
                fieldname = self.get_fldnm_method(usr_method)
                nmtup = self.NtMethodInfo(method_source, usr_method, fieldname)
                self.methods.append(nmtup)
                return
        for src, prefix in self.prefixes.items():
            if usr_method.startswith(prefix):
                method_source = src
                method = usr_method[len(prefix):]
                nmtup = self.NtMethodInfo(method_source, method, usr_method)
                self.methods.append(nmtup)
                return
        raise self.rpt_invalid_method(usr_method)

    def getmsg_valid_methods(self):
        """Return a string containing valid method names."""
        msg = []
        msg.append("    Available methods:")
        for method_source, methods in self.all_methods:
            msg.append("        {SRC}(".format(SRC=method_source))
            for method in methods:
                attrname = self._srcmethod2fieldname[(method_source, method)]
                msg.append("            {ATTR}".format(ATTR=attrname))
            msg.append("        )")
        return "\n".join(msg)

    def get_fieldname(self, method_source, method):
        """Get the name of the method used to create namedtuple fieldnames which store floats."""
        return self._srcmethod2fieldname[(method_source, method)]

    def _init_srcmethod2fieldname(self):
        """Return an OrderedDict with key, (method_src, method), and value, attrname."""
        srcmethod_fieldname = []
        ctr = self._get_method_cnts()
        for method_source, methods in self.all_methods:
            for method in methods:
                prefix = self.prefixes.get(method_source, "")
                prefix = prefix if ctr[method] != 1 else ""
                fieldname = "{P}{M}".format(P=prefix, M=method.replace('-', '_'))
                srcmethod_fieldname.append(((method_source, method), fieldname))
        return cx.OrderedDict(srcmethod_fieldname)

    def rpt_invalid_method(self, usr_method):
        """Report which methods are available."""
        msgerr = "FATAL: UNRECOGNIZED METHOD({M})".format(M=usr_method)
        msg = [msgerr, self.getmsg_valid_methods(), msgerr]
        raise Exception("\n".join(msg))

    def _get_method_cnts(self):
        """Count the number of times a method is seen."""
        ctr = cx.Counter()
        for source_methods in self.all_methods:
            for method in source_methods[1]:
                ctr[method] += 1
        return ctr

    def _add_method_src(self, method_source, usr_method, fieldname=None):
        """Add method source and method to list of methods."""
        fieldname = self._srcmethod2fieldname.get((method_source, usr_method), None)
        if fieldname is not None:
            nmtup = self.NtMethodInfo(method_source, usr_method, fieldname)
            self.methods.append(nmtup)
        else: raise Exception("ERROR: FIELD({FN}) METHOD_SOURCE({MS}) AND METHOD({M})".format(
            FN=fieldname, MS=method_source, M=usr_method))

    @staticmethod
    def get_fldnm_method(method):
        """Given method and source, return fieldname for method."""
        fieldname = method.replace('-', '_')
        return fieldname

    def get_statsmodels_multipletests(self):
        """Only load statsmodels package if it is used."""
        if self.statsmodels_multicomp is not None:
            return self.statsmodels_multicomp
        self.statsmodels_multicomp = multipletests
        return self.statsmodels_multicomp

    def __iter__(self):
        return iter(self.methods)


# Copyright (C) 2015-2019, DV Klopfenstein. All rights reserved.
