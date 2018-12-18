"""Manages a user-specified subset of a Reactome DAG."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2016-2019, DV Klopfenstein, H Tang, All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
# import timeit
# from goatools.test_data.godag_timed import prt_hms
from reactomeneo4j.code.subdag.subdag_init import Init
from reactomeneo4j.code.subdag.subdag_init import InitFields
from reactomeneo4j.code.subdag.go_tasks import chk_goids


class SubDag(object):
    """Manages a user-specified subset of a Reactome DAG."""

    #### def __init__(self, dbid_sources, dbid2obj, relationships=None, **kws):
    def __init__(self, dbid2obj, relationships=None, **kws):
        # kws _Init: rcntobj relationships
        # tic = timeit.default_timer()
        #### _ini = Init(dbid2obj, relationships, **kws)
        _ini = Init(dbid2obj)
        #### self.dbid_sources = _ini.dbid_sources # set(dbid_sources)
        self.dbid2obj = dbid2obj
        #### self.relationships = relationships
        # tic = prt_hms(tic, "SubDag: InitGOs")
        # GO IDs to total count of all descendants: Init to None or CountRelatives object
        #### _fld = InitFields(_ini, **kws)
        #### self.rcntobj = _fld.get_rcntobj()  # None or CountRelatives object
        #### self.prt_attr = {
        ####     'flds':_fld.prt_flds,           # namedtuple fields in go2nt
        ####     'fmt':_fld.get_prt_fmt(False),  # GO:NNNNNNN   No indication if an alternate GO ID
        ####     'fmta':_fld.get_prt_fmt(True)}  # GO:NNNNNNNa  'a' indicates if an alternate GO ID
        #### ### tic = _rpt_hms(tic, "SubDag: Create GoDepth1Letters")
        #### self.go2nt = _fld.get_go2nt_all(self.rcntobj)
        #### ### tic = _rpt_hms(tic0, "SubDag: total")
        #### prt = kws.get('prt', None)
        #### if prt is not None:
        ####     self.prt_objdesc(prt)

#    def prt_goids(self, goids=None, prtfmt=None, sortby=True, prt=sys.stdout):
#        """Given GO IDs, print decriptive info about each GO Term."""
#        if goids is None:
#            goids = self.dbid_sources
#        nts = self.get_nts(goids, sortby)
#        if prtfmt is None:
#            prtfmt = self.prt_attr['fmta']
#        for ntgo in nts:
#            key2val = ntgo._asdict()
#            prt.write("{GO}\n".format(GO=prtfmt.format(**key2val)))
#        return nts
#
#    def get_nts(self, goids=None, sortby=None):
#        """Given GO IDs, get a list of namedtuples."""
#        nts = []
#        # User GO IDs
#        if goids is None:
#            goids = self.dbid_sources
#        else:
#            chk_goids(goids, "SubDag::get_nts")
#        if goids:
#            ntobj = cx.namedtuple("NtGo", " ".join(self.prt_attr['flds']))
#            go2nt = self.get_go2nt(goids)
#            for goid, ntgo in self._get_sorted_go2nt(go2nt, sortby):
#                assert ntgo is not None, "{GO} NOT IN go2nt".format(GO=goid)
#                if goid == ntgo.GO:
#                    nts.append(ntgo)
#                else:
#                    fld2vals = ntgo._asdict()
#                    fld2vals['GO'] = goid
#                    nts.append(ntobj(**fld2vals))
#        return nts
#
#    def _get_sorted_go2nt(self, go2nt, sortby):
#        """Return sorted list of tuples."""
#        if sortby is True:
#            _fnc = self.get_fncsortnt()
#            return sorted(go2nt.items(), key=lambda t: _fnc(t[1]))
#        if sortby:
#            return sorted(go2nt.items(), key=lambda t: sortby(t[1]))
#        return go2nt.items()
#
#    def get_fncsortnt(self):
#        """Return sorted list of tuples."""
#        if 'dcnt' in self.prt_attr['flds']:
#            if 'D1' in self.prt_attr['flds']:
#                return lambda ntgo: [ntgo.NS, ntgo.depth, -1*ntgo.dcnt, ntgo.D1, ntgo.alt]
#            else:
#                return lambda ntgo: [ntgo.NS, ntgo.depth, -1*ntgo.dcnt, ntgo.alt]
#        else:
#            return lambda ntgo: [ntgo.NS, -1*ntgo.depth, ntgo.alt]
#
#    def get_go2nt(self, goids):
#        """Return dict of GO ID as key and GO object information in namedtuple."""
#        get_nt = self.go2nt
#        goids_present = set(goids).intersection(self.dbid2obj)
#        if len(goids_present) != len(goids):
#            print("GO IDs NOT FOUND IN DAG: {GOs}".format(
#                GOs=" ".join(set(goids).difference(goids_present))))
#        return {g:get_nt[g] for g in goids_present}
#
#    def get_dbid2obj(self, goids):
#        """Return a dbid2obj dict for just the user goids."""
#        dbid2obj = self.dbid2obj
#        return {go:dbid2obj[go] for go in goids}
#
#    def get_vals(self, field, goids=None):
#        """Return a dbid2obj dict for just the user goids."""
#        go2nt = self.go2nt
#        if goids is None:
#            goids = set(go2nt)
#        return [getattr(go2nt[go], field) for go in goids]
#
#    def get_key_goids(self, goids):
#        """Given GO IDs, return key GO IDs."""
#        dbid2obj = self.dbid2obj
#        return set(dbid2obj[go].id for go in goids)
#
#    def get_ns2goids(self, goids):
#        """Group GO IDs by namespace."""
#        ns2goids = cx.defaultdict(set)
#        go2nt = self.go2nt
#        for goid in goids:
#            ns2goids[go2nt[goid].NS].add(goid)
#        return {ns:gos for ns, gos in ns2goids.items()}
#
#    def prt_objdesc(self, prt):
#        """Return description of this SubDag object."""
#        txt = "INITIALIZING SubDag: {N:3} sources in {M:3} GOs rcnt({R}). {A} alt GO IDs\n"
#        alt2obj = {go:o for go, o in self.dbid2obj.items() if go != o.id}
#        prt.write(txt.format(
#            N=len(self.dbid_sources),
#            M=len(self.dbid2obj),
#            R=self.rcntobj is not None,
#            A=len(alt2obj)))
#        prt.write("             SubDag: namedtuple fields: {FLDS}\n".format(
#            FLDS=" ".join(self.prt_attr['flds'])))
#        prt.write("             SubDag: relationships: {RELS}\n".format(RELS=self.relationships))


# Copyright (C) 2016-2019, DV Klopfenstein, H Tang, All rights reserved.
