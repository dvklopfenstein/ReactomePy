"""Read pathways from neo4j and write to Python."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
# import collections as cx
# import timeit
# import datetime
# import textwrap
from reactomeneo4j.data.species import SPECIES
from reactomeneo4j.code.mkpy.utils import REPO
from reactomeneo4j.code.mkpy.utils import prt_docstr_module
# from reactomeneo4j.code.mkpy.utils import prt_namedtuple
from reactomeneo4j.code.mkpy.utils import prt_dict
from reactomeneo4j.code.mkpy.utils import prt_copyright_comment


class PathwayWrPy(object):
    """Write pathway information obtained from PythonQuery into Python modules."""

    taxid2nt = {nt.taxId:nt for nt in SPECIES}

    #### pwfmt = ('{stId:13} '
    ####          'dis={isInDisease:1} dia={hasDiagram:1} inferred={isInferred:1} '
    ####          '{releaseDate} {displayName}')

    #### exp_schema_class = set(['Pathway', 'TopLevelPathway'])
    #### excl_pw = set(['dbId', 'speciesName', 'oldStId', 'name', 'stIdVersion'])

    #### # LiteratureReference EXCLUDE: volume schemaClass pages dbId title
    #### ntlit = cx.namedtuple('ntlit', 'year pubMedIdentifier displayName journal')
    #### nturl = cx.namedtuple('nturl', 'URL title')
    #### ntgo = cx.namedtuple('ntgo', 'displayName accession')  # definition url
    #### # http://www.ebi.ac.uk/biomodels-main/publ-model.do?mid=BIOMD000000046,8

    def __init__(self, pw2info):
        self.pw2info = pw2info
        self.taxnt = self._init_taxnt()
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
                    prt.write("{VAL}\n".format(VAL=val))  # dict
                else:
                    for item in val:  # list
                        prt.write('{REL:20} {ITEM}\n'.format(REL=rel, ITEM=item))
                # prt.write(rel, val)
                #for elem in dct:
                #    prt.write(elem)

    def wrpy_summation(self, fpat_py):
        """Write pathway summation to a Python file."""
        fout_py = fpat_py.format(ABC=self.taxnt.abc)
        with open(os.path.join(REPO, fout_py), 'w') as prt:
            prt_docstr_module('Summations for pathways', prt)
            prt.write('# pylint: disable=line-too-long,too-many-lines\n')
            prt.write("PW2SUMS = {\n")
            for pwy, dct in sorted(self.pw2info.items()):
                prt.write("    '{KEY}': {VAL},\n".format(KEY=pwy, VAL=dct['summation']))
            prt.write("}\n")
            prt_copyright_comment(prt)
            print('  WROTE: {PY}'.format(PY=fout_py))

    def _init_taxnt(self):
        """Get the taxid for this set of pathways."""
        taxids = next(iter(self.pw2info.values()))['taxId']
        assert len(taxids) == 1
        return self.taxid2nt[taxids[0]]


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reservedsEvent
