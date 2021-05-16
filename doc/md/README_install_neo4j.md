# Neo4j Download Hints
Please see [**Reactome's official documentation**](https://reactome.org/dev/graph-database#GetStarted)
regarding installing Neo4j.

See below for user hints ...


## Hints for installing Neo4j
* [**Download the _Neo4j Community Server Edition_**](#download-the-neo4j-community-server-edition)
* [**Download Java, if needed**](#download-java-if-needed)
* [**Download the Reactome Knowledegebase and connect it to Neo4j**](README_download_hints.md)


## Hints for installing Neo4j (details)
Reactome v76 would not connect to Python using the latest Neo4j, 4.2.6.    
An older version of Neo4j, 4.1.9, works great.

This mixture of versions worked with Reactome v76:
```
export JAVA_VER=jdk-11.0.11
export NEO4J_CONF=/home/neo4j/neo4j/neo4j-community-4.1.9/conf
export NEO4J_HOME=/home/neo4j/neo4j/neo4j-community-4.1.9
```
This version of the `neo4j` Python package worked:
```
$ python3 -c "import neo4j; print(neo4j.__version__)"
4.2.1
```

### Download the [_Neo4j Community Server Edition_](https://neo4j.com/download-center/#releases)
https://neo4j.com/download-center/#releases
![Neo4j Community Server](/doc/md/images/Neo4j_CommunityServer.png)

### Download Java, if needed
Download the Java Design Kit from Oracle:    
https://www.oracle.com/technetwork/java/javase/downloads/index.html     
![JDK Download](/doc/md/images/java_jdk_download.png)

Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
