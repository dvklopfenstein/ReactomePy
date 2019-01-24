# Biological Pathways, Reactome, Python, and Neo4j
Explore peer-reviewed biological pathways in Reactome using Python to run neo4j queries

## **Scripts**
  * **No need to have Neo4j running:**    
    * [src/bin](/src/bin)     
  * **Neo4j must be installed and running on data downloaded from Reactome:**    
    * Run [**Reactome's tutorial**](https://reactome.org/dev/graph-database/extract-participating-molecules) of Neo4j queries using these Python scripts:    
       * **Jupyter notebooks:** [src/ipy/tutorial](src/ipy/tutorial)
       * **Python scripts:** [src/bin_neo4j/tutorial](src/bin_neo4j/tutorial)
    * Extract Reactome data using Neo4j. Save in Python modules used by scripts in [src/bin](src/bin):    
      * [src/bin_neo4j/wrpy](src/bin_neo4j/wrpy)

## Prerequisites
  * Python 3.5 or greater

### Packages
  * docopt

## Reactome Links
  * [**Download hints**](/doc/md/README_download_hints.md)
  * **Publications**
    * 2018 [Reactome graph database: Efficient access to complex pathway data](https://journals.plos.org/ploscompbiol/article?rev=2&id=10.1371/journal.pcbi.1005968)
  * [Data Schema](https://reactome.org/content/schema/DatabaseObject)    
  * [Glossary Data Model](http://wiki.reactome.org/index.php/Glossary_Data_Model)    
  * [Icon library](https://reactome.org/icon-lib)    
  * [Reactome Graph Database on GitHub](https://github.com/reactome/graph-core)    

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
