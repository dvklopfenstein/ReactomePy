"""Manage data in schemaClass, Pathway."""

__copyright__ = "Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

#from datetime import date
import sys
from neo4jrestclient.client import GraphDatabase as GdbRestIf
from neo4jrestclient import client

# pylint: disable=too-few-public-methods,too-many-instance-attributes
class GraphDatabase(object):
    """Manage data in schemaClass, Pathway."""

    def __init__(self, url='http://localhost:7474', username='neo4j', password='neo4j'):
        self.gdb = GdbRestIf(url, username, password)  # neo4jrestclient.client.GraphDatabase

    def get_query_node(self, query, prt=sys.stdout):
        """Given a Neo4j Cypher query, return a Reactome node."""
        results = self.gdb.query(query, returns=(client.Node))
        if prt is not None:
            prt.write('{QRY}\n'.format(QRY=query))
        assert results
        return results[0][0]

    # def __str__(self):
    #     return "PW {ID:9} {DATE} {NAME}".format(
    #         ID=self.st_id, DATE=self.release_date, NAME=self.display_name)


# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
