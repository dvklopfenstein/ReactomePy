# Python interface to Neo4j

1) [**Install the Python package, neo4j**](#1-install-the-python-package-neo4j)
2) [**Connect to the neo4j server from a Python script**](#2-connect-to-the-neo4j-server-from-a-python-script)
3) [**Three Arguments:**](#three-arguments-graphdatabasedriverurl-authusername-password): **GraphDatabase.driver([_url_](), auth=([_username_](), [_password_]()))**

## 1) Install the Python package, neo4j
```
pip install neo4j
```

## 2) Connect to the neo4j server from a Python script
```
from neo4j import GraphDatabase

gdbdr = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', password))
```

### Three Arguments: GraphDatabase.driver(_url_, auth=(_username_, _password_))
#### 1. _url_: _Hover your mouse over the tab_ to see it. NOT the url seen in the [browser command-line]().   
#### 2. _username_: Neo4j username seen with the neo4j command:    
```
:server status
```
#### 3. _password_: can be set in Neo4j using:   
```
:server change-password
```
![driver args](images/python_neo4j_gdbdr.png)

### The URL is not the one seen in the browser command line

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
