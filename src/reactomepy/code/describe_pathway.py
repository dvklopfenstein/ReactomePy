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
import pkgutil
import textwrap
from reactomepy.code.species import Species
from reactomepy.data.disease_definitions import DISEASE2DEFN


class DescribePathway(object):
    """Manages Publications: Research papers, books, and URLs."""

    objspecies = Species()
    sep = '\n-------------------------------------------------------------------\n'

    def __init__(self, abc, gosubdag=None, linewidth=80):
        self.abc = abc
        self.gosubdag = gosubdag
        self.mdir = 'reactomepy.data.{ABC}.pathways.'.format(ABC=abc)
        self.linewidth = linewidth
        self.pw2nt = {nt.stId:nt for nt in import_module(self.mdir+"pathways").PWYNTS}
        self.pw2sum = import_module(self.mdir+"pwy2summation").PW2SUMS
        self.pw2dis = import_module(self.mdir+"pwy2disease").PWY2DIS
        self.pw2pmids = import_module(self.mdir+"pwy2pmids").PWY2PMIDS
        self.pmid2nt = import_module(self.mdir+"pmid2nt").PMID2NT
        self.pmid2info = self._init_pmid2info()
        self.mh2ms = self._init_mh2ms()
        # self.books = self._init_books()  # TBD
        # self.urls = self._init_urls()    # TBD
        self.pw2relatedtaxids = import_module(self.mdir+"pwy2relatedspecies").PWY2TAXIDS
        # Gene Ontology
        self.pw2go = {
            'bp' : import_module(self.mdir+"pwy2bp").PWY2GOS,
            'cc' : import_module(self.mdir+"pwy2cc").PWY2GOS}

    def _init_mh2ms(self):
        """MeSH-to-namedtuple: UI MS."""
        if self.pmid2info is not None:
          modstr = 'dvkbiodnld.data.mesh.descriptors'
          if pkgutil.find_loader(modstr) is not None:
              return {nt.MH:nt.MS for nt in import_module(modstr).UI2NT.values()}

    def prt_pw(self, pwy_stid, prt=sys.stdout):
        """Print Pathway information."""
        prt.write(self.sep.replace('-', '='))
        prt.write('PATHWAY: {stId} {releaseDate} {marks} {displayName}\n'.format(
            **(self.pw2nt[pwy_stid])._asdict()))
        self._prt_summary(pwy_stid, prt)
        self._prt_diseases(pwy_stid, prt)
        self._prt_gos('bp', pwy_stid, prt)
        self._prt_gos('cc', pwy_stid, prt)
        self._prt_pmids(pwy_stid, prt)
        self._prt_species(pwy_stid, prt)

    def _prt_summary(self, pwy_stid, prt=sys.stdout):
        """Print Pathway Summary."""
        for summary in self.pw2sum[pwy_stid]:
            prt.write('SUMMARY: {TXT}\n'.format(TXT=('\n'.join(textwrap.wrap(summary, self.linewidth)))))

    def _prt_diseases(self, pwy_stid, prt):
        """Print diseases, if any, associated with this pathway."""
        if pwy_stid in self.pw2dis:
            for dis in self.pw2dis[pwy_stid]:
                prt.write('DISEASE({DIS})'.format(DIS=dis))
                if dis in DISEASE2DEFN:
                    prt.write(': {DESC}'.format(DESC=DISEASE2DEFN[dis]))
                prt.write('\n') 

    def _prt_gos(self, nsname, pwy_stid, prt):
        """Print GO information."""
        pw2go = self.pw2go[nsname]
        if pwy_stid in pw2go:
            goids = pw2go[pwy_stid]
            if self.gosubdag:
                self._prt_goids(prt, goids)
            else:
                for goid in goids:
                    prt.write('{GO}\n'.format(GO=goid))

    def _prt_pmids(self, pwy_stid, prt=sys.stdout):
        """Print Pathway PubMed IDs and titles."""
        if pwy_stid in self.pw2pmids:
            pwy_pmid = [(p, self.pmid2nt[p]) for p in self.pw2pmids[pwy_stid]]
            pmid_nt = sorted(pwy_pmid, key=lambda t: -1*t[1].year)
            prt.write('{SEP}{N} Publications in PubMed for {PWY}({DESC}):\n'.format(
                SEP=self.sep, N=len(pmid_nt), PWY=pwy_stid, DESC=self.pw2nt[pwy_stid].displayName))
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
               desc = mhstr.split('/')[0]
               if desc:
                   msstr = self.mh2ms.get(desc)
                   if msstr:
                       prt.write('      {MS}\n'.format(MS=msstr))

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
        modstr = 'reactomepy.work.{ABC}_pwy_pmid2info'.format(ABC=self.abc)
        if pkgutil.find_loader(modstr) is not None:
            return import_module(modstr).pmid2info

    def _prt_goids(self, prt, goids, sortby=None):
        """Print GO IDs."""
        nts = self.gosubdag.get_nts(goids, sortby)
        prtfmt = self.gosubdag.prt_attr['fmta']
        for ntgo in nts:
            key2val = ntgo._asdict()
            prt.write("{GO}\n".format(GO=prtfmt.format(**key2val)))
            goterm = self.gosubdag.go2obj[ntgo.GO]
            if hasattr(goterm , 'defn'):
                prt.write("{DEFN}\n\n".format(DEFN=goterm.defn))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
