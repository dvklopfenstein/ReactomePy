"""Read pathways from neo4j and write to Python."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
import collections as cx
import timeit
import datetime
from neo4j import GraphDatabase
# import textwrap
from reactomeneo4j.data.species import SPECIES


class PathwayQuery(object):
    """Collect pathway description, summary, and literature using Neo4j queries."""

    pwfmt = ('{stId:13} '
             'dis={isInDisease:1} dia={hasDiagram:1} inferred={isInferred:1} '
             '{releaseDate} {displayName}')

    exp_schema_class = set(['Pathway', 'TopLevelPathway'])
    excl_pw = set(['dbId', 'speciesName', 'oldStId', 'name', 'stIdVersion'])
    # Stored for every Book: ISBN year title
    excl_book = set(['dbId', 'schemaClass', 'displayName', 'ISBN', 'year', 'title'])

    # LiteratureReference EXCLUDE: volume schemaClass pages dbId title
    ntlit = cx.namedtuple('ntlit', 'year displayName journal')
    ntbook = cx.namedtuple('ntbook', 'year ISBN title other')
    nturl = cx.namedtuple('nturl', 'URL title')
    ntgo = cx.namedtuple('ntgo', 'displayName GO')  # definition url
    # http://www.ebi.ac.uk/biomodels-main/publ-model.do?mid=BIOMD000000046,8

    def __init__(self, species, gdbdr):
        self.log = sys.stdout
        self.name2nt = {nt.displayName:nt for nt in SPECIES}
        assert species in self.name2nt, "SPECIES({S}) NOT FOUND IN:\n{A}\n".format(
            S=species, A="\n".join(sorted(self.name2nt)))
        self.species = species
        self.abc = self.name2nt[species].abc
        self.gdr = gdbdr
        self.reltype2fnc = {
            'inferredTo': self._get_inferredto,
            'summation': self._get_summation,
            # Pubs, Books, URLs
            'literatureReference': self._load_literatureref,
            'species': self._get_taxid,
            'crossReference': self._get_crossreference,
            'disease': self._get_disease,
            'hasEncapsulatedEvent': self._get_hasencapsulatedevent,
            'normalPathway': self._get_normalpathway,
            'figure': self._get_figure,
            'relatedSpecies': self._get_relatedspecies,
            'hasEvent': self._get_event,
        }

    def get_version(self):
        """Get Reactome version."""
        qry = 'MATCH (v:DBInfo) RETURN v'
        with self.gdr.session() as session:
            for rec in session.run(qry).records():
                dbinfo = rec['v']
                assert dbinfo.get('name') == 'reactome'
                return dbinfo.get('version')

    def get_pw2dcts(self, prt=sys.stdout):
        """Fill in Pathway with information by following other relationships."""
        pw2info = {}
        self.log = prt
        tic = timeit.default_timer()
        #qry_pw = 'MATCH (pw:Pathway{stId:"R-HSA-3000480"})-'
        qry = "".join([
            'MATCH (pw:Pathway{{speciesName:"{species}"}})-'.format(species=self.species),
            '[r]->(dst) RETURN pw, r, dst'])
        # Pathway relationships for Homo sapiens
        # Y   21040 inferredTo
        # x   14504 hasEvent
        # Y     294 normalPathway
        #       174 precedingEvent
        #
        # Y    8845 literatureReference
        # Y    2224 summation
        # Y    2222 species
        # Y    1422 crossReference
        # Y    1320 compartment
        # Y     970 goBiologicalProcess
        # Y     526 disease
        # Y     351 hasEncapsulatedEvent
        # Y     268 figure
        # Y     190 relatedSpecies
        # reltypes = cx.Counter()
        missing = cx.Counter()
        with self.gdr.session() as session:
            for rec in session.run(qry).records():
                rel = rec['r']
                typ = rel.type
                # reltypes[rel.type] += 1
                dst = rec['dst']
                # Updating dct updates pw2info
                dct = self._get_pwdct(pw2info, rec['pw'])
                # Pathways and TopLevelPathways
                if typ in self.reltype2fnc:
                    self.reltype2fnc[typ](dct, rel, dst)
                # Gene Ontology
                elif rel.type == 'compartment':
                    assert dst['schemaClass'] == 'Compartment'
                    self._get_go('Compartment', dct, rel, dst)
                elif rel.type == 'goBiologicalProcess':
                    assert dst['schemaClass'] == 'GO_BiologicalProcess'
                    self._get_go('GO_BiologicalProcess', dct, rel, dst)
                else:
                    missing[rel.type] += 1
                    # print(rel)  # stoichiometry order
                    # print(" ".join(dst.keys()))
                    # print("")
                # print("--------------------------------------------", dct['Pathway']['stId'])
                # print(dct)
                # pw2info[dct['Pathway']['stId']] = dct
            # print("{N} {FLD} FIELDS FOUND".format(N=cnt, FLD=field))
        # self.prt_cnts(reltypes)
        self.prt_cnts(missing)
        hms = str(datetime.timedelta(seconds=(timeit.default_timer()-tic)))
        print("HMS {HMS} {N:5} Pathways READ".format(HMS=hms, N=len(pw2info)))
        self.log = sys.stdout
        return pw2info

    def _get_pwdct(self, pw2info, pwy):
        """Return the dictionary in pw2info or create one."""
        stid = pwy['stId']
        if stid in pw2info:
            return pw2info[stid]
        dct_pwy = {k:v for k, v in pwy.items() if k not in self.excl_pw}
        assert pwy.get('schemaClass') in self.exp_schema_class, pwy.get('schemaClass')
        assert pwy.get('speciesName') == self.species
        #relctr = self._get_relationship_typecnt(session, stid)
        #print(self.pwfmt.format(**dct_pwy), relctr.most_common())
        # print(self.pwfmt.format(**dct_pwy))
        dct_all = {'Pathway':dct_pwy}
        pw2info[stid] = dct_all
        return dct_all

    def _load_literatureref(self, dct, rel, dst):
        """Get the destination thru the literatureReference relationship."""
        schema_class = dst['schemaClass']
        if schema_class == 'LiteratureReference':
            self.get_pub(dct, rel, dst)
        elif schema_class == 'Book':
            self._add_book(dct, rel, dst)
        elif schema_class == 'URL':
            self._add_url(dct, rel, dst)
        else:
            assert False, "UNKNOWN LiteratureReference({})".format(dst)

    def _add_book(self, dct, rel, dst):
        """Add Book Node info thru the literatureReference relationship."""
        # Book nodes have other relationships: author, created, publisher, modified, etc.
        # Dict fields include: ISBN year title and sometimes chapterTitle and pages
        # Skip displayName since info repeated in other fields (except author)
        assert dst['schemaClass'] == 'Book', dst
        # assert set(dct.keys()).intersection(set(['year', 'ISBN', 'title'])), dct
        dst_opt = {k:v for k, v in dst.items() if k not in self.excl_book}
        book = (rel['order'],
                self.ntbook(other=dst_opt, year=dst['year'], ISBN=dst['ISBN'], title=dst['title']))
        # print('BOOK', book)
        if 'Book' in dct:
            dct['Book'].append(book)
        else:
            dct['Book'] = [book]

    def _add_url(self, dct, rel, dst):
        """Add URL Node info thru the literatureReference relationship."""
        url = (rel['order'], self.nturl(URL=dst['uniformResourceLocator'], title=dst['title']))
        # self.log.write('URL({URL})\n'.format(URL=url))
        assert dst['schemaClass'] == 'URL', dst
        assert rel['stoichiometry'] == 1
        # print('URL', [url])
        if 'URL' in dct:
            dct['URL'].append(url)
        else:
            dct['URL'] = [url]

    def get_pub(self, dct_pw, rel, dst):
        """Get pubmed info given a relationship and a destination Node."""
        assert rel['stoichiometry'] == 1
        assert dst['schemaClass'] == 'LiteratureReference', dst
        assert rel['order'] >= 0
        dct_vals = {f:dst[f] for f in self.ntlit._fields}
        #### dct_vals['order'] = rel['order']
        ntd = self.ntlit(**dct_vals)
        # Check that 'title' and 'displayName' are the same
        title = self.rm_period(dst['title'])
        dct_vals['displayName'] = self.rm_period(dst['displayName'])
        if dct_vals['displayName'].lower() != title.lower():
            self.log.write("\nDISPLAY({})\nTITLE  ({})\n".format(dct_vals['displayName'], title))
        # print("PUB", ntd)
        pubmed = dst['pubMedIdentifier']
        order = rel['order']
        if pubmed is not None:
            if 'LiteratureReference' in dct_pw:
                dct_pw['LiteratureReference'].append((order, (pubmed, ntd)))
            else:
                dct_pw['LiteratureReference'] = [(order, (pubmed, ntd))]
        else:
            if 'Lit_pweratureReferenceNoPubMed' in dct_pw:
                dct_pw['LiteratureReferenceNoPubMed'].append((order, ntd))
            else:
                dct_pw['LiteratureReferenceNoPubMed'] = [(order, ntd)]
        return ntd

    def _get_go(self, name, dct, rel, dst):
        """Get Compartments in a pathway."""
        # 'displayName': 'nucleoplasm',
        # 'definition': 'That part of the nuclear content other than chromosomes or nucleolus',
        # 'accession': '0005654',
        # 'url':'http://www.ebi.ac.uk/ego/QuickGO?mode=display&entry=GO:0005654'}>
        assert rel['stoichiometry'] == 1
        assert dst['displayName'] == dst['name'], '{} {}'.format(dst['displayName'], dst['name'])
        assert dst['databaseName'] == 'GO'
        comp = self.ntgo(displayName=dst['displayName'], GO="GO:{GO}".format(GO=dst['accession']))
        if name in dct:
            dct[name].append(comp)
        else:
            dct[name] = [comp]

    @staticmethod
    def _get_crossreference(dct, rel, dst):
        """Get pathway crossReference."""
        assert dst['databaseName'] in set(['BioModels Database', 'OMIM']), dst
        assert dst['schemaClass'] == 'DatabaseIdentifier'
        assert rel['stoichiometry'] == 1
        if 'crossreference' not in dct:
            dct['crossreference'] = [dst['displayName']]
        else:
            dct['crossreference'].append(dst['displayName'])

    def _get_taxid(self, dct, rel, dst):
        """Get taxId text given a relationship and a destination Node."""
        assert dst['schemaClass'] == 'Species'
        assert rel['stoichiometry'] == 1
        # Mostly, there is one Species per pathway
        taxid = int(dst['taxId'])
        if 'taxId' not in dct:
            dct['taxId'] = [taxid]
        # Sometimes there is more than one taxId per pathway
        else:
            dct['taxId'].append(taxid)
            self.log.write('TAXIDS: {DCT}\n'.format(DCT=dct))

    @staticmethod
    def _get_summation(dct, rel, dst):
        """Get summation text given a relationship and a destination Node."""
        assert dst['schemaClass'] == 'Summation'
        assert rel['stoichiometry'] == 1
        # Mostly, there is one summation per pathway
        if 'summation' not in dct:
            dct['summation'] = [dst['text']]
        # Sometimes there is more than one summation per pathway
        else:
            dct['summation'].append(dst['text'])

    @staticmethod
    def _get_disease(dct, rel, dst):
        """Get disease associated with a pathway."""
        assert dst['schemaClass'] == 'Disease'
        assert dst['databaseName'] == 'DOID'
        assert rel['stoichiometry'] == 1
        # print("DISEASE", dst)
        if 'disease' not in dct:
            dct['disease'] = [dst['displayName']]
        else:
            dct['disease'].append(dst['displayName'])

    def _get_hasencapsulatedevent(self, dct, rel, dst):
        """Get encapsulated event."""
        assert dst['stId'] is not None, dst
        assert dst['schemaClass'] in self.exp_schema_class, dst  # (TopLevel)?Pathway
        assert rel['stoichiometry'] == 1
        # print("GET_ENCAPSULATED_EVENT", dst)
        if 'hasEncapsulatedEvent' not in dct:
            dct['hasEncapsulatedEvent'] = [dst['stId']]
        else:
            dct['hasEncapsulatedEvent'].append(dst['stId'])

    @staticmethod
    def _get_figure(dct, rel, dst):
        """Get figure."""
        assert dst['schemaClass'] == 'Figure'
        assert rel['stoichiometry'] == 1
        # print("GET_FIGURE", dst)
        fig = dst['displayName']
        assert fig[:9] == '/figures/', fig
        fig = fig[9:]
        assert fig is not None
        if 'figure' not in dct:
            dct['figure'] = [fig]
        else:
            dct['figure'].append(fig)

    @staticmethod
    def _get_normalpathway(dct, rel, dst):
        """Get normal pathway."""
        assert dst['schemaClass'] == 'Pathway'
        assert rel['stoichiometry'] == 1
        # print("GET_NORMAL_PATHWAY", dst)
        if 'normalPathway' not in dct:
            dct['normalPathway'] = [dst['stId']]
        else:
            dct['normalPathway'].append(dst['stId'])

    @staticmethod
    def _get_relatedspecies(dct, rel, dst):
        """Get related species."""
        assert dst['schemaClass'] == 'Species'
        assert rel['stoichiometry'] == 1
        # print("GET_RELATED_SPECIES", dst)
        if 'relatedSpecies' not in dct:
            dct['relatedSpecies'] = set([int(dst['taxId'])])
        else:
            dct['relatedSpecies'].add(int(dst['taxId']))

    def _get_inferredto(self, dct, rel, dst):
        """Get inferred to."""
        assert dst['schemaClass'] in self.exp_schema_class, dst  # (TopLevel)?Pathway
        assert rel['stoichiometry'] == 1
        # print("\nDCT GET_INFERRED_TO", dct)
        # print("KEY GET_INFERRED_TO", dct.keys())
        # print("DST GET_INFERRED_TO", dst)
        if 'inferredTo' not in dct:
            dct['inferredTo'] = [dst['stId']]
        else:
            # print("INF GET_INFERRED_TO", dct['inferredTo'])
            dct['inferredTo'].append(dst['stId'])
        # print("INF GET_INFERRED_TO", dct['inferredTo'])

    @staticmethod
    def _get_event(dct, rel, dst):
        assert rel['stoichiometry'] == 1
        #print("GET_EVENT", dst)

    @staticmethod
    def _get_relationship_typecnt(session, pw_stid):
        ctr = cx.Counter()
        qry = 'MATCH (Pathway{{stId:"{ID}"}})-[r]-() RETURN r'.format(ID=pw_stid)
        res = session.run(qry)
        for rec in res.records():
            ctr[rec['r'].type] += 1
        return ctr



    @staticmethod
    def rm_period(title):
        """Remove ending period, if one exists."""
        return title if title[-1] != '.' else title[:-1]

    @staticmethod
    def prt_cnts(ctr, prt=sys.stdout):
        """Print counts of items found in a Counter."""
        for fld, cnt in ctr.most_common():
            prt.write("  {CNT:6} {FLD}\n".format(CNT=cnt, FLD=fld))


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reservedsEvent
