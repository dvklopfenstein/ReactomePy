
vim_:
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

# Copyright (C) 2014-2018, DV Klopfenstein. All rights reserved.
