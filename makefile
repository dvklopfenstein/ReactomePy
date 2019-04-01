# Reactome Python Neo4j tasks

PY = python3

# pylint:
# 	git status -uno | perl -ne 'if (/(\S.*\S):\s+(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$2}' | tee tmp_pylint
# 	chmod 755 tmp_pylint
# 	tmp_pylint

run:
	src/bin/pwy_enrichment_reactome.py data/enrich/studyids/UniProt.txt

pylint:
	@git status -uno | perl -ne 'if (/(\S+.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

run_tutorial:
	$(PY) src/bin_neo4j/tutorial/fig4a_2018_molecules_in_interleukin_signaling.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/fig4b_2018_ccr5_pathways.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s1a_get_pathway.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s1b_get_protein.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s2a_get_protein_fields.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s2b_get_protein_fields_from_nodes.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s3a_get_participants_complexes.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s4a_pathway_subpathways.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s4b_pathway_superpathways.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s5a_pathway_reactions.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s6a_reaction_participants.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s6b_reaction_participants.py $(PASSWORD)
	$(PY) src/bin_neo4j/tutorial/s7a_pathway_molecules.py $(PASSWORD)

# --------------------------------------------------------------------------------
# Re-generate Python modules containing Reatome data
# This is done for every new Reactome version
wrpy:
	src/bin_neo4j/wrpy/species.py $(PASSWORD)
	src/bin_neo4j/wrpy/disease.py $(PASSWORD)
	src/bin_neo4j/wrpy/referencedatabase.py $(PASSWORD)
	src/bin_neo4j/wrpy/inferredfrom.py $(PASSWORD)
	src/bin_neo4j/wrpy/pathway_molecules.py $(PASSWORD)

# --------------------------------------------------------------------------------
dist_archive:
	#python3 -m pip install --user --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	find dist

clean_dist:
	rm -rf dist build reactomepy.egg-info

# --------------------------------------------------------------------------------
upload_pypi_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

# - TEST ---------------------------------------------------------------------------------
test_all:
	make test_internet
	make test_simple

test_internet:
	echo TBD

test_simple:
	$(PY) src/tests/rpt_figs.py
	$(PY) src/tests/test_args_neo4j.py
	$(PY) src/tests/test_args_pwyea_reactome.py

# ----------------------------------------------------------------------------------------
clean:
	rm -f *.csv
	rm -f *pathway_enrichment*.pdf
	rm -f relationship_*.txt
	rm -f tmp_pylint
	make -f makefile clean_pyc

clean_tutorial:
	rm -f fig4a_pathway_molecules_IL_sig_R-HSA-6785807.txt
	rm -f fig4b_pathways_containing_CCR5.txt
	rm -f complex_components_all.txt
	rm -f pathway_molecules_R-HSA-983169.txt

clean_pyc:
	find . -name \*.pyc | xargs rm -f
	find . -name \*.st\*p | xargs rm -f
	rm -f tmp
	rm -f tmp_pylint

clobber_materials:
	rm goa_human.*; wget http://geneontology.org/gene-associations/goa_human.gaf.gz; gunzip goa_human.gaf.gz
	rm go-basic.obo*; wget http://geneontology.org/ontology/go-basic.obo

clobber_pwys:
	rm -f src/reactomepy/data/*/pathways/p*.py
	

# Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
