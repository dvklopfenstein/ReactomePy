#!/usr/bin/env python
"""Test command-line-interface for pwy_enrichment_reactome.py"""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomepy.code.rest.service_analysis import AnalysisService
#from enrichmentanalysis.file_utils import get_kws_analyse
from enrichmentanalysis.file_utils import get_fout_pdf


# pylint: disable=bad-whitespace,line-too-long
def test_args():
    """Test command-line-interface for pwy_enrichment_reactome.py"""
    test_ea_params()
    test_pdf()

def test_pdf():
    """Test getting pdf file."""
    assert get_fout_pdf({'csv':'pathway_enrichment.csv', 'pdf':True}) == 'pathway_enrichment.pdf'
    assert get_fout_pdf({'csv':'pathway_enrichment.csv', 'pdfname':'test.pdf'}) == 'test.pdf'
    assert get_fout_pdf({'csv':'pathway_enrichment.csv', 'pdf':True, 'pdfname':'test.pdf'}) == 'test.pdf'

def test_ea_params():
    """Test parameters for /identifiers/form and /identifiers/form/projection"""
    stim_list = [
        {                    'includeDisease':False},
        {                                          },
        {'interactors':True, 'includeDisease':False},
        {'interactors':True,                       }]

    exp_list = [
        {'interactors':False, 'includeDisease':False},
        {'interactors':False, 'includeDisease':True},
        {'interactors':True,  'includeDisease':False},
        {'interactors':True,  'includeDisease':True}]

    for idx, (kws, exp) in enumerate(zip(stim_list, exp_list)):
        act_all = AnalysisService.get_params_ea(kws)
        act_cur = {k:act_all[k]=='true' for k in {'interactors', 'includeDisease'}}
        assert act_cur == exp, '{I}) ACT({A}) != EXP({E}):  {X}'.format(I=idx, A=act_cur, E=exp, X=kws)


if __name__ == '__main__':
    test_args()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
