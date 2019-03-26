"""Enrichment object."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
from reactomepy.code.enrich.enrich_base import Enrichment
from reactomepy.data.pwy.stid2pwy import STID2NTPWY


class PathwayEnrichment():
    """Enrichment object."""

    def __init__(self, population_ids, associations, alpha=.05, methods=None):
        self.pop_ids = population_ids
        self.assc = associations
        self.enrich = Enrichment(population_ids, associations, alpha, methods)

    def run_study(self, study_ids):
        """Run an enrichment."""
        return self.enrich.run_study(study_ids)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
