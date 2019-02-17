"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from reactomeneo4j.code.enrich.pvalcalc import FisherFactory
from reactomeneo4j.code.enrich.multiple_testing import Methods

class Enrichment():
    """Enrichment object."""

    def __init__(self, population_ids, associations, alpha=.05, methods=None):
        self.pop_ids = population_ids
        self.assc = associations
        self.pval_obj = FisherFactory().pval_obj
        if methods is None:
            methods = ['fdr_bh']
        self.methods = Methods(methods)

    def run_study(self, study_ids):
        """Run an enrichment."""
        results = []
        return results


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
