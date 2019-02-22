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
        self.pop_n = len(population_ids)
        self.assc = associations
        self.pval_obj = FisherFactory().pval_obj
        if methods is None:
            methods = ['fdr_bh']
        self.methods = Methods(methods)

    def run_study(self, study_ids):
        """Run an enrichment."""
        results = []
        if not study_ids:
            return results
        results = self.get_pval_uncorr(study_ids, log)
        if not results:
            return []
        return results

    def get_pval_uncorr(self, study, log=sys.stdout):
        """Calculate the uncorrected pvalues for study items."""
        results = []
        study_in_pop = self.pop_ids.intersection(study)
        # " 99%    378 of    382 study items found in population"
        go2studyitems = get_terms("study", study_in_pop, self.assc, self.obo_dag, log)
        pop_n, study_n = self.pop_n, len(study_in_pop)
        allterms = set(go2studyitems).union(set(self.go2popitems))
        if log is not None:
            # Some study genes may not have been found in the population. Report from orig
            study_n_orig = len(study)
            perc = 100.0*study_n/study_n_orig if study_n_orig != 0 else 0.0
            log.write("{R:3.0f}% {N:>6,} of {M:>6,} study items found in population({P})\n".format(
                N=study_n, M=study_n_orig, P=pop_n, R=perc))
            if study_n:
                log.write("Calculating {N:,} uncorrected p-values using {PFNC}\n".format(
                    N=len(allterms), PFNC=self.pval_obj.name))
        # If no study genes were found in the population, return empty GOEA results
        if not study_n:
            return []
        calc_pvalue = self.pval_obj.calc_pvalue

        for goid in allterms:
            study_items = go2studyitems.get(goid, set())
            study_count = len(study_items)
            pop_items = self.go2popitems.get(goid, set())
            pop_count = len(pop_items)

            one_record = GOEnrichmentRecord(
                goid,
                p_uncorrected=calc_pvalue(study_count, study_n, pop_count, pop_n),
                study_items=study_items,
                pop_items=pop_items,
                ratio_in_study=(study_count, study_n),
                ratio_in_pop=(pop_count, pop_n))

            results.append(one_record)

        return results


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
