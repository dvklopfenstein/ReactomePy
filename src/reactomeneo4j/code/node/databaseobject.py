"""Lists parameters seen on all DatabaseObjects."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from collections import namedtuple
from reactomeneo4j.data.species import SPECIES
from reactomeneo4j.code.schema.hier import DataSchemaHier


# pylint: disable=too-few-public-methods
class DatabaseObject():
    """Lists parameters seen on all DatabaseObjects."""

    objhier = DataSchemaHier()
    params_req = ('dbId', 'schemaClass', 'displayName')
    params_opt = ()
    prtfmt = '{dbId:8} {schemaClass:32} {displayName}'
    species2nt = {nt.displayName:nt for nt in SPECIES}

    # 'is' params:
    P2A = {  # Parameter-to-letter
        'isInDisease': 'D',
        'isInferred': 'I',
        'isChimeric': 'C',
        'isSequenceChanged': 'S',
        'isOrdered': 'O'
    }
    # If these relationships exist, add aliases to ASCII art markers
    R2A = {
        'figure': 'F',
        'disease': 'D',
    }

    relationships = {}

    ntobj = namedtuple('NtOpj', ' '.join(params_req + ('optional',)))

    def __init__(self, name):
        self.name = name
        # print('CREATING {S}'.format(S=name))

    def get_dict(self, node):
        """Return a Python dict containing all Neo4j Node parameters."""
        k2v = {p:node[p] for p in self.params_req}
        k2v['optional'] = {o:node[o] for o in self.params_opt if o in node}
        return k2v

    # pylint: disable=unused-argument
    @staticmethod
    def get_optstr(optional_dct):
        """Given optional dictionary, return printable strings."""
        return {}

    def get_nt(self, node):
        """Return a Python namedtuple containing all Neo4j Node parameters."""
        return self.ntobj(**self.get_dict(node))

    def get_nt_g_dct(self, dct):
        """Return a Python namedtuple using key-value pairs in dct."""
        k2v = {f:dct[f] for f in self.ntobj._fields}
        return self.ntobj(**k2v)

    def _get_abc(self, k2vopt):
        if 'speciesName' in k2vopt:
            species = k2vopt['speciesName']
            return self.species2nt[species].abbreviation if species in self.species2nt else 'nnn'
        return '...'


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
