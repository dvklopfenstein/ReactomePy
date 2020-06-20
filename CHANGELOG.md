# Change Log

## Unreleased changes





## Reactome v71

#### Summary for Reactome v71 pathways that are not inferred
##### Pathways

|count| description
|-----|------------
|2,492| total pathways
|  508| is in disease
|   32| top-level pathway

##### 999 (40.09%) pathways have figures

|count| description
|-----|------------
|  999| generated figure or hand-drawn figurehttps://t.co/7xByA9uKKa?amp=1
|  826| generated figure
|  173| hand-drawn figure

##### 2,302 pathways (92.38%) have a publication:

```
Publications summary key:
  P -> PubMed ID
  B -> Book
  U -> URL
```

| count | publication keys
|-------|-----------------
| 2,191 | P..
|    67 | PB.
|    34 | .B.
|     7 | P.U
|     2 | ..U
|     1 | PBU


#### Added:
  * One species: Clostridium perfringens (cpe, taxid=1502)

#### Changed
  * Number instances increased for relationships involving PhysicalEntity and Event except:
    * Small decrease for:
      * (PhysicalEntity)-[repeatedUnit]->(PhysicalEntity)
    * No change for:
      * (PhysicalEntity)-[entityOnOtherCell]->(PhysicalEntity)
      * (Event)-[reverseReaction]->(Event)
      * (Event)-[entityOnOtherCell]->(PhysicalEntity)
  * (Person):
    * Added about 4,000 more people (Person)
    * Removed *BA Brown-Kipphut* and *MD Maines*
  * (Figure):
    * Number of figures reduced to 785 from 808
    * Removed figure author, *Marcela Tello-Ruiz*
    * Seven more pathways have figures
  * (Summation):
    * Added ~50 Pathway Summations
  * Diseases: Added 47 and removed 4
  * Node instances that were reduced:

|Node name             |    from | to
|----------------------|---------|------
|GO_CellularComponent  |     338 | 304
|Depolymerisation      |      38 | 31
|OtherEntity           |     334 | 330
|Polymer               |   1,518 | 1,507
|GenomeEncodedEntity   |   6,909 | 5,915
|ReferenceDNASequence  | 533,570 | 475,150
|OtherEntity           |     334 | 330
|TopLevelPathway       |     389 | 374

## Reactome v69

### Release 2019-07-29 v69.00

#### Added:
  * New relationships:
    * regulation
    * regulationReference
    * catalystActivityReference
    * surroundedBy
  * New Classes:
    * ***ControlReference***
      * ***CatalystActivityReference***
      * ***RegulationReference***
  * New relationships on ***ReactionLikeEvent*** to new ***ControlReference*** classes
  * New optional parameter, ***stoichiometryKnown***, to ***Complex***
  * New optional parameter, ***pubmed***, to ***UndirectedInteraction***
  * New relationship, ***surroundedBy***, to ***GO_CellularComponent***

#### Removed:
  * Removed relationships from ***GO_BiologicalProcess***, ***GO_MolecularFunction***, :
    * ***regulate***
    * ***positivelyRegulate***
    * ***negativelyRegulate***


Copyright (C) 2018-present, DV Klopfenstein. All rights reserved.
