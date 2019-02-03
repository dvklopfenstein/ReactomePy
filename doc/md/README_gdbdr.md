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

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
