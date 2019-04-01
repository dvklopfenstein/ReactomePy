"""Manage a token."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# import os
# import sys
import requests
from reactomepy.data.species import SPECIES

## **download**   Retrieve downloadable files in CSV format
#    1) Downloads those identifiers found for a given analysis and a certain resource
#       GET /download/{token}/entities/found/{resource}/{filename}.csv
#    2) Downloads a list of the not found identifiers
#       GET /download/{token}/entities/notfound/{filename}.csv
#    3) Downloads all hit pathways for a given analysis
#       GET /download/{token}/pathways/{resource}/{filename}.csv

## **report** Retrieves report files in PDF format
#    1) Downloads a report for a given pathway analysis result
#       GET /report/{token}/{species}/{filename}.pdf

## **token** Previous queries filter
#    1) Returns the result associated with the token
#       GET /token/{token}
#    2) Returns the result for the pathway IDs sent by post (when present in the original result)
#       POST /token/{token}/filter/pathways
#    3) Filters the result by species
#       GET /token/{token}/filter/species/{species}
#    4) Get summary of the contained IDs and interactors for each requested pathway & provided token
#       POST /token/{token}/found/all
#    5) Returns a summary of the contained identifiers and interactors for a given pathway and token
#       GET /token/{token}/found/all/{pathway}
#    6) Returns a summary of the found curated identifiers for a given pathway and token
#       GET /token/{token}/found/entities/{pathway}
#    7) Returns a summary of the found interactors for a given pathway and token
#       GET /token/{token}/found/interactors/{pathway}
#    8) Returns a list of the identifiers not found for a given token
# -Y-   GET /token/{token}/notFound
#    9) Get page where the corresponding pathway is taking into account the passed parameters
#       GET /token/{token}/page/{pathway}
#    10) Returns a list of binned hit pathway sizes associated with the token
#       GET /token/{token}/pathways/binned
#    11) Gets reaction IDs of the pathway IDs sent by post that are present in the original result
#       POST /token/{token}/reactions/pathways
#    12) Returns the reaction ids of the provided pathway id that are present in the original result
#       GET /token/{token}/reactions/{pathway}
#    13) Returns the resources summary associated with the token
# -Y-   GET /token/{token}/resources

# pylint: disable=line-too-long
class TokenManager:
    """Manage a token."""

    url_ana = 'https://reactome.org/AnalysisService'

    species_names = {nt.displayName for nt in SPECIES}

    resource_names = set([
        'TOTAL',
        'UNIPROT',
        'ENSEMBL',
        'CHEBI',
        'MIRBASE',
        'NCBI_PROTEIN',
        'EMBL',
        'COMPOUND'])


    def __init__(self, token):
        self.token = token
        self.resources = self._init_resources()

    def get_results(self, resource='TOTAL'):
        """result.csv w/web; Get the overrepresented pathway results."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/pathways/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/pathways/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resource_names
        url = url_pat.format(URL=self.url_ana, TOKEN=self.token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        return rsp.json() if rsp.status_code == 200 else rsp

    def pdf_report(self, fout_pdf, species='Homo sapiens'):
        """report.pdf w/web; Get the full report on the pathways found overrepresented."""
        url_pat = "{URL}/report/{TOKEN}/{SPECIES}/report.pdf"
        self._chk_species(species)
        hdrs = {'accept': 'application/pdf'}
        params = (
            ('number', '25'),
            ('resource', 'TOTAL'),
            ('diagramProfile', 'Modern'),
            ('analysisProfile', 'Standard'),
            ('fireworksProfile', 'Copper'),  # Copper, Copper plus, Barium Lithium, Calcium Salts
        )
        # curl -X GET "https://reactome.org/AnalysisService/report/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/Homo%20sapiens/report.pdf?number=25&resource=TOTAL&diagramProfile=Modern&analysisProfile=Standard&fireworksProfile=Barium%20Lithium" -H "accept: application/pdf" --output curl_report.pdf
        url = url_pat.format(URL=self.url_ana, TOKEN=self.token, SPECIES=species.replace(' ', '%20'))
        # params = {'output':fout_pdf}
        rsp = requests.get(url, headers=hdrs, params=params)
        if rsp.status_code == 200:
            self._wr(fout_pdf, rsp.content, 'wb')

    def _chk_species(self, species):
        """Check that the species is found in Reactome."""
        if species in self.species_names:
            return
        print('NO SPECIES FOUND IN REACTOME: {SPECIES}'.format(SPECIES=species))
        for ntd in SPECIES:
            print(ntd.displayName)

    def csv_pathways(self, fout_csv, resource='TOTAL'):
        """result.csv w/web; Get the overrepresented pathway results."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/pathways/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/pathways/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resource_names, resource
        url = url_pat.format(URL=self.url_ana, TOKEN=self.token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        # print('PATHWAYS', dir(rsp))
        # print('PATHWAYS', rsp.headers)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text, 'w')
            return rsp.text
        return rsp

    def csv_notfound(self, fout_csv):
        """Report identifiers not found."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/entities/notfound/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/entities/notfound/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        url = url_pat.format(URL=self.url_ana, TOKEN=self.token, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            # print('IDS NOT FOUND', dir(rsp))
            # print(rsp.text)
            self._wr(fout_csv, rsp.text, 'w')
            return rsp.text

    def get_notfound(self):
        """Report identifiers not found."""
        # curl -X GET "https://reactome.org/AnalysisService/token/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/notFound?pageSize=40&page=1" -H  "accept: application/json"
        url_pat = "{URL}/token/{TOKEN}/notFound"  # ?pageSize=40&page=1
        hdrs = {'accept': 'application/json'}
        url = url_pat.format(URL=self.url_ana, TOKEN=self.token)
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            # print('RRRRRR', rsp)
            data = rsp.json()
            # pprint.pprint(data)
            return data

    @staticmethod
    def _wr(fout, rsp_data, mode):
        """Write response data to a file."""
        # attr = 'text' if mode == 'w' else 'content'
        #print('DDDDDDDDDDDDDDDDDDDDDDDDDD({})'.format(rsp_data))
        # rsp_data = getattr(rsp, attr)
        with open(fout, mode) as prt:
            prt.write(rsp_data)  # content for a binary (pdf) file
            print("  WROTE: {FILE}".format(FILE=fout))

    def csv_found(self, fout_csv, resource='TOTAL'):
        """mapping.csv w/web; Get IDs which were found and their mapping."""
        # curl -X GET "https://reactome.org/AnalysisService/download/MjAxODA4MTMxNjIzMTRfNDcwNw%253D%253D/entities/found/TOTAL/result.csv" -H  "accept: text/csv"
        url_pat = "{URL}/download/{TOKEN}/entities/found/{RESOURCE}/{FILENAME}.csv"
        hdrs = {'accept': 'text/csv'}
        assert resource in self.resource_names
        url = url_pat.format(URL=self.url_ana, TOKEN=self.token, RESOURCE=resource, FILENAME='result')
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            self._wr(fout_csv, rsp.text, 'w')
            return rsp.text

    def _init_resources(self):
        """Get the counts of pathways found for each type of resource (eg TOTAL UNIPROT)"""
        url_pat = "{URL}/token/{TOKEN}/resources"
        hdrs = {'accept': 'application/json'}
        url = url_pat.format(URL=self.url_ana, TOKEN=self.token)
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            return rsp.json()


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
