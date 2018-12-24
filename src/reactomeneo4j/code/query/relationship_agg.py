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
        self.rel2fnc = {
            'species': self._get_abc,
            'compartment': self._get_compartment
        }
        self._collapse_relationships()

    def _collapse_relationships(self):
        """Collapse specfied relationships into the main node dict."""
        popped = {}
        _dbid2dct = self.dbid2dct
        for dbid, node in self.dbid2node.items():
            k2v = _dbid2dct[dbid]
            for rel, dstnodes in node.relationship.items():
                if rel in self.rel2fnc:
                    self.rel2fnc[rel](k2v, dstnodes)
            for rel in set(node.relationship).intersection(self.rel2fnc):
                if rel in self.rel2fnc:
                    popped[(dbid, rel)] = node.relationship.pop(rel)
        return popped

    def _get_compartment(self, dct, compartments):
        """Push compartment displayName onto parent."""
        for comp in compartments:
            comp_dct = self.dbid2dct[comp.dbid]
            if comp_dct['displayName'] not in dct['displayName']:
                # print('ADDING COMPARTMENT', node)
                dct['displayName'] += '[{COMP}]'.format(COMP=comp_dct['displayName'])

    def _get_abc(self, dct, species_nodes):
        """Return a value for abc."""
        abc = self.__get_abc(dct['abc'], species_nodes, dct)
        dct['abc'] = abc
        assert abc not in {'???', 'XXX'}

    def __get_abc(self, abc_param, species_nodes, dct):
        """Return a value for abc."""
        _abc = DatabaseObject.species2nt.get
        # pylint: disable=line-too-long
        abc_rel = '-'.join(_abc(self.dbid2dct[o.dbid]['displayName'], '???').abbreviation for o in species_nodes)
        # if abc_param == '...' or abc_param == abc_rel:
        if abc_param in {'...', abc_rel}:
            return abc_rel
        print('**ERROR: {SCH}{{dbId:{DBID}}} PARAMETER({P}) != species RELATIONSHIP({R})'.format(
            DBID=dct['dbId'], SCH=dct['schemaClass'], P=abc_param, R=abc_rel))
        return 'XXX'

    @staticmethod
    def prt_dct(dct):
        """Print params dct of one node."""
        # Required Parameters on this Node
        msg = ['{dbId} {schemaClass}'.format(dbId=dct['dbId'], schemaClass=dct['schemaClass'])]
        msg[0] += ' ' + dct['displayName']
        excl = {'dbId', 'schemaClass', 'displayName', 'optional'}
        dctlst = ['{}({})'.format(k, v) for k, v in sorted(dct.items()) if k not in excl]
        if dctlst:
            msg.append(' '.join(dctlst))
        # Optional Parameters on this Node
        if 'optional' in dct:
            optlst = ['{}({})'.format(k, v) for k, v in sorted(dct['optional'].items())]
            msg.append(' '.join(optlst))

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
