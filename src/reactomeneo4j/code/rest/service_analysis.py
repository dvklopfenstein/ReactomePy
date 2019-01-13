"""For communicating with Reactome's REST service."""

from __future__ import print_function

__copyright__ = "Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import json
import pprint
import requests


# pylint: disable=line-too-long
class AnalysisService(object):
    """Post identifiers to Reactome."""

    # url = 'https://reactome.org/AnalysisService/identifiers/\?pageSize\=1\&page\=1'
    # url = 'https://reactome.org/AnalysisService/identifiers/'
    url = 'https://reactome.org/AnalysisService'

    headers = {'Content-type': 'text/plain'}  # application/json'}

    diagram_profile = 'Modern'
    analysis_profile = 'Standard'
    fireworks_profile = 'Barium Lithium'

    resources = set([
        'TOTAL',
        'UNIPROT',
        'ENSEMBL',
        'CHEBI',
        'MIRBASE',
        'NCBI_PROTEIN',
        'EMBL',
        'COMPOUND'])

    def post_ids(self, ids, sample_name=None):
        """Data Submission, identifiers."""
        # curl -X POST "https://reactome.org/AnalysisService/identifiers/?interactors=false&sortBy=ENTITIES_PVALUE&order=ASC&resource=TOTAL" -H  "accept: application/json" -H  "content-type: text/plain" -d "# 1-1q21.3Q68E01P22532P31151P35321P05109Q9UBC9Q9BYE4Q99584P35326Q5K4L6Q96LB8P22528Q12905Q9HCY8Q96FQ6P80511Q9Y3Y2P16066P33763P33764P35325P23297P29034P06703P06702P23490Q96LB9Q96PI1Q5T871Q5T870Q96RM1P22531O95295P26447Q86SG5"
        # https://curl.trillworks.com/  curl-to-requests

        #    {u'expression': {u'columnNames': []},
        #     u'identifiersNotFound': 12,
        #     u'pathways': [{u'dbId': 6809371,

        #            {u'dbId': 6805567,
        #             u'entities': {u'exp': [],
        #                           u'fdr': 3.106759294269068e-10,
        #                           u'found': 11,
        #                           u'pValue': 8.876455126483052e-12,
        #                           u'ratio': 0.016295334919604873,
        #                           u'resource': u'TOTAL',
        #                           u'total': 226},
        #             u'llp': True,
        #             u'name': u'Keratinization',
        #             u'reactions': {u'found': 6,
        #                            u'ratio': 0.002920209567980761,
        #                            u'resource': u'TOTAL',
        #                            u'total': 34},
        #             u'species': {u'dbId': 48887,
        #                          u'name': u'Homo sapiens',
        #                          u'taxId': u'9606'},
        #             u'stId': u'R-HSA-6805567'},

        #     u'pathwaysFound': 56,
        #     u'resourceSummary': [{u'pathways': 56, u'resource': u'TOTAL'},
        #                          {u'pathways': 56, u'resource': u'UNIPROT'}],
        #     u'summary': {u'interactors': False,
        #                  u'projection': False,
        #                  u'sampleName': u'',
        #                  u'text': True,
        #                  u'token': u'MjAxODA4MjAxNTU0MjBfNzM2MA%3D%3D',
        #                  u'type': u'OVERREPRESENTATION'},
        #     u'warnings': [u'Missing header. Using a default one.']}

        # params = (
        #     ('interactors', 'false'),
        #     ('sortBy', 'ENTITIES_PVALUE'),
        #     ('order', 'ASC'),
        #     ('resource', 'TOTAL'),
        # )

        # Format data
        str_ids = "\n".join(str(g) for g in ids)
        if sample_name is not None:
            str_ids = "\n".join([sample_name, str_ids])
        data = '"{DATA}"'.format(DATA=str_ids)
        # print(data)
        # Other fields
        url = '{URL}/identifiers/'.format(URL=self.url)
        hdrs = { # 'accept':'application/json',
            'Content-type':'text/plain'}
        # POST and received response
        rsp = requests.post(url, data=data, headers=hdrs)  # , params=params)
        if rsp.status_code == 200:
            rsp_json = rsp.json()
            # pprint.pprint(rsp_json)
            return rsp_json
        print("FAILED POST: {CODE} {REASON}".format(CODE=rsp.status_code, REASON=rsp.reason))
        print(rsp.text)
        print("\nHDRS", rsp.headers)
        print("\nURL", rsp.url)
        print(dir(rsp))
        return rsp

    @staticmethod
    def _wr(fout, rsp_data):
        """Write response data to a file."""
        with open(fout, 'w') as prt:
            prt.write(rsp_data)  # content for a binary (pdf) file
            print("  WROTE: {FILE}".format(FILE=fout))

    def pdf_report(self, fout_pdf, token):
        """report.pdf w/web; Get the full report on the pathways found overrepresented."""
        url_pat = "{URL}/report/{TOKEN}/Homo%20sapiens/report.pdf"
        hdrs = {'accept': 'application/pdf'}
        params = (
            ('number', '25'),
            ('resource', 'TOTAL'),
            ('diagramProfile', 'Modern'),
            ('analysisProfile', 'Standard'),
            ('fireworksProfile', 'Copper'),  # 'Copper', 'Copper plus', 'Barium Lithium', 'Calcium Salts'
        )
        # curl -X GET "https://reactome.org/AnalysisService/report/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/Homo%20sapiens/report.pdf?number=25&resource=TOTAL&diagramProfile=Modern&analysisProfile=Standard&fireworksProfile=Barium%20Lithium" -H "accept: application/pdf" --output curl_report.pdf
        url = url_pat.format(URL=self.url, TOKEN=token, PDF=fout_pdf)
        # params = {'output':fout_pdf}
        rsp = requests.get(url, headers=hdrs, params=params)
        if rsp.status_code == 200:
            self._wr(fout_pdf, rsp.content)

    def csv_pathways(self, fout_csv, token, resource='TOTAL'):
        """result.csv w/web; Get the overrepresented pathway results."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/pathways/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/pathways/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resources
        url = url_pat.format(URL=self.url, TOKEN=token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text)

    def get_results(self, token, resource='TOTAL'):
        """result.csv w/web; Get the overrepresented pathway results."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/pathways/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/pathways/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resources
        url = url_pat.format(URL=self.url, TOKEN=token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        return rsp
        # if rsp.status_code == 200:
        #     self._wr(fout_csv, rsp.text)

    def csv_found(self, fout_csv, token, resource='TOTAL'):
        """mapping.csv w/web; Get IDs which were found and their mapping."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/entities/found/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/entities/found/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resources
        url = url_pat.format(URL=self.url, TOKEN=token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text)

    def csv_notfound(self, fout_csv, token):
        """Report identifiers not found."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/entities/notfound/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/entities/notfound/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        url = url_pat.format(URL=self.url, TOKEN=token, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text)

    def get_notfound(self, token):
        """Report identifiers not found."""
        # curl -X GET "https://reactome.org/AnalysisService/token/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/notFound?pageSize=40&page=1" -H  "accept: application/json"
        url_pat = "{URL}/token/{TOKEN}/notFound"  # ?pageSize=40&page=1
        hdrs = {'accept': 'application/json'}
        url = url_pat.format(URL=self.url, TOKEN=token)
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            print(rsp)
            data = rsp.json()
            pprint.pprint(data)
            return data

# # token = 'MjAxODA4MTMxNjIzMTRfNDcwNw%3D%3D'
# GET "/token/{token}/page/{pathway}".format(pathway="R-HSA-6809371")  # Get page number
# 1
#
# # Get reaction identifiers R-HSA-NNN...
# GET "/token/{token}/reactions/{pathway}".format(pathway="R-HSA-6809371")
# [
#   6814387,
#   6811539,
#   6814734,
#   6814764,
#   6814298,
#   6810937
# ]
#
#
# GET /token/{token}/resources
# [
#   {
#     "resource": "TOTAL",
#     "pathways": 213
#   },
#   {
#     "resource": "UNIPROT",
#     "pathways": 213
#   }
# ]

# Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
