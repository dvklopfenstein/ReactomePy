# Python interface to Neo4j

## Install the Python package, neo4j
```
pip install neo4j
```

## Connect to the neo4j server from a Python script
```
from neo4j import GraphDatabase

gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
```

### GraphDatabase.driver Arguments
The _url_ argument is tha value you see when you hover your mouse over the tab.    
The _user_ is the Neo4j username.
The _password_ can be set in Neo4j using:
```
:server change-password
```
![driver args](images/python_neo4j_gdbdr.png)

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
