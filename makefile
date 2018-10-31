# Reactome Python Neo4j tasks

# pylint:
# 	git status -uno | perl -ne 'if (/(\S.*\S):\s+(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$2}' | tee tmp_pylint
# 	chmod 755 tmp_pylint
# 	tmp_pylint

run:
	echo Hello

# Re-generate Python modules containing Reatome data
# This is done for every new Reactome version
mkpy:
	src/mkpy/pathways.py $(PASSWORD)
	src/mkpy/species.py $(PASSWORD)
	src/mkpy/disease.py $(PASSWORD)

# mv_db:
# 	mv $(DL)/reactome.graphdb.gz .
# 	gunzip reactome.graphdb.gz
# 	tar -xvf reactome.graphdb.gz
# 	mv reactome.graphdb.v66 ~/neo4j/neo4j-community-3.4.7/data/graph.db

vim_:
	vim -p \
	./src/bin/run_reactome_tutorial.py \
	./src/mkpy/pathways.py \
	./src/reactomeneo4j/code/session.py \
	./src/reactomeneo4j/code/graph.py \
	./src/reactomeneo4j/code/record.py \
	./src/reactomeneo4j/code/node.py \
	./src/reactomeneo4j/code/relationship.py \
	./src/reactomeneo4j/code/schema/data_schema.py \
	./src/reactomeneo4j/code/schema/hier.py \
	./src/reactomeneo4j/code/schema/hier_init.py \
	./src/reactomeneo4j/code/schema/node.py

vim_pw:
	vim -p \
	./src/mkpy/pathways.py \
	src/reactomeneo4j/code/mkpy/pathway_query.py \
	src/reactomeneo4j/code/mkpy/pathway_wrpy.py \
	src/reactomeneo4j/data/hsa/pathways_publications.py \
	src/reactomeneo4j/data/species.py \
	src/reactomeneo4j/code/mkpy/utils.py

vim_pub:
	vim -p \
	src/bin/describe_pathway.py \
	src/reactomeneo4j/code/describe_pathway.py \
	src/reactomeneo4j/data/hsa/pathways/pathways.py

vim_old:
	vim -p \
	./src/bin/test_reactome_tutorial.py \
	./src/reactomeneo4j/code/graphdb.py \
	./src/reactomeneo4j/code/lit_ref.py \
	./src/reactomeneo4j/code/pathway.py \
	./src/reactomeneo4j/code/acc_seq.py \
	./src/reactomeneo4j/code/node.py

pylint:
	@git status -uno | perl -ne 'if (/(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

clean_pyc:
	find . -name \*.pyc | xargs rm -f
	find . -name \*.stackdump | xargs rm -f

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
