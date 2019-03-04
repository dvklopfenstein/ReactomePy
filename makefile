# Reactome Python Neo4j tasks

# pylint:
# 	git status -uno | perl -ne 'if (/(\S.*\S):\s+(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$2}' | tee tmp_pylint
# 	chmod 755 tmp_pylint
# 	tmp_pylint

run:
	echo Hello

# Re-generate Python modules containing Reatome data
# This is done for every new Reactome version
wrpy:
	src/reactomeneo4j/data/reactome_version.py $(PASSWORD)
	src/bin_neo4j/wrpy/species.py $(PASSWORD)
	src/bin_neo4j/wrpy/disease.py $(PASSWORD)
	src/bin_neo4j/wrpy/referencedatabase.py $(PASSWORD)
	src/bin_neo4j/wrpy/inferredfrom.py $(PASSWORD)
	src/bin_neo4j/wrpy/pathway_molecules.py $(PASSWORD)


# Write relationships for various schema
WRREL := src/bin_neo4j/run/get_relationship_cnts.py 
wr_rel:
	$(WRREL) $(PASSWORD) -o --schemaClass=ReactionLikeEvent
	$(WRREL) $(PASSWORD) -o --schemaClass=ReactionLikeEvent -r
	$(WRREL) $(PASSWORD) -o --schemaClass=Pathway
	$(WRREL) $(PASSWORD) -o --schemaClass=Pathway -r
	$(WRREL) $(PASSWORD) -o --schemaClass=TopLevelPathway
	$(WRREL) $(PASSWORD) -o --schemaClass=PhysicalEntity
	$(WRREL) $(PASSWORD) -o --schemaClass=PhysicalEntity -r
	$(WRREL) $(PASSWORD) -o --species='' --schemaClass=Drug
	mv relationship_r*.txt log/get_relationship_cnts
	

# mv_db:
# 	mv $(DL)/reactome.graphdb.gz .
# 	gunzip reactome.graphdb.gz
# 	tar -xvf reactome.graphdb.gz
# 	mv reactome.graphdb.v66 ~/neo4j/neo4j-community-3.4.7/data/graph.db

vim_:
	vim -p \
	./src/bin_neo4j/wrpy/pathways.py \
	./src/reactomeneo4j/code/session.py \
	./src/reactomeneo4j/code/graph.py \
	./src/reactomeneo4j/code/record.py \
	./src/reactomeneo4j/code/node.py \
	./src/reactomeneo4j/code/relationship.py \
	./src/reactomeneo4j/code/schema/data_schema.py \
	./src/reactomeneo4j/code/schema/hier.py \
	./src/reactomeneo4j/code/schema/hier_init.py \
	./src/reactomeneo4j/code/schema/node.py

vim_wrpy:
	vim -p \
	./src/bin_neo4j/wrpy/pathways.py \
	src/reactomeneo4j/code/wrpy/query_general.py \
	src/reactomeneo4j/code/wrpy/pathway_query.py \
	src/reactomeneo4j/code/wrpy/wrpy_general.py \
	src/reactomeneo4j/code/wrpy/pathway_wrpy.py \
	src/reactomeneo4j/data/hsa/pathways_publications.py \
	src/reactomeneo4j/data/species.py \
	src/reactomeneo4j/code/wrpy/utils.py

vim_pub:
	vim -p \
	src/bin/describe_pathway.py \
	src/reactomeneo4j/code/describe_pathway.py \
	src/reactomeneo4j/data/hsa/pathways/pathways.py \
	src/reactomeneo4j/code/species.py

vim_old:
	vim -p \
	./src/bin/test_reactome_tutorial.py \
	./src/reactomeneo4j/code/graphdb.py \
	./src/reactomeneo4j/code/lit_ref.py \
	./src/reactomeneo4j/code/pathway.py \
	./src/reactomeneo4j/code/acc_seq.py \
	./src/reactomeneo4j/code/node.py

vim_ea:
	vim -p \
	../reactome_neo4j_py/src/bin/example_pathway_enrichment.py \
	../reactome_neo4j_py/src/reactomeneo4j/code/rest/service_analysis.py \
	../reactome_neo4j_py/src/reactomeneo4j/code/cli/pwy_enrichment.py

pylint:
	@git status -uno | perl -ne 'if (/(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

# --------------------------------------------------------------------------------
dist_archive:
	#python3 -m pip install --user --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	find dist

clean_dist:
	rm -rf dist build enrichmentanalysis.egg-info

# --------------------------------------------------------------------------------
upload_pypi_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

# ----------------------------------------------------------------------------------------
clean:
	rm -f *.csv
	rm -f relationship_*.txt
	rm -f tmp_pylint
	make -f makefile clean_pyc

clean_pyc:
	find . -name \*.pyc | xargs rm -f
	find . -name \*.st\*p | xargs rm -f

clobber_materials:
	rm goa_human.*; wget http://geneontology.org/gene-associations/goa_human.gaf.gz; gunzip goa_human.gaf.gz
	rm go-basic.obo*; wget http://geneontology.org/ontology/go-basic.obo

clobber_pwys:
	rm -f src/reactomeneo4j/data/*/pathways/p*.py
	

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
