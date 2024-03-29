# Reactome Download Hints
See [**Reactome's official documentation**](https://reactome.org/dev/graph-database#GetStarted)
regarding downloading the Reactome Knowledgebase.

See below for unofficial user hints ...

## Hints for downloading the Reactome Knowledgebase
1. [**Download the Reactome database**](#1-download-the-reactome-database)
2. [**Uncompress and extract the database**](#2-uncompress-and-extract-the-reactome-database-in-neo4j-format)
3. [**Ensure the graph.db directory does not exist in the Neo4j directory structure**](#3-ensure-the-graphdb-directory-does-not-exist-in-the-neo4j-directory-structure)
4. [**Moved the Reactome database to the Neo4j graph.db directory**](#4-moved-the-reactome-database-to-the-graphdb-directory)
5. [**Start the neo4j server on the new Reactome Knowledgebase**](#5-start-the-neo4j-server-on-the-new-reactome-knowledgebase)
6. [**View the Reactome database in the neo4j browser**]()
7. [**Python interface to neo4j**](README_gdbdr.md):    
  7.1) [**Install the Python package, neo4j**](README_gdbdr.md##1-install-the-python-package-neo4j)    
  7.2) [**Connect to the neo4j server from a Python script**](README_gdbdr.md#2-connect-to-the-neo4j-server-from-a-python-script)    


## Hints for downloading the Reactome Knowledgebase (details)
### 1. Download the Reactome database
Download from **https://reactome.org/dev/graph-database** or
`wget https://reactome.org/download/current/reactome.graphdb.tgz`
![download](images/download.png)

### 2. Uncompress and extract the Reactome database in Neo4j format
```
$ tar -xzvf reactome.graphdb.tgz
    reactome.graphdb.v67/
    reactome.graphdb.v67/neostore.labeltokenstore.db.names.id
    reactome.graphdb.v67/neostore.nodestore.db.id
    reactome.graphdb.v67/neostore.propertystore.db.index.id
    reactome.graphdb.v67/neostore.relationshipstore.db.id
    reactome.graphdb.v67/neostore.counts.db.a
    reactome.graphdb.v67/neostore.propertystore.db.strings
    ...
```

### 3. Ensure the graph.db directory does not exist in the Neo4j directory structure

Does the graph.db directory exist?    
No? Go to step 4.    

```
$ cd ~/neo4j/neo4j-community-4.1.9/data/databases/
$ ls graph.db
    ls: cannot access 'graph.db': No such file or directory
```

Yes? Move it out of the way:
```
$ ls graph.db
    debug.log                             neostore.nodestore.db.labels             neostore.relationshipgroupstore.db.id
    index                                 neostore.nodestore.db.labels.id          neostore.relationshipstore.db
    neostore                              neostore.propertystore.db                neostore.relationshipstore.db.id
    ...
$ mv graph.db graph.db.v66
$ ls graph.db
    ls: cannot access 'graph.db': No such file or directory
```

### 4. Moved the Reactome database to the graph.db directory
```
$ mv reactome.graphdb.v67 ~/neo4j/neo4j-community-4.1.9/data/databases/graph.db

# Confirm it is moved
$ cd ~/neo4j/neo4j-community-4.1.9/data/databases/graph.db
$ ls graph.db
    debug.log                             neostore.nodestore.db.labels             neostore.relationshipgroupstore.db.id
    index                                 neostore.nodestore.db.labels.id          neostore.relationshipstore.db
    neostore                              neostore.propertystore.db                neostore.relationshipstore.db.id
    ...
```

### 5. Start the neo4j server on the new Reactome Knowledgebase
[Where to look if it does not work](#where-to-look-if-it-does-not-work)

```
$ neo4j/neo4j-community-4.1.9/bin/neo4j start
    Active database: graph.db
    Directories in use:
      home:         /home/neo4j/neo4j/neo4j-community-4.1.9
      config:       /home/neo4j/neo4j/neo4j-community-4.1.9/conf/
      logs:         /home/neo4j/neo4j/neo4j-community-4.1.9/logs
      plugins:      /home/neo4j/neo4j/neo4j-community-4.1.9/plugins
      import:       /home/neo4j/neo4j/neo4j-community-4.1.9/import
      data:         /home/neo4j/neo4j/neo4j-community-4.1.9/data
      certificates: /home/neo4j/neo4j/neo4j-community-4.1.9/certificates
      run:          /home/neo4j/neo4j/neo4j-community-4.1.9/run
    Starting Neo4j.
    WARNING: Max 1024 open files allowed, minimum of 40000 recommended. See the Neo4j manual.
    Started neo4j (pid 545). It is available at http://localhost:7474/
    There may be a short delay until the server is ready.
    See /home/neo4j/neo4j/neo4j-community-4.1.9/logs/neo4j.log for current status.
```

#### Where to look if it does not work
Look at the bottom of both the **debug.log** and the **neo4j.log**   
```
$ find neo4j-community-4.1.9/logs -type f
neo4j-community-4.1.9/logs/debug.log
neo4j-community-4.1.9/logs/neo4j.log
```

The neo4j config file is at `/home/neo4j/neo4j/neo4j-community-4.1.9/conf/neo4j.conf` if seen in the `debug.log` file:
```
Neo4j cannot be started because the database files require
upgrading and upgrades are disabled in the configuration.
Please set 'dbms.allow_upgrade' to 'true' in your
configuration file and try again.
```

### 6. Connect to the server for the first time
#### Create a password    
Setting both *Username* and *Password* to *neo4j* worked for us when loading a new Reactome database version for the first time.
![Authentification1](/doc/md/images/neo4j_reactome_connect1.png)

#### You will be asked to create a new password
To change your password again:    
```
:server change-password
```
![new password](/doc/md/images/neo4j_reactome_connect2.png)

### 7. View the Reactome database in the neo4j browser
In your browser, go to: **http://localhost:7474/browser/**

Click on the *Database* icon at the upper left corner (which should be green after clicking on it); there should be lots of Node Labels:
![success](/doc/md/images/neo4j_reactome_connect3_success.png)    
![databases](/doc/md/images/neo4j_reactome_connect4_dbs.png)

#### Try a Cypher command:
What sub-pathways are under under pathway, R-HSA-983169, _Class I MHC mediated antigen processing & presentation_?

![subpwy](images/neo4j_pwy_subpwy.png)

### 8. [**Python interface to neo4j**](README_gdbdr.md)    
More on the [next page...](README_gdbdr.md)    

Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
