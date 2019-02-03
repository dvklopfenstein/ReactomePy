# Python interface to Neo4j

1) [**Install the Python package, neo4j**](#install-the-python-package-neo4j)
2) [**Connect to the neo4j server from a Python script**](#connect-to-the-neo4j-server-from-a-python-script)
3) [**Three Graphdatabase.driver Arguments:**]()
3) [**Three Arguments](): GraphDatabase.driver(_url_, auth=(_username_, _password_))**]

## Install the Python package, neo4j
```
pip install neo4j
```

## Connect to the neo4j server from a Python script
```
from neo4j import GraphDatabase

gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
```

### Three Arguments: GraphDatabase.driver(_url_, auth=(_username_, _password_))
#### 1. The _url_ argument is tha value you see when you hover your mouse over the tab.    
#### 2. The _user_ is the Neo4j username seen with the neo4j command:    
```
:server status
```
#### 3. The _password_ can be set in Neo4j using:   
```
:server change-password
```
![driver args](images/python_neo4j_gdbdr.png)

### The URL is not the one seen in the browser command line

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
