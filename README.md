# [Reactome](https://reactome.org/), Python, and Neo4j

In addition to being a world-class pathway database, 
Reactome contains 
expert-authored and peer-reviewed
reactions, 
molecular complex ingredients and structure, and
protein-protein interactions.

Links 
links to biological models, 
links to associated reasearch papers, URLs, and books.


## Use this Python library to:

  1) Run [**Reactome's Neo4j Tutorial**](https://reactome.org/dev/graph-database/extract-participating-molecules)
     from one of the [**Jupyter notebooks**](src/ipy/tutorial) or a plain [**Python script**](src/bin_neo4j/tutorial)

  2) Find enriched pathways [**from the command line**](doc/md/README_analyses.md),
     accessing Reactome's online [**Pathway Analysis Service**](https://reactome.org/AnalysisService/) 

  3) Find enriched pathways using custom associations.

  4) Explore the Reactome Knowledgebase 
     with a [**neo4j query**](doc/md/README_cypher_cmd.md)
     in a [**Python script**](src/ipy/tutorial/s4a_pathway_subpathways.ipynb)

## To Cite

_Please cite the following research paper if this repo is used in your research_:

Klopfenstein DV, Dampier W 
[**Understudied disease genes are similar to gene neighbors in human, mouse and fly**](https://www.nature.com/articles/s41598-018-28948-z)    
_bioRxiv_ | (2019) N:NNNNN | DOI:XXXXXXXXX

## Links
  * **User's Download hints**:
    * [1) Install Neo4j](/doc/md/README_install_neo4j.md)
    * [2) Download Reactome Knowledgebase](/doc/md/README_download_hints.md)    
  * **Reactome Publications**
    * 2018 | [Reactome graph database: Efficient access to complex pathway data](https://journals.plos.org/ploscompbiol/article?rev=2&id=10.1371/journal.pcbi.1005968)
  * **Reactome Documentation**    
    * [Data Schema](https://reactome.org/content/schema/DatabaseObject)    
    * [Glossary Data Model](http://wiki.reactome.org/index.php/Glossary_Data_Model)    
    * [Icon library](https://reactome.org/icon-lib)    
    * [Reactome Graph Database on GitHub](https://github.com/reactome/graph-core)    

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
