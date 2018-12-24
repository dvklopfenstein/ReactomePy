"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from reactomeneo4j.code.node.databaseobject import DatabaseObject


# pylint: disable=too-few-public-methods
class RelationshipCollapse():
    """Pull data from lower-level relationship nodes. Rm rels."""

    def __init__(self, dbid2node, dbid2dct, all_details=True):
        self.dbid2node = dbid2node
        self.dbid2dct = dbid2dct
        self.all_details = all_details
        self._collapse_relationships()

    def _collapse_relationships(self):
        """Collapse specfied relationships into the main node dict."""
        popped = {}
        _dbid2dct = self.dbid2dct
        for dbid, node in self.dbid2node.items():
            k2v = _dbid2dct[dbid]
            rel = node.relationship
            if 'abc' in k2v and 'species' in rel:
                self._get_abc(rel['species'], _dbid2dct, k2v)
                popped[(dbid, 'species')] = rel.pop('species')
            if 'compartment' in rel:
                self._get_compartment(k2v, rel['compartment'])
                popped[(dbid, 'compartment')] = rel.pop('compartment')
        return popped

    def _get_compartment(self, dct, compartments):
        """Push compartment displayName onto parent."""
        for comp in compartments:
            comp_dct = self.dbid2dct[comp.dbid]
            if comp_dct['displayName'] not in dct['displayName']:
                # print('ADDING COMPARTMENT', node)
                dct['displayName'] += '[{COMP}]'.format(COMP=comp_dct['displayName'])

    def _get_abc(self, species_nodes, dbid2dct, dct):
        """Return a value for abc."""
        abc = self.__get_abc(dct['abc'], species_nodes, dbid2dct, dct)
        dct['abc'] = abc
        assert abc not in {'???', 'XXX'}

    @staticmethod
    def __get_abc(abc_param, species_nodes, dbid2dct, dct):
        """Return a value for abc."""
        _abc = DatabaseObject.species2nt.get
        # pylint: disable=line-too-long
        abc_rel = '-'.join(_abc(dbid2dct[o.dbid]['displayName'], '???').abbreviation for o in species_nodes)
        # if abc_param == '...' or abc_param == abc_rel:
        if abc_param in {'...', abc_rel}:
            return abc_rel
        print('**ERROR: {SCH}{{dbId:{DBID}}} PARAMETER({P}) != species RELATIONSHIP({R})'.format(
            DBID=dct['dbId'], SCH=dct['schemaClass'], P=abc_param, R=abc_rel))
        return 'XXX'


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
