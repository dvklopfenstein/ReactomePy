"""A handler for a Neo4j Session."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys
from reactomeneo4j.code.schema.hier import DataSchemaHier


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class Session(object):
    """A handler for a Neo4j Session."""

    def __init__(self, session):
        self.ses = session
        self.sch = DataSchemaHier()

    def run(self, query, prt=sys.stdout):
        """Query the neo4j database."""
        # BoltStatementResult:
        #   data          [{'pathway': <Node id=2052401 labels={'DatabaseObject', ...
        #   value values  [           [<Node id=2052401 labels={'DatabaseObject', ...
        #   attached consume detach graph keys peek records session single summary
        if prt is not None:
            prt.write('\nQUERY: {Q}\n'.format(Q=query))
        return self.ses.run(query)

    def prt_relationships(self, node='Complex{stId:"R-HSA-983126"}', prt=sys.stdout):
        """Get all relationships of an object. Ex: 'Complex{stId:"R-HSA-983126"}' """
        # 'MATCH (Complex{stId:"R-HSA-983126"})-[r]-() RETURN r'
        # <Relationship id=9938679
        #     nodes=(<Node id=2049818 labels=set() properties={}>,
        #            <Node id=2020241 labels=set() properties={}>)
        #     type='hasComponent'
        #     properties={'stoichiometry': 1, 'order': 0}
        # >
        qry = 'MATCH ({NODE})-[r]-() RETURN r'.format(NODE=node)
        res = self.ses.run(qry)
        for rec in res.records():
            rel = rec['r']
            print("ITEMS:", rel.items())
            print(rel)
            prt.write("TYPE({TYPE})\n".format(TYPE=rel.type))

    def get_node(self, neo4j_node_id):
        """Return nodes for neo4j IDs."""
        qry = 'START s=NODE({ID}) MATCH(s) RETURN s'.format(ID=neo4j_node_id)
        res = self.ses.run(qry)
        print('NNNNNNN', res.data())

#  begin_transaction(self, bookmark=None, metadata=None, timeout=None)
#      Create a new :class:`.Transaction` within this session.
#      Calling this method with a bookmark is equivalent to
#
#      :param bookmark: a bookmark to which the server should
#                       synchronise before beginning the transaction
#      :param metadata:
#      :param timeout:
#      :returns: new :class:`.Transaction` instance.
#      :raise: :class:`.TransactionError` if a transaction is already open
#
#  close(self)
#      Close the session. This will release any borrowed resources,
#      such as connections, and will roll back any outstanding transactions.
#
#  closed(self)              # Indicator for whether or not this session has been closed.
#      :returns: :const:`True` if closed, :const:`False` otherwise.
#
#  commit_transaction(self)  # Commit the current transaction.
#      :returns: the bookmark returned from the server, if any
#      :raise: :class:`.TransactionError` if no transaction is currently open
#
#  detach(self, result, sync=True)
#  Detach a result from this session by fetching and buffering any remaining records.
#      :param result:
#      :param sync:
#      :returns: number of records fetched
#
#  fetch(self)           # Attempt to fetch at least one more record.
#      :returns: number of records fetched
#
#  has_transaction(self)
#
#  last_bookmark(self)   # The bookmark returned by the last :class:`.Transaction`.
#
#  next_bookmarks(self)  # The set of bookmarks to be passed into the next
#      :class:`.Transaction`.
#
#  read_transaction(self, unit_of_work, *args, **kwargs)
#
#  rollback_transaction(self) Rollback the current transaction.
#
#      :raise: :class:`.TransactionError` if no transaction is currently open
#
#  run(self, statement, parameters=None, **kwparameters)
#      Run a Cypher statement within an auto-commit transaction.
#
#      The statement is sent and the result header received
#      immediately but the :class:`.StatementResult` content is
#      fetched lazily as consumed by the client application.
#
#      If a statement is executed before a previous
#      :class:`.StatementResult` in the same :class:`.Session` has
#      been fully consumed, the first result will be fully fetched
#      and buffered. Note therefore that the generally recommended
#      pattern of usage is to fully consume one result before
#      executing a subsequent statement. If two results need to be
#      consumed in parallel, multiple :class:`.Session` objects
#      can be used as an alternative to result buffering.
#
#      For more usage details, see :meth:`.Transaction.run`.
#
#      :param statement: template Cypher statement
#      :param parameters: dictionary of parameters
#      :param kwparameters: additional keyword parameters
#      :returns: :class:`.StatementResult` object
#
#  send(self) Send all outstanding requests.
#
#  sync(self) Carry out a full send and receive.
#      :returns: number of records fetched
#
# write_transaction(self, unit_of_work, *args, **kwargs)


# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
