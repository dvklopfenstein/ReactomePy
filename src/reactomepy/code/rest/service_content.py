"""For communicating with Reactome's REST Content Service."""

__copyright__ = "Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import requests


class ContentService(object):
    """Post identifiers to Reactome."""

    url = 'https://reactome.org/ContentService'

    # curl -X GET "https://reactome.org/ContentService/data/database/name" -H "accept: text/plain"
    def get_databasename(self):
        """Get the latest Reactome Knowledgebase version."""
        return str(self._str_database('name'))

    # curl -X GET "https://reactome.org/ContentService/data/database/version" -H "accept:text/plain"
    def get_version(self):
        """Get the latest Reactome Knowledgebase version."""
        txt = self._str_database('version')
        return int(txt) if txt.isdigit() else txt

    def _str_database(self, typ):
        """Get the latest Reactome Knowledgebase."""
        url = "{URL}/data/database/{TYPE}".format(URL=self.url, TYPE=typ)
        hdrs = {'accept': 'text/plain'}
        rsp = requests.get(url, headers=hdrs)
        if rsp.status_code == 200:
            return rsp.text
        return rsp


# Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved."
