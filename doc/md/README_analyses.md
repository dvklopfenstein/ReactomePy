# Analyze Data with <img src="images/logo_reactome.png" height="50pt">
Get the [**same analysis results**](#command-line-and-reactome-gui-return-the-same-results)
from the [**command line**](#command-line-examples)
as from Reactome's [**Analyse Data Tool GUI**](https://reactome.org/PathwayBrowser/#TOOL=AT).

The results are written into these files:
  * result.csv
  * mapping.csv
  * result.pdf
  * not_found.csv

## Command-line Examples
```
$ src/bin/pwy_enrichment_reactome.py data/enrich/studyids/1q21o3.txt
```

## Command-line and Reactome GUI return the same results

  1. [**Reactome Pathway Analysis**](#1-reactome-pathway-analysis)
  2. [**Load Study IDs**](#2-load-study-ids)

### 1) Reactome Pathway Analysis
Click on **Analyze Data** to begin a pathway enrichment analysis.
![Reactome's Pathway Analysis](images/anal00_analyze_data.png)

### 2) Load Study IDs
![Load Study IDs into Reactome](images/anal01_load_study_ids.png)


Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
