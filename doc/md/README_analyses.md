# Analyze Data with <img src="images/logo_reactome.png" height="50pt">
Do pathway enrichment analysis using Reactome's
[**Pathway Analysis Service**](https://reactome.org/AnalysisService/)
from the command-line.

This returns the same results as running a pathway enrichment analysis
from the [_Analyse your data_i](https://reactome.org/PathwayBrowser/#TOOL=AT) tabxi
in the Reactome _Analysis tools_ web page.

The results are written into these files:
  * result.csv
  * mapping.csv
  * result.pdf
  * not_found.csv

## Examples
```
$ src/bin/pwy_enrichment_reactome.py data/enrich/studyids/1q21o3.txt
```

Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
