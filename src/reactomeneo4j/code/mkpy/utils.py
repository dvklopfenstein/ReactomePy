"""Functions to write Reactome data extracted from Neo4j to Python."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
#import textwrap
import datetime

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../..")
COPYRIGHT = "Copyright (C) 2018-{YEAR}, DV Klopfenstein. All rights reserved.".format(
    YEAR=str(datetime.datetime.now().year))


def prt_dict(key_val, name, afmt='{A}', bfmt='{B}', sortby=None, prt=sys.stdout):
    """Write data in dicts into a namedtuple."""
    prt.write("{NAME} = {{\n".format(NAME=name.upper()))
    for key, val in key_val:
        if afmt is not None:
            key = afmt.format(A=key)
        if bfmt is not None:
            val = bfmt.format(B=val)
        prt.write("    {KEY}: {VAL},\n".format(KEY=key, VAL=val))
        # prt.write(str([dct[fld] for fld in flds]))
        # prt.write('),\n')
    prt.write("}\n")

def prt_namedtuple(lst_of_dcts, name, flds, prt=sys.stdout):
    """Write data in dicts into a namedtuple."""
    prt.write("NtObj = cx.namedtuple('nt{NAME}', '{FLDS}')\n".format(
        NAME=name, FLDS=" ".join(flds)))
    prt.write("{NAME} = [\n".format(NAME=name.upper()))
    for dct in lst_of_dcts:
        prt.write('    NtObj._make(')
        prt.write(str([dct[fld] for fld in flds]))
        prt.write('),\n')
    prt.write("]\n")

def prt_docstr_module(docstr, prt=sys.stdout):
    """Print module docstring."""
    prt.write('"""{DOC}"""\n\n'.format(DOC=docstr))
    prt.write('__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."\n')
    prt.write('__author__ = "DV Klopfenstein"\n\n')

def prt_copyright_comment(prt=sys.stdout):
    """Print Copyright as a comment."""
    prt.write('\n# {C}\n'.format(C=COPYRIGHT))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
