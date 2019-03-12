# NF Open Science Initiative metadata schema
This document describes the metadata requirements for all NF specific projects

### All files
These keys are required of all files in the NF-OSI projects

| key | 
 |---| 
| resourceType |
| fileFormat   |
| fundingAgency|
| consortium   |

The following requirement apply to subsets of data.

### `experimentalData` files
If `resourceType` is `experimentalData` we also require:

| key | condition |
| --- | ---|
| assay | *always* |
| dataType |*always* |
| dataSubtype| *always* |
| platform |*always* |
| specimenID |*always* |
| individualID ||
| species |*always* |
| diagnosis |If diseased|
| isCellLine |*always* |
| sex |*always* |
| tissue | if not cancer|
| tumoeType| if cancer|
| nf1Genotype ||
| nf2Genotype ||
| genePerturbationType|*if applicable*|
| genePertubrationTechnology| if applicable*|
| genePerturbed|if applicable*|
| experimentalCondition|optional|
| experimentalTimepoint|if applicable*|
| timePointUnit|if applicable*|


#### Files that are Sequencing
All sequencing files (`assay` is one of `rnaSeq,exomeSeq,wholeGenomeSeq,mrnaSeq`...) require these annotations:

| key |
| --- |
| readLength |
| readPair |
| runType |
| isStranded |
| dissociationMethod |
| nucleicAcidSource |
| libraryPrep |
| libraryPreparationMethod |

### `curatedData` files
TBD
| key |
| --- |
| curatedDataType|

### `report` files
TBD
| key |
| --- |
| diagnosis|


### `tools` files
Anything that is a tool should be annotated with the following:

| key |
| --- |
| softwareName |
| softwareType |
| softwareLanguage |
| softwareRepository|
| inputDataType |
| outputDataType |

