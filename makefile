# Reactome Python Neo4j tasks

# pylint:
# 	git status -uno | perl -ne 'if (/(\S.*\S):\s+(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$2}' | tee tmp_pylint
# 	chmod 755 tmp_pylint
# 	tmp_pylint

run:
	echo Hello

vim_ea_reactome:
	vim -p \
	../reactome_neo4j_py/src/bin/pwy_enrichment_reactome.py \
	../reactome_neo4j_py/src/reactomeneo4j/code/rest/service_analysis.py

pylint:
	@git status -uno | perl -ne 'if (/(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

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
	
# --------------------------------------------------------------------------------
dist_archive:
	#python3 -m pip install --user --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	find dist

clean_dist:
	rm -rf dist build reactomeneo4j.egg-info

# --------------------------------------------------------------------------------
upload_pypi_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

# - TEST ---------------------------------------------------------------------------------
test_internet:
	$(PY) src/tests/pwy_enrichment_reactome.py

test_simple:
	$(PY) src/tests/rpt_figs.py
	$(PY) src/tests/test_args.py

test_all:
	make test_internet
	make test_simple

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
