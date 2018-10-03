"""Node functions."""

__copyright__ = "Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

import sys


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class BoltStatementResult(object):
    """A handler for the result of Cypher statement execution."""

    def __init__(self, bolt_statement_result):
        self.res = bolt_statement_result

# class BoltStatementResult(StatementResult)
#  |  A handler for the result of Cypher statement execution.
#  |
#  |  Method resolution order:
#  |      BoltStatementResult
#  |      StatementResult
#  |      builtins.object
#  |
#  |  Methods defined here:
#  |
#  |  __init__(self, session, hydrant, metadata)
#  |      Initialize self.  See help(type(self)) for accurate signature.
#  |
#  |  data(self, *items)
#  |      Return the remainder of the result as a list of dictionaries.
#  |
#  |      :param items: fields to return for each remaining record
#  |      :returns: list of dictionaries
#  |
#  |  value(self, item=0, default=None)
#  |      Return the remainder of the result as a list of values.
#  |
#  |      :param item: field to return for each remaining record
#  |      :param default: default value, used if the index of key is unavailable
#  |      :returns: list of individual values
#  |
#  |  values(self, *items)
#  |      Return the remainder of the result as a list of tuples.
#  |
#  |      :param items: fields to return for each remaining record
#  |      :returns: list of value tuples
#  |
#  |  ----------------------------------------------------------------------
#  |  Methods inherited from StatementResult:
#  |
#  |  __iter__(self)
#  |
#  |  attached(self)
#  |      Indicator for whether or not this result is still attached to
#  |      a :class:`.Session`.
#  |
#  |      :returns: :const:`True` if still attached, :const:`False` otherwise
#  |
#  |  consume(self)
#  |      Consume the remainder of this result and return the summary.
#  |
#  |      :returns: The :class:`.ResultSummary` for this result
#  |
#  |  detach(self, sync=True)
#  |      Detach this result from its parent session by fetching the
#  |      remainder of this result from the network into the buffer.
#  |
#  |      :returns: number of records fetched
#  |
#  |  graph(self)
#  |      Return a Graph instance containing all the graph objects
#  |      in the result. After calling this method, the result becomes
#  |      detached, buffering all remaining records.
#  |
#  |      :returns: result graph
#  |
#  |  keys(self)
#  |      The keys for the records in this result.
#  |
#  |      :returns: tuple of key names
#  |
#  |  peek(self)
#  |      Obtain the next record from this result without consuming it.
#  |      This leaves the record in the buffer for further processing.
#  |
#  |      :returns: the next :class:`.Record` or :const:`None` if none remain
#  |
#  |  records(self)
#  |      Generator for records obtained from this result.
#  |
#  |      :yields: iterable of :class:`.Record` objects
#  |
#  |  single(self)
#  |      Obtain the next and only remaining record from this result.
#  |
#  |      A warning is generated if more than one record is available but
#  |      the first of these is still returned.
#  |
#  |      :returns: the next :class:`.Record` or :const:`None` if none remain
#  |      :warns: if more than one record is available
#  |
#  |  summary(self)
#  |      Obtain the summary of this result, buffering any remaining records.
#  |
#  |      :returns: The :class:`.ResultSummary` for this result
#  |
#  |  ----------------------------------------------------------------------
#  |  Data descriptors inherited from StatementResult:
#  |
#  |  __dict__
#  |      dictionary for instance variables (if defined)
#  |
#  |  __weakref__
#  |      list of weak references to the object (if defined)
#  |
#  |  session

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
