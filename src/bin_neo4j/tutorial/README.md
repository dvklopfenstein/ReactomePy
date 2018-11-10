# Reactome's Neo4j Tutorial
Run Reactome's [tutorial](https://reactome.org/dev/graph-database/extract-participating-molecules) of Neo4j queries using Python scripts.

## Tutorial: Report participating molecules
Build a query to retrieve the resource and identifier of each participating molecule of a given Pathway in six stages:

1. [How to retrieve objects like proteins, reactions, pathways, etc.](https://reactome.org/dev/graph-database/extract-participating-molecules#retrieving-objects)
2. [How to get the identifier of proteins or chemicals](https://reactome.org/dev/graph-database/extract-participating-molecules#identifiers-proteins-or-chemicals)
3. [How to deconstruct complexes or sets to get their participants](https://reactome.org/dev/graph-database/extract-participating-molecules#complexes-sets-participants)
4. [How to retrieve the subpathways for a given pathway](https://reactome.org/dev/graph-database/extract-participating-molecules#retrieving-pathways)
5. [How to retrieve the reactions of a pathway](https://reactome.org/dev/graph-database/extract-participating-molecules#retrieving-reactions)
6. [How to retrieve the participants of a reaction](https://reactome.org/dev/graph-database/extract-participating-molecules#joining-pieces)

/src/bin_neo4j/tutorial/s1a_get_pathway.py
/src/bin_neo4j/tutorial/s1b_get_protein.py
/src/bin_neo4j/tutorial/s2a_get_protein_fields.py
/src/bin_neo4j/tutorial/s2b_get_protein_fields_from_nodes.py
/src/bin_neo4j/tutorial/s3a_get_participants_complexes.py
/src/bin_neo4j/tutorial/s4a_pathway_subpathways.py
/src/bin_neo4j/tutorial/s4b_pathway_superpathways.py
/src/bin_neo4j/tutorial/s5a_pathway_reactions.py
/src/bin_neo4j/tutorial/s6a_reaction_participants.py
/src/bin_neo4j/tutorial/s6b_reaction_participants.py
/src/bin_neo4j/tutorial/s7a_pathway_molecules.py

Copyright (C) 2014-2019, DV Klopfenstein. All rights reserved.
