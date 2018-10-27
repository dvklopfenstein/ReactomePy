"""Manages Publications: Research papers, books, and URLs."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# Data Schema for 'Publication'
#
# - Publication(dcnt=3)
# -- Book(dcnt=0)
# -- LiteratureReference(dcnt=0)
# -- URL (dcnt=0)

import sys

class Publication(object):
    """Manages Publications: Research papers, books, and URLs."""

    def __init__(self, abc):
        self.abc = abc
        self.pubs = self._init_literaturereference()
        self.books = self._init_books()
        self.urls = self._init_urls()

    def _init_literaturereference():
        pass

    def _init_books():
        pass

    def _init_urls():
        pass

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
