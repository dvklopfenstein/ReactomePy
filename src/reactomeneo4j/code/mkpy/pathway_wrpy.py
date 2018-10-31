"""Read pathways from neo4j and write to Python."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import collections as cx
# import timeit
# import datetime
# import textwrap
from datetime import date
from reactomeneo4j.data.species import SPECIES
from reactomeneo4j.code.mkpy.utils import REPO
from reactomeneo4j.code.mkpy.utils import prt_docstr_module
# from reactomeneo4j.code.mkpy.utils import prt_namedtuple
# from reactomeneo4j.code.mkpy.utils import prt_dict
from reactomeneo4j.code.mkpy.utils import prt_copyright_comment


class PathwayWrPy(object):
    """Write pathway information obtained from PythonQuery into Python modules."""

    taxid2nt = {nt.taxId:nt for nt in SPECIES}

# stId
# displayName
# speciesName
# releaseDate
# schemaClass
# isInDisease
# hasDiagram
# isInferred
# stIdVersion
# dbId
# name
    figerr = '{stId:13} dia={hasDiagram:1} {diagramHeight:>4}x{diagramWidth:<4} {displayName}'

    def __init__(self, pw2info, log=sys.stdout):
        self.log = log
        # abc='hsa', abbreviation taxId displayName
        self.taxnt = self._init_taxnt(pw2info)
        print(self.taxnt)
        self.pw2info = cx.OrderedDict(sorted(pw2info.items(), key=self._sortby))
        self.pubs = self._init_pubs()
        # assert species in self.name2nt, "SPECIES({S}) NOT FOUND IN:\n{A}\n".format(
        #     S=species, A="\n".join(sorted(self.name2nt)))
        # self.species = species
        # self.reltype2fnc = {
        #     'inferredTo': self._get_inferredto,
        #     'summation': self._get_summation,
        #     # Pubs, Books, URLs
        #     'literatureReference': self._load_literatureref,
        #     'species': self._get_taxid,
        #     'crossReference': self._get_crossreference,
        #     'disease': self._get_disease,
        #     'hasEncapsulatedEvent': self._get_hasencapsulatedevent,
        #     'normalPathway': self._get_normalpathway,
        #     'figure': self._get_figure,
        #     'relatedSpecies': self._get_relatedspecies,
        #     # 'hasEvent': self._get_event,
        # }

    @staticmethod
    def wrpy_version(fout_py, version):
        """Write Reactome version to a Python module."""
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt_docstr_module('Reactome version', prt)
            prt.write('VERSION = {V}\n'.format(V=version))
            prt_copyright_comment(prt)
            print("  WROTE: {PY}".format(PY=fout_py))

    def wrpy_pwy2pmids(self, fout_py):
        """Write Publications(LiteratureReference, Book, URL) into a Python module."""
        pw2pmids = self.pubs['pw2pubs']
        with open(fout_py, 'w') as prt:
            # prt = sys.stdout
            prt_docstr_module('PubMed IDs for each Pathway', prt)
            prt.write('\n# {N} of {M} Pathways are associated with PubMed IDs\n'.format(
                N=len(pw2pmids), M=len(self.pw2info)))
            prt.write('# pylint: disable=line-too-long,too-many-lines,bad-continuation\n')
            prt.write('PWY2PMIDS = {\n')
            for pwy, pmid_nts in sorted(pw2pmids.items(), key=self._sortby):
                pmids = sorted(set(pmid for pmid, _ in pmid_nts))
                prt.write("    '{PW}' : {{{PMIDS}}},\n".format(
                    PW=pwy, PMIDS=", ".join(str(i) for i in pmids)))
            prt.write('}\n\n')
            prt_copyright_comment(prt)
            print("  WROTE: {TXT}".format(TXT=fout_py))

    def wrpy_pubmeds(self, fout_py):
        """Write Publications(LiteratureReference, Book, URL) into a Python module."""
        pmid2nt = self._get_pmid2nt()
        keys = ' '.join(next(iter(pmid2nt.values()))._fields)
        with open(fout_py, 'w') as prt:
            prt.write('# coding=utf-8\n')
            # prt = sys.stdout
            prt_docstr_module('Publications including Pubmed papers, Books, and URLs', prt)
            prt.write('from collections import namedtuple\n')
            prt.write('\n# {N} PubMed IDs assc. w/{M} Pathways\n'.format(
                N=len(pmid2nt), M=len(self.pubs['pw2pubs'])))
            prt.write("Ntlit = namedtuple('ntlit', '{KEYS}')\n".format(KEYS=keys))
            prt.write('# pylint: disable=line-too-long,too-many-lines,bad-continuation\n')
            prt.write('PMID2NT = {\n')
            for pmid, ntd in sorted(pmid2nt.items(), key=lambda t: [t[1].year, t[0]]):
                prt.write('    {PMID:>8} : Ntlit._make({VALS}),\n'.format(
                    PMID=pmid, VALS=list(ntd)))
            prt.write('}\n\n')
            prt_copyright_comment(prt)
            print("  WROTE: {TXT}".format(TXT=fout_py))

    def _get_pmid2nt(self):
        """Get the PMIDs referenced in the Pathways."""
        pmid2nt = {}
        for pmid_nt in self.pubs['pw2pubs'].values():
            for pmid, ntd in pmid_nt:
                if pmid not in pmid2nt:
                    pmid2nt[pmid] = ntd
                else:
                    assert pmid2nt[pmid].displayName == ntd.displayName
        return pmid2nt

    def _init_pubs(self):
        """Get Publications(LiteratureReference, Book, URL) into a Python module."""
        pw2pubs = {}
        pw2lits = {}
        pw2books = {}
        pw2urls = {}
        # pylint: disable=line-too-long
        for pwy, dct in self.pw2info.items():
            if 'LiteratureReference' in dct:
                pw2pubs[pwy] = [a[1] for a in sorted(dct['LiteratureReference'], key=lambda a: a[0])]
            elif 'LiteratureReferenceNoPubMed' in dct:
                pw2lits[pwy] = [a[1] for a in sorted(dct['LiteratureReferenceNoPubMed'], key=lambda a: a[0])]
            elif 'Book' in dct:
                pw2books[pwy] = [a[1] for a in sorted(dct['Book'], key=lambda a: a[0])]
            elif 'URL' in dct:
                pw2urls[pwy] = [a[1] for a in sorted(dct['URL'], key=lambda a: a[0])]
        return {'pw2pubs':pw2pubs, 'pw2books':pw2books, 'pw2urls':pw2urls}

    def wrpy_pwy2nt(self, fout_py):
        """Write all pathways into a Python module in a condensed format."""
        pwy2nt = self.get_pwy2nt()
        keys = ' '.join(next(iter(pwy2nt.values()))._fields)
        with open(fout_py, 'w') as prt:
            prt.write('# coding=utf-8\n')
            prt_docstr_module('Pathway information', prt)
            prt.write('from collections import namedtuple\n')
            prt.write('from datetime import date\n')
            prt.write("\nNto = namedtuple('ntpwy', '{KEYS}')\n".format(KEYS=keys))
            prt.write('# {N} {SPECIES} Pathways\n'.format(
                N=len(pwy2nt), SPECIES=self.taxnt.displayName))
            prt.write('# pylint: disable=line-too-long,too-many-lines\n')
            prt.write('PWYNTS = [\n')
            for dct in pwy2nt.values():
                ntstr = '{}'.format(list(dct)).replace('datetime.date', 'date')
                prt.write('    Nto._make({VALS}),\n'.format(VALS=ntstr))
            prt.write(']\n')
            prt_copyright_comment(prt)
            print("  {N:5} pathways WROTE: {TXT}".format(N=len(self.pw2info), TXT=fout_py))

    def get_pwy2nt(self):
        """Write all pathways into a Python module in a condensed format."""
        pwy_nt = []
        ntobj = cx.namedtuple("ntpwy", "stId releaseDate marks NS displayName")
        for pwy, dct in self.pw2info.items():
            pwydct = dct['Pathway']
            date_ints = [int(i) for i in pwydct['releaseDate'].split('-')]
            ntd = ntobj(
                stId=pwydct['stId'],
                releaseDate=date(*date_ints),
                marks=self._get_pwmarkstr(dct),
                NS=self._get_namespace(dct),
                displayName=pwydct['displayName'])
            pwy_nt.append((pwy, ntd))
        return cx.OrderedDict(pwy_nt)

    def wrpwys(self, fout_txt):
        """Write all pathways into a text file in a condensed format."""
        with open(fout_txt, 'w') as prt:
            # prt = sys.stdout
            for dct in self.pw2info.values():
                prt.write('{PWY}\n'.format(PWY=self.pwstr(dct)))
            print("  {N:5} pathways WROTE: {TXT}".format(N=len(self.pw2info), TXT=fout_txt))

    def _get_pwmarkstr(self, dct):
        """Get a string representing Pathway information markers."""
        pwy = dct['Pathway']
        return "".join([
            'T' if pwy['schemaClass'] == 'TopLevelPathway' else '.',
            'D' if pwy['isInDisease'] else '.',
            self._get_fig_mark(dct),
            'I' if pwy['isInferred'] else '.',
            'P' if 'LiteratureReference' in dct else '.',
            'B' if 'Book' in dct else '.',
            'U' if 'URL' in dct else '.',
        ])

    @staticmethod
    def _get_namespace(dct):
        """Return Gene Ontology namespace markers."""
        return "".join([
            'B' if 'GO_BiologicalProcess' in dct else '.',  # Biological Process
            'C' if 'Compartment' in dct else '.',           # Cellular Compartment
        ])

    @staticmethod
    def _get_fig_mark(dct):
        """Get a mark showing the presence of a Diagram and a filename."""
        if dct['Pathway']['hasDiagram']:
            return 'F' if 'Figure' in dct else 'f'
        return '.'

    def wrtxt(self, fout_pat):
        """Write pathway information into Python modules."""
        fout_txt = fout_pat.format(ABC=self.taxnt.abc)
        with open(fout_txt, 'w') as prt:
            self.prttxt(prt)
            print("  {N:5} pathways WROTE: {TXT}".format(N=len(self.pw2info), TXT=fout_txt))

    def prttxt(self, prt=sys.stdout):
        """Write pathway information into Python modules."""
        for pwy, rel2dct in self.pw2info.items():
            prt.write("\n-----------------------------------------------------------\n")
            prt.write("PATHWAY: {PW} {NAME}\n".format(
                PW=pwy, NAME=rel2dct['Pathway']['displayName']))
            # prt.write("DICTS:", dcts)
            for rel, val in rel2dct.items():
                if rel == 'Pathway':
                    val = {k:v for k, v in val.items() if k not in set(['hasDiagram', 'diagramWidth', 'diagramHeight'])} # DVK:RM
                    prt.write("{VAL}\n".format(VAL=val))  # dict
                # else:  # DVK:UNC
                elif rel not in set(['summation', 'figure']): # DVK:RM
                    for item in val:  # list
                        prt.write('{REL:20} {ITEM}\n'.format(REL=rel, ITEM=item))
                # prt.write(rel, val)
                #for elem in dct:
                #    prt.write(elem)

    def wrpy_pwy2summation(self, fpat_py):
        """Write pathway summation to a Python file."""
        fout_py = fpat_py.format(ABC=self.taxnt.abc)
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt.write('# coding=utf-8\n')
            prt_docstr_module('Summations for pathways', prt)
            prt.write('# pylint: disable=line-too-long,too-many-lines\n')
            prt.write("PW2SUMS = {\n")
            for pwy, dct in self.pw2info.items():
                prt.write("    '{KEY}': {VAL},\n".format(KEY=pwy, VAL=dct['summation']))
            prt.write("}\n")
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    # def wrpy_inferredto(self, fout_py):
    #     """Write inferredTo species for a pathway."""
    #     pw2abcs = self._get_inferredto()
    #     with open(os.path.join(REPO, fout_py), 'w') as prt:
    #         for pwy, abcs in pw2abcs.items():
    #             pass
    #         print('  WROTE: {PY}'.format(PY=fout_py))

    def wrpy_figure(self, fpat_py):
        """Write pathway summation to a Python file."""
        fout_py = fpat_py.format(ABC=self.taxnt.abc)
        pw2ntfig = self._get_ntfig()
        keys = ' '.join(next(iter(pw2ntfig.values()))._fields)
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt_docstr_module('{N} of {T} Pathway have figures'.format(
                N=len(pw2ntfig), T=len(self.pw2info)), prt)
            prt.write('from collections import namedtuple\n')
            prt.write("Ntfig = namedtuple('ntfig', '{KEYS}')\n".format(KEYS=keys))
            prt.write("PW2FIGS = {\n")
            for pwy, ntfig in sorted(pw2ntfig.items(), key=self._sortby):
                prt.write("    '{PWY}' : Ntfig._make({VALS}),\n".format(PWY=pwy, VALS=list(ntfig)))
            prt.write("}\n")
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    def _get_inferredto(self):
        """Get inferredTo species for a pathway."""
        pw2abcs = {}
        for pwy, dct in self.pw2info.items():
            if 'inferredTo' in dct:
                # pwnum = pwy.split('-')[2]
                ids = set(p.split('-')[2] for p in dct['inferredTo'])
                if len(ids) != 1:
                    self.log.write('**INFO-inferredTo MULTI: {PW}'.format(PW=self.pwstr(dct)))
            else:
                self.log.write('**INFO-inferredTo NONE: {PW}\n'.format(PW=self.pwstr(dct)))
        return pw2abcs

    def pwstr(self, dct):
        """Get Pathway string."""
        pwy = dct['Pathway']
        return '{PW:13} {DATE} {MARKS} {NAME}'.format(
            PW=pwy['stId'],
            MARKS=self._get_pwmarkstr(dct),
            DATE=pwy['releaseDate'],
            NAME=pwy['displayName'])

    def _get_ntfig(self):
        """Get pathways and their figure information."""
        pw2ntfig = {}
        ntobj = cx.namedtuple('ntfig', 'width height filename')
        cnt = 0
        for pwy, dct in self.pw2info.items():
            pwdct = dct['Pathway']
            if 'diagramHeight' in pwdct:
                if 'figure' in dct:
                    ntd = ntobj(width=pwdct['diagramWidth'],
                                height=pwdct['diagramHeight'],
                                filename=dct['figure'])
                    pw2ntfig[pwy] = ntd
                else:
                    self.log.write('**ERROR: NO FIGURE FOUND: {PW}\n'.format(
                        PW=self.figerr.format(**pwdct)))
                    cnt += 1
            else:
                self.log.write('**INFO: NO FIGURE EXPECTED: {PW} {NAME}\n'.format(
                    PW=pwy, NAME=dct['Pathway']['displayName']))
        self.log.write('{Y} Figures found. {N} Figures missing.\n'.format(
            Y=len(pw2ntfig), N=cnt))
        return pw2ntfig

    def _sortby(self, key_val):
        """Sort by Pathway number."""
        vals = key_val[0].split('-')
        assert len(vals) == 3
        assert vals[0] == 'R'
        assert vals[1] == self.taxnt.abc.upper(), "{} {} {}".format(
            vals[1], self.taxnt.abc, key_val)
        return int(vals[2])

    def _init_taxnt(self, pw2info):
        """Get the taxid for this set of pathways."""
        taxids = next(iter(pw2info.values()))['taxId']
        assert len(taxids) == 1
        return self.taxid2nt[taxids[0]]


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reservedsEvent
