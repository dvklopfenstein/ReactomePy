"""For communicating with Reactome's REST service."""
# TBD: Add pathway analysis options:
#   1) Project to human using ENSEMBL's Inferra database
#      Analyse the identifiers in the file over the different species and projects the result to Homo Sapiens
#      /identifiers/form/projection
#   2) include interactors from IntAct
#

from __future__ import print_function

__copyright__ = "Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import json
import pprint
import requests
import datetime

## **database**   Database info queries
#    GET /database/name The name of current database
#    GET /database/version The version number of current database

## **download**   Retrieve downloadable files in CSV format
#    1) Downloads those identifiers found for a given analysis and a certain resource
#       GET /download/{token}/entities/found/{resource}/{filename}.csv
#    2) Downloads a list of the not found identifiers
#       GET /download/{token}/entities/notfound/{filename}.csv
#    3) Downloads all hit pathways for a given analysis
#       GET /download/{token}/pathways/{resource}/{filename}.csv

## **identifier**   Queries for only one identifier
#    1) Analyse the identifier over the different species in the database
#       GET /identifier/{id}
#    2) Analyse the identifier over the different species in the database and projects the result to Homo Sapiens
#       GET /identifier/{id}/projection

## **identifiers**   Queries for multiple identifiers
#    1) Analyse the post identifiers over the different species
#       POST /identifiers/
#    2) Analyse the identifiers in the file over the different species
#       POST /identifiers/form
#    3) Analyse the identifiers in the file over the different species and projects the result to Homo Sapiens
#       POST /identifiers/form/projection
#    4) Analyse the post identifiers over the different species and projects the result to Homo Sapiens
#       POST /identifiers/projection
#    5) Analyse the identifiers contained in the provided url over the different species
#       POST /identifiers/url
#    6) Analyse the identifiers contained in the provided url over the different species and projects the result to Homo Sapiens
#       POST /identifiers/url/projection

## **mapping** Identifiers mapping methods
#    1) Maps the post identifiers over the different species
#       POST /mapping/
#    2) Maps the identifiers in the file over the different species
#       POST /mapping/form
#    3) Maps the identifiers in the file over the different species and projects the result to Homo Sapiens
#       POST /mapping/form/projection
#    4) Maps the post identifiers over the different species and projects the result to Homo Sapiens
#       POST /mapping/projection
#    5) Maps the identifiers contained in the provided url over the different species
#       POST /mapping/url
#    6) Maps the identifiers contained in the provided url over the different species and projects the result to Homo Sapiens
#       POST /mapping/url/projection

## **report** Retrieves report files in PDF format
#    1) Downloads a report for a given pathway analysis result
#       GET /report/{token}/{species}/{filename}.pdf

## **species** Species comparison
#    1) Compares Homo sapiens to the specified species
#       GET /species/homoSapiens/{species}

## **token** Previous queries filter
#    1) Returns the result associated with the token
#       GET /token/{token}
#    2) Returns the result for the pathway ids sent by post (when they are present in the original result)
#       POST /token/{token}/filter/pathways
#    3) Filters the result by species
#       GET /token/{token}/filter/species/{species}
#    4) Returns a summary of the contained identifiers and interactors for each requested pathway and a given token
#       POST /token/{token}/found/all
#    5) Returns a summary of the contained identifiers and interactors for a given pathway and token
#       GET /token/{token}/found/all/{pathway}
#    6) Returns a summary of the found curated identifiers for a given pathway and token
#       GET /token/{token}/found/entities/{pathway}
#    7) Returns a summary of the found interactors for a given pathway and token
#       GET /token/{token}/found/interactors/{pathway}
#    8) Returns a list of the identifiers not found for a given token
#       GET /token/{token}/notFound
#    9) Returns the page where the corresponding pathway is taking into account the passed parameters
#       GET /token/{token}/page/{pathway}
#    10) Returns a list of binned hit pathway sizes associated with the token
#       GET /token/{token}/pathways/binned
#    11) Returns the reaction ids of the pathway ids sent by post that are present in the original result
#       POST /token/{token}/reactions/pathways
#    12) Returns the reaction ids of the provided pathway id that are present in the original result
#       GET /token/{token}/reactions/{pathway}
#    13) Returns the resources summary associated with the token
#       GET /token/{token



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

    def __init__(self, fout_log_tokens):
        self.fout_log_tokens = fout_log_tokens

    #### def get_ids(self, fin_study_ids):
    ####     """Get study
    #### study_dct = read_ids(args['study_ids'])

    def get_token(self, ids, name=None, token=None):
        """Return a token associated with a Pathway enrichment analysis."""
        # If user provides no token, then run a Pathway enrichment analysis. Return token
        if token is None:
            return self._get_token(ids, name)
        return token

    def _get_token(self, data, sample_name):
        """Run a Pathway enrichment analysis. Return token"""
        rsp = self.post_ids(data, sample_name)
        # pylint: disable=superfluous-parens
        assert 'summary' in rsp, rsp
        token = rsp['summary']['token']
        self._prt_token(token, data, sample_name)
        return token

    def _prt_token(self, token, data, sample_name):
        """Print newly genrated token."""
        txt = 'TOKEN: {T}  # {DATE} {N:4} user items {NAME}'.format(
            T=token, N=len(data), NAME=sample_name,
            DATE=datetime.datetime.today().strftime("%a %b %d %H:%M:%S %Y"))
        print('  {TXT}'.format(TXT=txt))
        with open(self.fout_log_tokens, 'a') as log:
            log.write('{TOKEN}\n'.format(TOKEN=txt))
            print('  APPENDED: {LOG}'.format(LOG=self.fout_log_tokens))

    def post_ids(self, ids, sample_name=None):
        """POST: /identifiers/ Analyse the post identifiers over the different species."""
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
        print(rsp)
        print("\nHDRS", rsp.headers)
        print("\nURL", rsp.url)
        print(dir(rsp))
        return rsp

    @staticmethod
    def _wr(fout, rsp_data, mode):
        """Write response data to a file."""
        with open(fout, mode) as prt:
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
            self._wr(fout_pdf, rsp.content, 'wb')

    def csv_pathways(self, fout_csv, token, resource='TOTAL'):
        """result.csv w/web; Get the overrepresented pathway results."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/pathways/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/pathways/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resources
        url = url_pat.format(URL=self.url, TOKEN=token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text, 'w')
            return rsp.text
        return rsp

    def get_results(self, token, resource='TOTAL'):
        """result.csv w/web; Get the overrepresented pathway results."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/pathways/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/pathways/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resources
        url = url_pat.format(URL=self.url, TOKEN=token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        return rsp.json() if rsp.status_code == 200 else rsp

    def csv_found(self, fout_csv, token, resource='TOTAL'):
        """mapping.csv w/web; Get IDs which were found and their mapping."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/entities/found/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/entities/found/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resources
        url = url_pat.format(URL=self.url, TOKEN=token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text, 'w')
            return rsp.text

    def csv_notfound(self, fout_csv, token):
        """Report identifiers not found."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/entities/notfound/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/entities/notfound/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        url = url_pat.format(URL=self.url, TOKEN=token, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text, 'w')
            return rsp.text

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

    def get_version(self):
        """Compare version of Reactome online with version in this repo."""
        # curl -X GET "https://reactome.org/ContentService/data/database/version" -H  "accept: text/plain"
        url = "https://reactome.org/ContentService/data/database/version"
        hdrs = {'accept': 'text/plain'}
        rsp = requests.get(url, headers=hdrs)
        print(rsp)
        if rsp.status_code == 200:
            return rsp.text
        return rsp

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
