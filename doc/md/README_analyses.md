# Analyze Data with <img src="images/logo_reactome.png" height="50pt">
Get analysis results
from the [**command line**](#command-line-examples)
like those from Reactome's [**Analyse Data Tool GUI**](https://reactome.org/PathwayBrowser/#TOOL=AT).

## Table of Contents
  * [Output files](#output-files)
  * [Command-line Examples](#command-line-examples)
  * [Command-line and Reactome GUI compared](#command-line-and-reactome-gui-return-the-same-results)

## Output Files

The pathway enrichment results are written into these files:

| Reactome Name | ReactomePy Name
|---------------|-----------------
| result.csv    | pathway_enrichment.csv
| result.pdf    | pathway_enrichment.pdf
| mapping.csv   | ids_mapping.csv
| not_found.csv | ids_notfound.csv

## Command-line Examples
```
$ src/bin/pwy_enrichment_reactome.py data/enrich/studyids/1q21o3.txt
```

## Command-line and Reactome GUI return the same results

  1. [**Reactome Pathway Analysis**](#1-reactome-pathway-analysis)
  2. [**Load Study IDs**](#2-load-study-ids)

### 1) Reactome Pathway Analysis
Click on **Analyze Data** on [**Reactome's homepage**](https://reactome.org) to begin a pathway enrichment analysis.

![Reactome's Pathway Analysis](images/anal00_analyze_data.png)

### 2) Load Study IDs
Load the study ID file
from the [**command line**](#command-line-examples)
or in Reactome's [**Analyse Data Tool GUI**](https://reactome.org/PathwayBrowser/#TOOL=AT).

![Load Study IDs into Reactome](images/anal01_load_study_ids.png)


Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
