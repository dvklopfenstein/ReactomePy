#!/usr/bin/env python
"""Print all disease in Reactome."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
from neo4j import GraphDatabase
from reactomeneo4j.code.wrpy.utils import REPO
from reactomeneo4j.code.wrpy.utils import prt_docstr_module
from reactomeneo4j.code.wrpy.utils import prt_namedtuple
from reactomeneo4j.code.wrpy.utils import prt_dict
from reactomeneo4j.code.wrpy.utils import prt_copyright_comment


def prt_disease():
    """Print all disease in Reactome."""
    fout_disease_py = os.path.join(REPO, 'src/reactomeneo4j/data/disease_definitions.py')
    #fout_common_py = os.path.join(REPO, 'src/reactomeneo4j/data/disease_synonyms.py')
    # Get a list of disease dicts from Neo4j
    diseases = _get_disease()
    _prt_disease2defn(fout_disease_py, diseases, 'DISEASE2DEFN')
    # _prt_info(fout_disease_py, disease) TBD Names and synonyms

def _prt_disease2defn(fout_py, diseases, name):
    """Print disease common names."""
    # Find all diseases which have definitions
    with open(fout_py, 'w') as prt:
        dis2defn = _get_dis2defn(diseases)
        docstr = '{N} of {M} diseases in Reactome have definitions'.format(
            M=len(diseases), N=len(dis2defn))
        prt_docstr_module(docstr, prt)
        prt.write('# pylint: disable=line-too-long\n')
        disease_names = sorted(dis2defn.items())
        prt_dict(disease_names, name, afmt='"{A}"', bfmt='"{B}"', prt=prt)
        prt_copyright_comment(prt)
        print('  WROTE: {PY}'.format(PY=fout_py))

def _get_dis2defn(diseases):
    """Get all diseases that have definitions."""
    dis2defn = {}
    for dct in diseases:
        defn = dct['definition']
        if defn is not None:
            dis2defn[dct['displayName']] = defn
    return dis2defn

def _prt_info(fout_py, disease):
    """Print Reactome disease main information."""
    fields = ['abc', 'abbreviation', 'taxId', 'displayName']
    with open(fout_py, 'w') as prt:
        prt_docstr_module('Species in Reactome', prt)
        prt.write('import collections as cx\n\n')
        prt_namedtuple(disease, 'disease', fields, prt)
        prt_copyright_comment(prt)
        print('  WROTE: {PY}'.format(PY=fout_py))

    # with open(fout_py, 'w') as prt:

def _get_disease():
    disease = []
    assert len(sys.argv) != 1, "NO NEO4J PASSWORD PROVIDED"
    password = sys.argv[1]
    gdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    # fields_exp = set(['name', 'schemaClass', 'abbreviation', 'displayName', 'taxId', 'dbId'])
    fields_keep = set(['displayName', 'definition', 'synonym', 'name'])
    with gdr.session() as session:
        res = session.run('MATCH (n:Disease) RETURN n')
        for rec in res.records():
            node = rec['n']
            # assert node.keys() == fields_exp
            assert node.get('schemaClass') == 'Disease'
            assert node.get('databaseName') == 'DOID'
            key2val = {f:node.get(f) for f in fields_keep}
            disease.append(key2val)
    _chk_cnts(disease)
    disease = sorted(disease, key=lambda d: d['displayName'])
    return disease

def _chk_cnts(disease):
    """Expect that displayNames are unique."""
    num_disease = len(disease)
    display = set()
    for dct in disease:
        display.add(dct['displayName'])
    assert len(display) == num_disease


if __name__ == '__main__':
    prt_disease()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
