# Change Log

## Unreleased changes

## Reactome v69

### Release 2019-NN-NN 0.9.5

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


Copyright (C) 2018-2019, DV Klopfenstein. All rights reserved.
