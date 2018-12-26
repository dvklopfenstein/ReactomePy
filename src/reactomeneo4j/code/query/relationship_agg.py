"""Functions to run Neo4j queries."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# from collections import defaultdict
from reactomeneo4j.code.node.databaseobject import DatabaseObject
from reactomeneo4j.code.relationships import Relationships
# from reactomeneo4j.code.query.node_tasks import get_id2children
# from reactomeneo4j.code.query.node_tasks import get_id2parents
from goatools.godag.go_tasks import get_id2children
from goatools.godag.go_tasks import get_id2parents


# pylint: disable=too-few-public-methods
class RelationshipCollapse():
    """Pull data from lower-level relationship nodes. Rm rels."""

    def __init__(self, dbid2node, dbid2dct, all_details=True):
        self.dbid2node = dbid2node
        self.dbid2dct = dbid2dct
        self.all_details = all_details
        self.rel2fnc = {
            'species': self._get_abc,
            'compartment': self._get_compartment,
            'referenceDatabase': self._get_db,
        }
        # Relationships to child PhysicalENtity
        # self.relhier2fnc = {
        #     'hasMember': self._get_hier_pe,
        #     'hasComponent': self._get_hier_pe,
        #     'hasCandidate': self._get_hier_pe,
        #     'repeatedUnit': self._get_hier_pe,
        #     'entityOnOtherCell': self._get_hier_pe,
        # }
        self._collapse_relationships()

    def mv_children_parents(self):
        """Move children from selected relationships to children parameters for ALL nodes."""
        for srcnode in self.dbid2node.values():
            relationships = Relationships.physicalentity_hier.intersection(srcnode.relationship)
            for rel in relationships:
                dstnodes = srcnode.relationship[rel]
                srcnode.children.update(dstnodes)
                for dstnode in dstnodes:
                    dstnode.parents.add(srcnode)

    def set_dcnt(self):
        """Initialize descendant count."""
        id2descendants = get_id2children(self.dbid2node.values())
        for dbid, descendants in id2descendants.items():
            node = self.dbid2node[dbid]
            node.descendants = descendants
            node.dcnt = len(descendants)

    def set_ancestors(self):
        """Initialize ancestors count."""
        id2ancestors = get_id2parents(self.dbid2node.values())
        for id_, ancestors in id2ancestors.items():
            node = self.dbid2node[id_]
            node.ancestors = ancestors

    # def _mv_children(self, node, rel, dstnodes):
    #     """Move children from relationships to children parameters for ONE node."""

    def _collapse_relationships(self):
        """Collapse specfied relationships into the main node dict."""
        popped = {}
        for dbid_src, node in self.dbid2node.items():
            k2v = self.dbid2dct[dbid_src]
            # Merge relationship destination node info into current node
            rel2dstdbids_rm = {}
            for rel, dstnodes in node.relationship.items():
                if rel in self.rel2fnc:
                    rel2dstdbids_rm[rel] = self.rel2fnc[rel](k2v, dstnodes)
            for rel, dstdbids_rm in rel2dstdbids_rm.items():
                node.relationship[rel] = set(o for o in node.relationship[rel] if o.item_id not in dstdbids_rm)
            rels_rm = set(r for r, objs in node.relationship.items() if not objs)
            # print('RRRRR REMOVING COLLAPSED RELATIONSHIPS', rels_rm)

            # print('DDDDDDDDDDDDDDDD', dbid_src, rel, dstdbidsrm)
            # # Remove relationships when thier info has been merged into parent node
            # for dbid_node in dstnodes:
            #     if dbid_node.item_id in dstdbidsrm:
            #         node.relationship[rel]
            for rel in rels_rm:
                popped[(dbid_src, rel)] = node.relationship.pop(rel)
        return popped

    def _get_db(self, sdct, referencedatabases):
        """Push database displayName onto parent."""
        dbids_rm = set()
        for odst in referencedatabases:
            ddct = self.dbid2dct[odst.item_id]
            if 'identifier' in sdct:
                sdct['displayName'] = '{DB}:{ID}'.format(DB=ddct['displayName'], ID=sdct['identifier'])
                dbids_rm.add(odst.item_id)
            elif ddct['displayName'] == 'GO' and 'GO' in sdct['displayName']:
                dbids_rm.add(odst.item_id)
        return dbids_rm

    def _get_compartment(self, dct, compartments):
        """Push compartment displayName onto parent, if necessary."""
        for comp in compartments:
            comp_dct = self.dbid2dct[comp.item_id]
            if comp_dct['displayName'] not in dct['displayName']:
                # print('ADDING COMPARTMENT', node)
                dct['displayName'] += '[{COMP}]'.format(COMP=comp_dct['displayName'])
        return set(o.item_id for o in compartments)

    def _get_abc(self, dct, species_nodes):
        """Return a value for abc."""
        abc = self.__get_abc(dct['abc'], species_nodes, dct)
        dct['abc'] = abc
        assert abc not in {'???', 'XXX'}
        return set(o.item_id for o in species_nodes)

    def __get_abc(self, abc_param, species_nodes, dct):
        """Return a value for abc."""
        _abc = DatabaseObject.species2nt.get
        # pylint: disable=line-too-long
        abc_rel = '-'.join(_abc(self.dbid2dct[o.item_id]['displayName'], '???').abbreviation for o in species_nodes)
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
