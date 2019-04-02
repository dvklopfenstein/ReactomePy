"""For communicating with Reactome's REST service."""
# TBD: Add pathway analysis options:
#   1) Project to human using ENSEMBL's Inferra database
#      Analyse the identifiers in the file over the different species and projects the result to Homo Sapiens
#      /identifiers/form/projection
#   2) include interactors from IntAct
#

from __future__ import print_function

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import os
import sys
import re
# import json
# import pprint
import datetime
import requests


## **identifier**   Queries for only one identifier
#    1) Analyse the identifier over the different species in the database
#       GET /identifier/{id}
#    2) Analyse ID over the different species and projects the result to Homo Sapiens
#       GET /identifier/{id}/projection

## **identifiers**   Queries for multiple identifiers
#    1) Analyse the post identifiers over the different species
#       POST /identifiers/
#    2) Analyse the identifiers in the file over the different species
# -Y-   POST /identifiers/form
#    3) Analyse IDs in the file over the different species and projects to Homo Sapiens
# -Y-   POST /identifiers/form/projection
#    4) Analyse the post identifiers over the different species and projects to Homo Sapiens
#       POST /identifiers/projection
#    5) Analyse the identifiers contained in the provided url over the different species
#       POST /identifiers/url
#    6) Analyse IDs from the provided url over the different species and projects to Homo Sapiens
#       POST /identifiers/url/projection

## **mapping** Identifiers mapping methods
#    1) Maps the post identifiers over the different species
#       POST /mapping/
#    2) Maps the identifiers in the file over the different species
#       POST /mapping/form
#    3) Maps IDs in the file over the different species and projects to Homo Sapiens
#       POST /mapping/form/projection
#    4) Maps the post identifiers over the different species and projects to Homo Sapiens
#       POST /mapping/projection
#    5) Maps the identifiers contained in the provided url over the different species
#       POST /mapping/url
#    6) Maps IDs contained from url over the different species and projects to Homo Sapiens
#       POST /mapping/url/projection

## **species** Species comparison
#    1) Compares Homo sapiens to the specified species
#       GET /species/homoSapiens/{species}


# pylint: disable=line-too-long
class AnalysisService:
    """Post identifiers to Reactome."""

    url = 'https://reactome.org/AnalysisService'

    diagram_profile = 'Modern'
    analysis_profile = 'Standard'
    fireworks_profile = 'Barium Lithium'

    resources = set([
        'TOTAL',
        'UNIPROT',
        'ENSEMBL',
        'CHEBI',
        'IUPHAR',
        'MIRBASE',
        'NCBI_PROTEIN',
        'EMBL',
        'COMPOUND',
        'PUBCHEM_COMPOUND',
    ])

    sortby = set([
        'NAME',
        'TOTAL_ENTITIES',
        'TOTAL_INTERACTORS',
        'TOTAL_REACTIONS',
        'FOUND_ENTITIES',
        'FOUND_INTERACTORS',
        'FOUND_REACTIONS',
        'ENTITIES_RATIO',
        'ENTITIES_PVALUE',
        'ENTITIES_FDR',
        'REACTIONS_RATIO',
    ])

    order = set(['ASC', 'DESC'])

    def __init__(self, fout_log_tokens='tokens.log'):
        self.fout_log_tokens = fout_log_tokens

    def get_token(self, ids=None, token=None, to_hsa=True, **kws):
        """Return a token associated with a Pathway enrichment analysis."""
        # If user provides no token, then run a Pathway enrichment analysis. Return token
        if token is None:
            assert ids is not None, 'FATAL IDS({IDs})'.format(IDs=ids)
            if os.path.exists(ids):
                if to_hsa:
                    return self._get_token(ids, self.post_ids_form_project, **kws)
                else:
                    return self._get_token(ids, self.post_ids_form, **kws)
            else:
                raise RuntimeError('CANNOT READ STUDY ID FILE: {F}'.format(F=ids))
        assert token is not None, 'FATAL TOKEN({IDs})'.format(IDs=token)
        return token

    def _get_token(self, data, post_fnc, **kws):
        """Run a Pathway enrichment analysis. Return token"""
        rsp_raw = post_fnc(data, **kws)
        rsp_json = rsp_raw.json()
        # pylint: disable=superfluous-parens
        assert 'summary' in rsp_json, rsp_json
        token = rsp_json['summary']['token']
        self._prt_token(rsp_raw, rsp_json, data)
        return token

    def _prt_token(self, rsp_raw, rsp_json, data):
        """Print newly generated token."""
        # pprint.pprint(rsp_json)
        token = rsp_json['summary']['token']
        sample_name = rsp_json['summary']['sampleName']
        txt = 'TOKEN: {T}  # {DATE} {N:4} user items {NAME}'.format(
            T=token, N=len(data), NAME=sample_name,
            DATE=datetime.datetime.today().strftime("%a %b %d %H:%M:%S %Y"))
        print('  {TXT}'.format(TXT=txt))
        print('  URL: {URL}'.format(URL=rsp_raw.url))
        with open(self.fout_log_tokens, 'a') as log:
            log.write('{TOKEN}\n'.format(TOKEN=txt))
            log.write("URL: {URL}\n".format(URL=rsp_raw.url))
            # Summary
            log.write('SUMMARY:\n')
            for param, val in rsp_json['summary'].items():
                log.write('  {K:11} = {V}\n'.format(K=param, V=val))
            # Headers
            log.write('HEADERS:\n')
            for param, val in rsp_raw.headers.items():
                log.write('  {K:12} = {V}\n'.format(K=param, V=val))
            # Number of IDs and Pathways found
            log.write('FOUND:\n')
            log.write('{N:4} study IDs not found\n'.format(N=rsp_json['identifiersNotFound']))
            log.write('{N:4} pathways found for study IDs\n'.format(N=rsp_json['pathwaysFound']))
            # Expression column names
            colnames = rsp_json['expression']['columnNames']
            if colnames:
                log.write('EXPRESSION COLUMN NAMES:\n')
                for idx, name in enumerate(colnames):
                    log.write('{I:3}) {COL}\n'.format(I=idx, COL=name))
            log.write('{LINE}\n'.format(LINE=self._get_desc_oneline(rsp_raw, rsp_json)))
            print('{LINE}\n'.format(LINE=self._get_desc_oneline(rsp_raw, rsp_json)))
            log.write('\n')
            print('  APPENDED: {LOG}'.format(LOG=self.fout_log_tokens))

    @staticmethod
    def _get_desc_oneline(rsp_raw, rsp_json):
        """Get one-liner describing simulation."""
        mtch = re.search(r'(includeDisease=(true|false))', str(rsp_raw.url))
        disease = mtch.group(1) if mtch else 'NO_DISEASE'
        return '{PWY:4} pwys, {M:3} IDs not found: projection={PROJ:1} interactors={INT:1} {DIS}'.format(
            PWY=rsp_json['pathwaysFound'],
            M=rsp_json['identifiersNotFound'],
            PROJ=rsp_json['summary']['projection'],
            INT=rsp_json['summary']['interactors'],
            DIS=disease)

    def post_ids_form_project(self, fin_ids, **kws):
        """POST: /identifiers/ Analyse the post identifiers over the different species."""
        return self.post_ids_form(fin_ids, True, **kws)

    def post_ids_form(self, fin_ids, to_hsa=False, **kws):
        """POST: /identifiers/ Analyse the post identifiers over the different species."""
        files = {
            'file': (fin_ids, open(fin_ids, 'rb'), 'text/plain'),
        }
        # /identifiers/form or /identifiers/form/projection
        cmd = 'identifiers/form/projection' if to_hsa else 'identifiers/form'
        url = '{URL}/{CMD}'.format(URL=self.url, CMD=cmd)
        # hdrs = { 'accept':'application/json', 'Content-type':'multipart/form-data'}
        # POST and received response
        # print('HEADERS:', hdrs)
        params = self.get_params_ea(kws)
        rsp = requests.post(url, files=files, params=params)
        if rsp.status_code == 200:
            return rsp
        self.prt_rsp_info(rsp, prt=sys.stdout)
        return rsp

    def get_params_ea(self, kws):
        """Get parameters for enrichment analysis"""
        params = {
            'interactors': 'false',
            'pageSize': 20,
            'page': 1,
            'sortBy': 'ENTITIES_PVALUE',
            'order': 'ASC',
            'resource': 'TOTAL',
            'pValue': 1,
            'includeDisease': 'true',
        }
        for key in set(['interactors', 'includeDisease']).intersection(kws):
            params[key] = str(kws[key]).lower()
        if 'resource' in kws:
            self._set_param(params, 'resource', kws['resource'], self.resources)
        if 'sortBy' in kws:
            self._set_param(params, 'sortBy', kws['sortBy'], self.sortby)
        if 'order' in kws:
            self._set_param(params, 'order', kws['order'], self.order)
        if 'pValue' in kws:
            params['pValue'] = kws['pValue']
        # print('KWWWWW:', kws)
        # print('PARAMS:', params)
        return params

    def _set_param(self, params,  key, val, expected):
        """Set parameter and check for expected results."""
        self._chk_option(key, val, expected)
        params[key] = val

    @staticmethod
    def prt_rsp_info(rsp, prt=sys.stdout):
        """Print response information."""
        prt.write("POST CODE: {CODE}({REASON})\n".format(CODE=rsp.status_code, REASON=rsp.reason))
        prt.write('RSP:  {RSP}\n'.format(RSP=rsp))
        prt.write("HDRS: {HDRS}\n".format(HDRS=rsp.headers))
        prt.write("URL:  {URL}\n".format(URL=rsp.url))
        prt.write("DIRS: {DIRS}\n".format(DIRS=dir(rsp)))
        if rsp.status_code != 200:
            prt.write("TEXT: {TEXT}\n".format(TEXT=rsp.text))

    def _chk_option(self, key, val, expected_values):
        """Check the option value."""
        if val in expected_values:
            return
        msg = '**FATAL: UNEXPECTED VALUE({V}) FOUND FOR {K}.'.format(V=val, K=key)
        print('{MSG} EXPECTED VALUES ARE:'.format(MSG=msg))
        for exp in sorted(expected_values):
            print('    {EXP}'.format(EXP=exp))
        raise RuntimeError(msg)



# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
