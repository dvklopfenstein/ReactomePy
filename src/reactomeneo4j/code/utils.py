"""Functions to write Reactome data extracted from Neo4j to Python."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import timeit
import datetime
import collections as cx
from docopt import docopt
from neo4j import GraphDatabase


def chk_unique(dcts, fld2expunique):
    """Ex: Expect that taxIds and displayNames are unique while abbreviation is not."""
    num_dcts = len(dcts)
    fld2sets = cx.OrderedDict([(f, set()) for f in fld2expunique])
    for dct in dcts:
        for fld in fld2expunique:
            fld2sets[fld].add(dct[fld])
    for fld, items in fld2sets.items():
        actually_unique = len(items) == num_dcts
        assert actually_unique == fld2expunique[fld]

def get_gdbdr(docstr):
    """Return GraphDatabase driver given user args."""
    args = get_args(docstr, ['url', 'neo4j_username', 'neo4j_password'])
    return GraphDatabase.driver(args[0], auth=(args[1], args[2]))

def get_args(docstr, fields):
    """Given a doc string and desired fields, return a namedtuple w/user values."""
    fld2docopt = {
        'url': '--url',
        'neo4j_username': '--neo4j_username',
        'neo4j_password': '<neo4j_password>',
    }
    # If user provided no options, print help screen
    if len(sys.argv) == 1 and 'neo4j_password' in fields:
        sys.argv.append('-h')
    # Get user args matching doc-string
    args = docopt(docstr)
    dct = {}
    for usrfld in fields:
        argfld = fld2docopt[usrfld]
        argval = args[argfld]
        dct[usrfld] = argval
    ntobj = cx.namedtuple('NtArgs', [f for f in fields if f in fld2docopt])
    return ntobj(**dct)

def sortby_stid(stid):
    """Sort by Pathway number."""
    vals = stid.split('-')
    #### TBD: Put in test
    #### assert len(vals) == 3
    #### assert vals[0] == 'R'
    #### assert vals[1] == self.taxnt.abc.upper(), "{} {} {}".format(
    ####     vals[1], self.taxnt.abc, stid)
    return int(vals[2])

def get_hms(tic):
    """Return HMS since script started."""
    return str(datetime.timedelta(seconds=(timeit.default_timer()-tic)))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
