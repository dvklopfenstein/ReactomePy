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


class PathwayMaker(object):
    """Collect pathway description, summary, and literature."""

    pwfmt = ('{stId:13} '
             'dis={isInDisease:1} dia={hasDiagram:1} inferred={isInferred:1} '
             '{releaseDate} {displayName}')

    exp_schema_class = set(['Pathway', 'TopLevelPathway'])
    excl_pw = set(['dbId', 'speciesName', 'oldStId', 'name', 'stIdVersion'])

    # LiteratureReference EXCLUDE: volume schemaClass pages dbId title
    ntlit = cx.namedtuple('ntlit', 'year pubMedIdentifier displayName journal')
    nturl = cx.namedtuple('nturl', 'URL title')
    ntgo = cx.namedtuple('ntgo', 'displayName accession')  # definition url
    # http://www.ebi.ac.uk/biomodels-main/publ-model.do?mid=BIOMD000000046,8

    def __init__(self, species, password):
        self.name2nt = {nt.displayName:nt for nt in SPECIES}
        assert species in self.name2nt, "SPECIES({S}) NOT FOUND IN:\n{A}\n".format(
            S=species, A="\n".join(sorted(self.name2nt)))
        self.species = species
        self.gdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))

    def get_pw2dcts(self):
        """Fill in Pathway with information by following other relationships."""
        pw2info = {}
        tic = timeit.default_timer()
        qry_pw = 'MATCH (pw:Pathway{{speciesName:"{species}"}})-'.format(species=self.species)
        #qry_pw = 'MATCH (pw:Pathway{stId:"R-HSA-3000480"})-'
        qry_rels = ('[:summation]->(s:Summation) RETURN pw, s')
        qry_rels = ('[r]->(dst) RETURN pw, r, dst')
        qry = "".join([qry_pw, qry_rels])
        # Pathway relationships for Homo sapiens
        # x   21040 inferredTo
        # x   14504 hasEvent
        # Y     294 normalPathway
        #
        # Y    8845 literatureReference
        # Y    2224 summation
        # Y    2222 species
        # Y    1422 crossReference
        # Y    1320 compartment
        # Y     970 goBiologicalProcess
        # Y     526 disease
        # Y     351 hasEncapsulatedEvent
        #       268 figure
        #       190 relatedSpecies
        #       174 precedingEvent
        dont_do = set(['hasEvent', 'inferredTo'])
        # reltypes = cx.Counter()
        missing = cx.Counter()
        with self.gdr.session() as session:
            res = session.run(qry)
            for rec in res.records():
                rel = rec['r']
                # reltypes[rel.type] += 1
                pwy = rec['pw']
                dst = rec['dst']
                dct = self._get_pwdct(pw2info, pwy)
                if rel.type == 'summation':
                    self._get_summation(dct, rel, dst)
                elif rel.type == 'literatureReference':
                    self._load_literatureref(dct, rel, dst)
                elif rel.type == 'species':
                    self._get_taxid(dct, rel, dst)
                elif rel.type == 'crossReference':
                    self._get_crossreference(dct, rel, dst)
                # Gene Ontology
                elif rel.type == 'compartment':
                    assert dst['schemaClass'] == 'Compartment'
                    self._get_go('Compartment', dct, rel, dst)
                elif rel.type == 'goBiologicalProcess':
                    assert dst['schemaClass'] == 'GO_BiologicalProcess'
                    self._get_go('GO_BiologicalProcess', dct, rel, dst)
                # Disease
                elif rel.type == 'disease':
                    self._get_disease(dct, rel, dst)
                elif rel.type == 'hasEncapsulatedEvent':
                    self._get_hasencapsulatedevent(dct, rel, dst)
                elif rel.type == 'normalPathway':
                    self._get_normalpathway(dct, rel, dst)
                elif rel.type == 'figure':
                    self._get_figure(dct, rel, dst)
                # elif rel.type == 'authored':
                #     self._get_authored(dct, rel, dst)
                elif rel.type not in dont_do:
                    missing[rel.type] += 1
                    # print(rel)  # stoichiometry order
                    # print(" ".join(dst.keys()))
                    # print("")
            # print("{N} {FLD} FIELDS FOUND".format(N=cnt, FLD=field))
        # self.prt_cnts(reltypes)
        self.prt_cnts(missing)
        hms = str(datetime.timedelta(seconds=(timeit.default_timer()-tic)))
        print("HMS {HMS} {N:5} Pathways READ".format(HMS=hms, N=len(pw2info)))
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
            pub = self.get_pub(rel, dst)
            if 'LiteratureReferences' in dct:
                dct['LiteratureReferences'].append(pub)
            else:
                dct['LiteratureReferences'] = [pub]
        elif schema_class == 'Book':
            self._add_book(dct, dst)
        elif schema_class == 'URL':
            self._add_url(dct, dst)
        else:
            assert False, "UNKNOWN LiteratureReference({})".format(dst)

    @staticmethod
    def _add_book(dct, dst):
        """Add Book Node info thru the literatureReference relationship."""
        # Book nodes have other relationships: author, created, publisher, modified, etc.
        # Dict fields include: pages ISBN year chapterTitle
        # But displayName is sufficient currently
        book = dst['displayName']
        # print('BOOK', book)
        # print('BOOK', dst)
        if 'Book' in dct:
            dct['Book'].append(book)
        else:
            dct['Book'] = [book]

    def _add_url(self, dct, dst):
        """Add URL Node info thru the literatureReference relationship."""
        url = self.nturl(URL=dst['uniformResourceLocator'], title=dst['title'])
        print('URL', url)
        if 'URL' in dct:
            dct['URL'].append(url)
        else:
            dct['URL'] = [url]

    def get_pub(self, rel, dst):
        """Get pubmed info given a relationship and a destination Node."""
        assert rel['stoichiometry'] == 1
        assert rel['order'] >= 0
        assert dst['schemaClass'] == 'LiteratureReference', dst
        dct = {f:dst[f] for f in self.ntlit._fields}
        title = self.rm_period(dst['title'])
        dct['displayName'] = self.rm_period(dst['displayName'])
        if dct['displayName'].lower() != title.lower():
            print("\nDISPLAY({})\nTITLE  ({})".format(dct['displayName'], title))
        return self.ntlit(**dct)

    def _get_go(self, name, dct, rel, dst):
        """Get Compartments in a pathway."""
        # 'displayName': 'nucleoplasm',
        # 'definition': 'That part of the nuclear content other than chromosomes or nucleolus',
        # 'accession': '0005654',
        # 'url':'http://www.ebi.ac.uk/ego/QuickGO?mode=display&entry=GO:0005654'}>
        assert rel['stoichiometry'] == 1
        assert dst['displayName'] == dst['name'], '{} {}'.format(dst['displayName'], dst['name'])
        assert dst['databaseName'] == 'GO'
        comp = self.ntgo(displayName=dst['displayName'], accession=dst['accession'])
        if name in dct:
            dct[name].append(comp)
        else:
            dct[name] = [comp]

    @staticmethod
    def _get_crossreference(dct, rel, dst):
        """Get pathway crossReference."""
        assert dst['databaseName'] == 'BioModels Database', dst
        assert dst['schemaClass'] == 'DatabaseIdentifier'
        assert rel['stoichiometry'] == 1
        if 'crossreference' not in dct:
            dct['crossreference'] = [dst['displayName']]
        else:
            dct['crossreference'].append(dst['displayName'])

    @staticmethod
    def _get_taxid(dct, rel, dst):
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
            print('TAXID', dct)

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
        if 'figure' not in dct:
            dct['figure'] = [fig[9:]]
        else:
            dct['figure'].append(dst[fig[9:]])

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
