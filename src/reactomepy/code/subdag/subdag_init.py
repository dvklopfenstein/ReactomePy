"""Adds children and parents for traversing through pathways and PEs."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2016-2019, DV Klopfenstein, H Tang, All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
import math
from goatools.godag.relationship_str import RelationshipStr
from goatools.godag.go_tasks import CurNHigher
from reactomepy.code.subdag.godag_rcnt import CountRelatives
from reactomepy.code.subdag.go_tasks import get_leaf_children
from reactomepy.code.subdag.utils import get_kwargs


# pylint: disable=too-few-public-methods
class Init(object):
    """Adds children and parents for traversing through pathways and PEs."""

    # Set of relationships used to traverse the pathway and pyhsical entity hierarchy
    RELS = set([
        'input',
        'output',
        'hasComponent',
        'hasMember',
        'hasCandidate',
        'repeatedUnit',
        'catalystActivity',
        'entityFunctionalStatus',
        'physicalEntity',
        'regulatedBy',
        'regulator'])

    # Add additional GO IDs if used in user tasks
    kws_aux_gos = set(['go2color'])

    #### #### def __init__(self, go_sources, dbid2obj, relationships=False, **kws):
    #### def __init__(self, dbid2obj):
    ####     # kws: go2color, children
    ####     #### self.kws = kws
    ####     # Process: rcntobj tcntobj go2nt relationships
    ####     self.dbid2obj = dbid2obj
    ####     #### if relationships:
    ####     ####     assert hasattr(next(iter(dbid2obj.values())), 'relationship'), "NO DAG RELATIONSHIPS"
    ####     # Init dbid2obj and go_sources
    ####     #### self.go_sources = None
    ####     #### self._init_gos(go_sources, relationships)
    ####     #### # Using reduced dbid2obj, init relationships
    ####     #### self.relationships = self._init_relationships(relationships)  # set of relationship types

    def __init__(self, dbid2node):
        self.dbid2node = dbid2node
        self._add_children()
        # _child2parents = self._get_child2parents()
        # _names = set(ITEM2CHILDREN).union(_child2parents)
        # self._init_parents_children(_child2parents)
        # self._init_depth()
        # self._init_dcnt()
        # self._init_ancestors()

    def _init_dcnt(self):
        """Initialize descendant count."""
        id2descendants = get_id2children(self.dbid2node.values())
        for id_, descendants in id2descendants.items():
            obj = self.dbid2node[id_]
            obj.descendants = descendants
            obj.dcnt = len(descendants)


    def _init_ancestors(self):
        """Initialize ancestors count."""
        id2ancestors = get_id2parents(self.dbid2node.values())
        for id_, ancestors in id2ancestors.items():
            obj = self.dbid2node[id_]
            obj.ancestors = ancestors

    def _init_depth(self):
        """Set depth for a Reactome data schema object."""
        # Local function for finding depth
        def _init_depth_local(rec):
            """Recursive depth function"""
            if rec.depth is None:
                if rec.parents:
                    rec.depth = max(_init_depth_local(rec) for rec in rec.parents) + 1
                else:
                    rec.depth = 0
            return rec.depth
        # Initialize depth for each DataSchemaNode
        for rec in self.dbid2node.values():
            if rec.depth is None:
                _init_depth_local(rec)

    def _init_parents_children(self, child2parents):
        """Add links to an Reactome data schema's child and parent gene families."""
        for obj in self.dbid2node.values():
            name = obj.item_id
            if name in ITEM2CHILDREN:
                obj.children = set(self.dbid2node[i] for i in ITEM2CHILDREN[name])
            if name in child2parents:
                obj.parents = set(self.dbid2node[i] for i in child2parents[name])

    @staticmethod
    def _get_child2parents():
        """Get child-to-parent relationships for data schema."""
        child2parents = cx.defaultdict(set)
        for parent, children in ITEM2CHILDREN.items():
            for child in children:
                child2parents[child].add(parent)
        return child2parents

    def _add_children(self):
        """From relationships loaded, extract children."""
        seen = set()
        for dbid, node in self.dbid2node.items():
            if not seen:
                seen.add(dbid)
                children = set()
                for ntrel in node.ntrels:
                    if ntrel.rel in self.RELS:
                        children.add(ntrel.dst)
                node.children = children

    #### def _init_relationships(self, relationships_arg):
    ####     """Return a set of relationships found in all subset GO Terms."""
    ####     if relationships_arg:
    ####         relationships_all = self._get_all_relationships()
    ####         if relationships_arg is True:
    ####             return relationships_all
    ####         else:
    ####             return relationships_all.intersection(relationships_arg)
    ####     return set()

    #### def _get_all_relationships(self):
    ####     """Return all relationships seen in GO Dag subset."""
    ####     relationships_all = set()
    ####     for node in self.dbid2obj.values():
    ####         if node.relationship:
    ####             relationships_all.update(node.relationship)
    ####         if node.relationship_rev:
    ####             relationships_all.update(node.relationship_rev)
    ####     return relationships_all

    #### def _init_gos(self, go_sources_arg, relationships_arg):
    ####     """Initialize GO sources."""
    ####     # No GO sources provided
    ####     if not go_sources_arg:
    ####         assert self.dbid2obj_orig, "dbid2obj MUST BE PRESENT IF go_sources IS NOT"
    ####         self.go_sources = set(self.dbid2obj_orig)
    ####         self.dbid2obj = self.dbid2obj_orig
    ####         sys.stdout.write("**NOTE: {N:,} SOURCE GO IDS\n".format(N=len(self.go_sources)))
    ####         return
    ####     # GO sources provided
    ####     go_sources = self._init_go_sources(go_sources_arg, self.dbid2obj_orig)
    ####     # Create new dbid2obj_user subset matching GO sources
    ####     # Fill with source and parent GO IDs and alternate GO IDs
    ####     dbid2obj_user = {}
    ####     objrel = CurNHigher(relationships_arg, self.dbid2obj_orig)
    ####     objrel.get_id2obj_cur_n_high(dbid2obj_user, go_sources)
    ####     # Add additional GOTerm information, if needed for user task
    ####     kws_gos = {k:v for k, v in self.kws.items() if k in self.kws_aux_gos}
    ####     if kws_gos:
    ####         self._add_nodes_kws(dbid2obj_user, kws_gos)
    ####     self.go_sources = go_sources
    ####     self.dbid2obj = dbid2obj_user

    #### def _add_nodes_kws(self, dbid2obj_user, kws_gos):
    ####     """Add more GOTerms to dbid2obj_user, if requested and relevant."""
    ####     if 'go2color' in kws_gos:
    ####         for goid in kws_gos['go2color'].keys():
    ####             self._add_nodes(dbid2obj_user, goid)

    #### def _add_nodes(self, dbid2obj_user, goid):
    ####     """Add alt GO IDs to dbid2obj subset, if requested and relevant."""
    ####     node = self.dbid2obj_orig[goid]
    ####     if goid != node.id and node.id in dbid2obj_user and goid not in dbid2obj_user:
    ####         dbid2obj_user[goid] = node

    #### def _init_go_sources(self, go_sources_arg, dbid2obj_arg):
    ####     """Return GO sources which are present in GODag."""
    ####     gos_user = set(go_sources_arg)
    ####     if 'children' in self.kws and self.kws['children']:
    ####         gos_user |= get_leaf_children(gos_user, dbid2obj_arg)
    ####     gos_godag = set(dbid2obj_arg)
    ####     gos_source = gos_user.intersection(gos_godag)
    ####     gos_missing = gos_user.difference(gos_godag)
    ####     if not gos_missing:
    ####         return gos_source
    ####     sys.stdout.write("{N} GO IDs NOT FOUND IN GO DAG: {GOs}\n".format(
    ####         N=len(gos_missing), GOs=" ".join([str(e) for e in gos_missing])))
    ####     return gos_source


class InitFields(object):
    """Initialize print attributes and namedtuple fields."""

    exp_keys = set(['rcntobj', 'tcntobj', 'go2nt', 'go2letter'])

    def __init__(self, ini_main, **kws):
        self.dbid2obj = ini_main.dbid2obj
        self.kws = get_kwargs(kws, self.exp_keys, None)
        if 'rcntobj' not in kws:
            self.kws['rcntobj'] = True
        self.kw_elems = self._init_kwelems()
        self.relationships = ini_main.relationships
        self.prt_flds = self._init_prt_flds()

    def get_rcntobj(self):
        """Return None or user-provided CountRelatives object."""
        # rcntobj value in kws can be: None, False, True, CountRelatives object
        if 'rcntobj' in self.kws:
            rcntobj = self.kws['rcntobj']
            if isinstance(rcntobj, CountRelatives):
                return rcntobj
            return CountRelatives(
                self.dbid2obj,  # Subset dbid2obj contains only items needed by go_sources
                self.relationships,
                dcnt='dcnt' in self.kw_elems,
                go2letter=self.kws.get('go2letter'))

    def get_go2nt_all(self, rcntobj):
        """For each GO id, put all printable fields in one namedtuple."""
        if 'go2nt' in self.kws:
            go2nt = self.kws['go2nt']
            return {go:go2nt[go] for go in self.dbid2obj}
        else:
            return self._get_go2nt_all(rcntobj)

    def _init_prt_flds(self):
        """Return the print fields in the go2nt namedtuple."""
        # Create namedtuple fields or copy namedtuple fields
        if 'go2nt' not in self.kws:
            return self.__init_prt_flds()
        else:
            return next(iter(self.kws['go2nt'].values()))._asdict()

    def __init_prt_flds(self):
        """Return the print fields in the go2nt namedtuple."""
        prt_flds = ['NS', 'level', 'depth']
        if self.relationships:
            prt_flds.append('reldepth')
        prt_flds.extend(['GO', 'alt', 'GO_name'])
        if 'dcnt' in self.kw_elems:
            prt_flds.append('dcnt')
        if 'D1' in self.kw_elems:
            prt_flds.append('D1')
        if 'tcnt' in self.kw_elems:
            prt_flds.append('tcnt')
            prt_flds.append('tfreq')
            prt_flds.append('tinfo')
        if self.relationships:
            prt_flds.append('childcnt')
            prt_flds.append('REL')
            prt_flds.append('REL_short')
            prt_flds.append('rel')
        prt_flds.append('id')
        return prt_flds

    def get_prt_fmt(self, alt=False):
        """Return the format for printing GO named tuples and their related information."""
        # prt_fmt = [ #                                                        rcnt
        #     '{GO} # {NS}  L{level:02} D{depth:02} {GO_name}',
        #     '{GO} # {NS} {dcnt:6,} L{level:02} D{depth:02} {D1:5} {GO_name}']
        prt_fmt = []
        if alt:
            prt_fmt.append('{GO}{alt:1}')
        else:
            prt_fmt.append('{GO}')
        prt_fmt.append('# {NS}')
        if 'dcnt' in self.prt_flds:
            prt_fmt.append('{dcnt:5}')
        if 'childcnt' in self.prt_flds:
            prt_fmt.append('{childcnt:3}')
        if 'tcnt' in self.prt_flds:
            prt_fmt.append("{tcnt:7,}")
        if 'tfreq' in self.prt_flds:
            prt_fmt.append("{tfreq:8.6f}")
        if 'tinfo' in self.prt_flds:
            prt_fmt.append("{tinfo:5.2f}")
        prt_fmt.append('L{level:02} D{depth:02}')
        if self.relationships:
            prt_fmt.append('R{reldepth:02}')
        if 'D1' in self.prt_flds:
            prt_fmt.append('{D1:5}')
        if 'REL' in self.prt_flds:
            prt_fmt.append('{REL}')
            prt_fmt.append('{rel}')
        prt_fmt.append('{GO_name}')
        return " ".join(prt_fmt)

    def _get_go2nt_all(self, rcntobj):
        """For each GO id, put all printable fields in one namedtuple."""
        ### tic = timeit.default_timer()
        go2nt = {}
        ntobj = cx.namedtuple("NtGo", " ".join(self.prt_flds))
        ### tic = _rpt_hms(tic, "GoSubDag: _Init::get_go2nt")
        tcntobj = self.kws['tcntobj'] if 'tcntobj' in self.kws else None
        b_tcnt = tcntobj is not None
        # b_rcnt = rcntobj is not None and rcntobj
        objrelstr = RelationshipStr(self.relationships)
        namespace2ns = objrelstr.consts.NAMESPACE2NS
        for goid, goobj in self.dbid2obj.items():
            ns_go = namespace2ns[goobj.namespace]
            fld2vals = {
                'NS' : ns_go,
                'level' : goobj.level,
                'depth' : goobj.depth,
                'GO' : goid,
                'alt' : '' if goid == goobj.id else 'a',
                'id' : goobj.id,
                'GO_name' : goobj.name}
            if 'dcnt' in self.kw_elems:
                fld2vals['dcnt'] = rcntobj.go2dcnt.get(goid)
            if 'D1' in self.kw_elems:
                fld2vals['D1'] = rcntobj.get_d1str(goobj)
            if b_tcnt:
                tcnt = tcntobj.gocnts[goid]
                num_ns = float(tcntobj.aspect_counts[goobj.namespace])
                tfreq = float(tcnt)/num_ns if num_ns != 0 else 0
                fld2vals['tcnt'] = tcnt
                fld2vals['tfreq'] = tfreq
                fld2vals['tinfo'] = -1.0 * math.log(tfreq) if tfreq else 0
            if self.relationships:
                fld2vals['childcnt'] = len(goobj.children)
                fld2vals['reldepth'] = goobj.reldepth
                fld2vals['REL'] = objrelstr.str_relationships(goobj)
                fld2vals['REL_short'] = objrelstr.str_rel_short(goobj)
                fld2vals['rel'] = objrelstr.str_relationships_rev(goobj)
            go2nt[goid] = ntobj(**fld2vals)
        ### tic = _rpt_hms(tic, "GoSubDag: _Init::get_go2nt")
        return go2nt

    def _init_kwelems(self):
        """Init set elements."""
        ret = set()
        if 'rcntobj' in self.kws:
            ret.add('dcnt')
            ret.add('D1')
        if 'tcntobj' in self.kws:
            ret.add('tcnt')
            ret.add('tfreq')
            ret.add('tinfo')
        return ret


# Copyright (C) 2016-2019, DV Klopfenstein, H Tang, All rights reserved.
