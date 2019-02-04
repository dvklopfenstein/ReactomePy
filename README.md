# Reactome, Python, and Neo4j

**_[Reactome](https://reactome.org/) isn't just Biological Pathways_ ...**

Reactome contains a treasure trove of expert-authored, peer-reviewed detailed knowledge of reactions, ingredients of molecular complexes, protein-protein interactions, links to biological models, links to associated reasearch papers, URLs, and books, as well as pathway information.

Explore [**using Python**](src/ipy/tutorial/s4a_pathway_subpathways.ipynb) to run [**neo4j queries**](/doc/md/README_download_hints.md#6-view-the-reactome-database-in-the-neo4j-browser) on the Reactome Knowledgebase.

## To Cite

_Please cite the following research paper if this repo is useful for your research_:

Klopfenstein DV, Tozeren A, Dampier W [Disease hotspots in Human, Mouse, and Fly](https://www.nature.com/articles/s41598-018-28948-z)    
_bioRxiv_ | (2019) N:NNNNN | DOI:XXXXXXXXX


## Scripts
  * **No need to have Neo4j running:**    
    * [src/bin](/src/bin)     
  * **Neo4j must be installed and running on data downloaded from Reactome:**    
    * Run [**Reactome's tutorial**](https://reactome.org/dev/graph-database/extract-participating-molecules) of Neo4j queries using these Python scripts:    
       * **Jupyter notebooks:** [src/ipy/tutorial](src/ipy/tutorial)
       * **Python scripts:** [src/bin_neo4j/tutorial](src/bin_neo4j/tutorial)

## Prerequisites
  * Python 3.5 or greater

### Packages
  * docopt

## Reactome Links
  * **Download hints**:
    * [**Download Reactome Knowledgebase**](/doc/md/README_download_hints.md)
  * **Publications**
    * 2018 [Reactome graph database: Efficient access to complex pathway data](https://journals.plos.org/ploscompbiol/article?rev=2&id=10.1371/journal.pcbi.1005968)
  * [Data Schema](https://reactome.org/content/schema/DatabaseObject)    
  * [Glossary Data Model](http://wiki.reactome.org/index.php/Glossary_Data_Model)    
  * [Icon library](https://reactome.org/icon-lib)    
  * [Reactome Graph Database on GitHub](https://github.com/reactome/graph-core)    

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
