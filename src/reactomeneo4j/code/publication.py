"""Manages Publications: Research papers, books, and URLs."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# Data Schema for 'Publication'
#
# - Publication(dcnt=3)
# -- Book(dcnt=0)
# -- LiteratureReference(dcnt=0)
# -- URL (dcnt=0)

# import sys
from importlib import import_module

class Publication(object):
    """Manages Publications: Research papers, books, and URLs."""

    PWYS = 'reactomeneo4j.data.{ABC}.pathways.pathways'
    SUMS = 'reactomeneo4j.data.{ABC}.pathways.pwy2summation'
    PYPM = 'reactomeneo4j.data.{ABC}.pathways.pwy2pmids'
    PMDS = 'reactomeneo4j.data.{ABC}.pathways.pmid2nt'

    def __init__(self, abc):
        self.abc = abc
        self.pw2nt = {nt.stId:nt for nt in import_module(self.PWYS.format(ABC=abc)).PWYNTS}
        self.pw2sum = import_module(self.SUMS.format(ABC=abc)).PW2SUMS
        self.pw2pmids = import_module(self.PYPM.format(ABC=abc)).PWY2PMIDS
        self.pmid2nt = import_module(self.PMDS.format(ABC=abc)).PMID2NT
        # self.books = self._init_books()  # TBD
        # self.urls = self._init_urls()    # TBD

    def prt_pw(self, pwy_stid, prt=sys.stdout):
        """Print Pathway information."""
        prt.write('{NT}\n'.format(NT=self.pw2nt[pwy_stid]))

    def get_pwys_w_all(self):
        """Get a set of Pathways that contain all types of descriptions."""
        pwys = set()
        for pwy, ntpw in self.pw2nt.items():
            if pwy in self.pw2sum and pwy in self.pw2pmids:
                pwys.add(pwy)
        return pwys


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
