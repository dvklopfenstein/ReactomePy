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
from importlib import import_module
import textwrap
from reactomeneo4j.code.species import Species

class DescribePathway(object):
    """Manages Publications: Research papers, books, and URLs."""

    PWYS = 'reactomeneo4j.data.{ABC}.pathways.pathways'
    SUMS = 'reactomeneo4j.data.{ABC}.pathways.pwy2summation'
    PYPM = 'reactomeneo4j.data.{ABC}.pathways.pwy2pmids'
    PMDS = 'reactomeneo4j.data.{ABC}.pathways.pmid2nt'
    SPEC = 'reactomeneo4j.data.{ABC}.pathways.pwy2relatedspecies'

    objspecies = Species()
    sep = '\n-------------------------------------------------------------------\n'

    def __init__(self, abc, linewidth=80):
        self.abc = abc
        self.linewidth = linewidth
        self.pw2nt = {nt.stId:nt for nt in import_module(self.PWYS.format(ABC=abc)).PWYNTS}
        self.pw2sum = import_module(self.SUMS.format(ABC=abc)).PW2SUMS
        self.pw2pmids = import_module(self.PYPM.format(ABC=abc)).PWY2PMIDS
        self.pmid2nt = import_module(self.PMDS.format(ABC=abc)).PMID2NT
        self.pmid2info = self._init_pmid2info()
        # self.books = self._init_books()  # TBD
        # self.urls = self._init_urls()    # TBD
        self.pw2relatedtaxids = import_module(self.SPEC.format(ABC=abc)).PWY2TAXIDS

    def prt_pw(self, pwy_stid, prt=sys.stdout):
        """Print Pathway information."""
        prt.write(self.sep.replace('-', '='))
        prt.write('PATHWAY: {stId} {releaseDate} {marks} {displayName}\n'.format(
            **(self.pw2nt[pwy_stid])._asdict()))
        self._prt_summary(pwy_stid, prt)
        self._prt_pmids(pwy_stid, prt)
        self._prt_species(pwy_stid, prt)

    def _prt_summary(self, pwy_stid, prt=sys.stdout):
        """Print Pathway Summary."""
        for summary in self.pw2sum[pwy_stid]:
            prt.write('SUMMARY: {TXT}\n'.format(TXT=('\n'.join(textwrap.wrap(summary, self.linewidth)))))

    def _prt_pmids(self, pwy_stid, prt=sys.stdout):
        """Print Pathway PubMed IDs and titles."""
        if pwy_stid in self.pw2pmids:
            pwy_pmid = [(p, self.pmid2nt[p]) for p in self.pw2pmids[pwy_stid]]
            pmid_nt = sorted(pwy_pmid, key=lambda t: -1*t[1].year)
            prt.write('{SEP}{N} Publications in PubMed:\n'.format(SEP=self.sep, N=len(pmid_nt)))
            for idx, (pmid, ntpub) in enumerate(pmid_nt):
                prt.write('\n{I}) PMID: {year} {PMID:8} {journal}\n'.format(
                    I=idx, PMID=pmid, year=ntpub.year, journal=ntpub.journal))
                prt.write('TITLE: {displayName}\n'.format(displayName=ntpub.displayName))
                if self.pmid2info:
                    self._prt_pmid_info(pmid, prt)

    def _prt_pmid_info(self, pmid, prt):
        """Print PMID information."""
        fld2val = self.pmid2info[pmid]
        if 'AB' in fld2val:
             abstract = fld2val['AB']
             prt.write('ABSTRACT:\n')
             for line in abstract.strip().split('. '):
                 if line[-1] == '.':
                     line = line[:-1]
                 prt.write('{LINE}.\n'.format(LINE=line.strip()))
             prt.write('\n')
        if 'MH' in fld2val:
             for mhstr in fld2val['MH']:
               prt.write('MeSH: {MH}\n'.format(MH=mhstr))

    def _prt_species(self, pwy_stid, prt=sys.stdout):
        """Print speciesi that are related to this pathway."""
        if pwy_stid in self.pw2relatedtaxids:
            prt.write('{SEP}RELATED SPECIES:\n'.format(SEP=self.sep))
            self.objspecies.prt_taxids(self.pw2relatedtaxids[pwy_stid], prt)

    def get_pwys_w_all(self):
        """Get a set of Pathways that contain all types of descriptions."""
        pwys = set()
        for pwy in self.pw2nt:
            if pwy in self.pw2sum and pwy in self.pw2pmids:
                pwys.add(pwy)
        return pwys

    def _init_pmid2info(self):
        """Initialize PMID-to-Abstract if it is available."""
        modstr = 'reactomeneo4j.work.{ABC}_pwy_pmid2info'.format(ABC=self.abc)
        module = import_module(modstr)
        if module is None:
            return None
        return module.pmid2info
        


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
