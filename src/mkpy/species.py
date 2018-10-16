#!/usr/bin/env python
"""Print all species in Reactome."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
from neo4j import GraphDatabase
from reactomeneo4j.code.wrpy import REPO
from reactomeneo4j.code.wrpy import prt_docstr_module
from reactomeneo4j.code.wrpy import prt_namedtuple
from reactomeneo4j.code.wrpy import prt_dict
from reactomeneo4j.code.wrpy import prt_copyright_comment


def prt_species():
    """Print all species in Reactome."""
    fout_species_py = os.path.join(REPO, 'src/reactomeneo4j/data/species.py')
    fout_common_py = os.path.join(REPO, 'src/reactomeneo4j/data/species_commonnames.py')
    # Get a list of species dicts from Neo4j
    species = _get_species()
    _prt_info(fout_species_py, species)
    taxid2names = {d['taxId']:d['name'] for d in species}
    _prt_common_names(fout_common_py, taxid2names, 'TAXID2NAMES')

def _prt_common_names(fout_py, taxid2names, name):
    """Print species common names."""
    with open(fout_py, 'w') as prt:
        prt_docstr_module('Common name for the species in Reactome', prt)
        prt.write('# pylint: disable=line-too-long\n')
        taxid_names = sorted(taxid2names.items())
        prt_dict(taxid_names, name, afmt='{A}', bfmt=None, prt=prt)
        prt_copyright_comment(prt)
        print('  WROTE: {PY}'.format(PY=fout_py))

def _prt_info(fout_py, species):
    """Print Reactome species main information."""
    fields = ['abc', 'abbreviation', 'taxId', 'displayName']
    with open(fout_py, 'w') as prt:
        prt_docstr_module('Species in Reactome', prt)
        prt.write('import collections as cx\n\n')
        prt_namedtuple(species, 'species', fields, prt)
        prt_copyright_comment(prt)
        print('  WROTE: {PY}'.format(PY=fout_py))

    # with open(fout_py, 'w') as prt:

def _get_species():
    species = []
    assert len(sys.argv) != 1, "NO NEO4J PASSWORD PROVIDED"
    password = sys.argv[1]
    gdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
    fields_exp = set(['name', 'schemaClass', 'abbreviation', 'displayName', 'taxId', 'dbId'])
    fields_keep = set(['name', 'abbreviation', 'displayName', 'taxId'])
    with gdr.session() as session:
        res = session.run('MATCH (s:Species) RETURN s')
        for rec in res.records():
            node = rec['s']
            assert node.keys() == fields_exp
            assert node.get('schemaClass') == 'Species'
            key2val = {f:node.get(f) for f in fields_keep}
            key2val['taxId'] = int(key2val['taxId'])
            key2val['abc'] = key2val['abbreviation'].lower()
            species.append(key2val)
    _chk_cnts(species)
    species = sorted(species, key=lambda d: [d['abc'], d['taxId']])
    return species

def _chk_cnts(species):
    """Expect that taxIds and displayNames are unique while abbreviation is not."""
    num_species = len(species)
    taxids = set()     # 9940
    display = set()    # 'Ovis aries'
    abc = set()        # 'OAR'
    for dct in species:
        taxids.add(dct['taxId'])
        display.add(dct['displayName'])
        abc.add(dct['abbreviation'])
    assert len(taxids) == num_species
    assert len(display) == num_species
    assert len(abc) != num_species


if __name__ == '__main__':
    prt_species()

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
