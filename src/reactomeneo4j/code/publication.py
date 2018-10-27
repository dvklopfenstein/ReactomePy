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
    SUMS = 'reactomeneo4j.data.{ABC}.pathways.summation'
    PMDS = 'reactomeneo4j.data.{ABC}.pathways.pubmeds'

    def __init__(self, abc):
        self.abc = abc
        self.pw2nt = {nt.stId:nt for nt in import_module(self.PWYS.format(ABC=abc)).PWYNTS}
        self.pw2sum = import_module(self.SUMS.format(ABC=abc)).PW2SUMS
        self.pmid2nt = import_module(self.PMDS.format(ABC=abc)).PMID2NT
        self.pubs = self._init_literaturereference()
        self.books = self._init_books()
        self.urls = self._init_urls()

    def _init_literaturereference(self):
        pass

    def _init_books(self):
        pass

    def _init_urls(self):
        pass

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
