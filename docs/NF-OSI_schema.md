# NF Open Science Initiative metadata schema
This document describes the metadata requirements for all NF specific projects

### All files
These keys are required of all files in the NF-OSI projects

| key | 
|---| 
| resourceType |
| fileFormat   |
| fundingAgency|
| consortium  *if applicable* |

The following requirement apply to subsets of data.

### `experimentalData` files
If `resourceType` is `experimentalData` we also require:

| key | condition |
| --- | ---|
| assay | *always* |
| dataType |*always* |
| dataSubtype| *always* |
| specimenID |*always* |
| individualID ||
| species |*always* |
| diagnosis |If diseased|
| isCellLine |*always* |
| sex |*always* |
| tissue | if not cancer|
| tumorType| if cancer|
| nf1Genotype ||
| nf2Genotype ||
| genePerturbationType|*if applicable*|
| genePerturbationTechnology| *if applicable*|
| genePerturbed|*if applicable*|
| experimentalCondition|optional|
| experimentalTimepoint|*if applicable*|
| timePointUnit|*if applicable*|

#### Files that are Sequencing
All sequencing files (`assay` is one of `rnaSeq,exomeSeq,wholeGenomeSeq,mrnaSeq`...) require these annotations:

| key |
| --- |
| platform |
| readLength |
| readPair |
| runType |
| isStranded |
| dissociationMethod |
| nucleicAcidSource |
| libraryPrep |
| libraryPreparationMethod |

#### Files that are Arrays
All array files (`assay` is one of `snpArray`, `rnaArray`, `mirnaArray`...) require these annotations:

| key ||
| --- | --- |
| platform ||
| nucleicAcidSource | *if applicable* |

#### Files that are Immunochemistry
All immunochemistry files (`assay` is one of `westernBlot`, `immunohistochemistry`...) require these annotations:

| key |
| --- |
| assayTarget |

#### Files that are Drug Screening
All drug screening files (`assay` is `cellViabilityAssay`) require these annotations:

| key ||
| --- | --- |
| chemicalStructure | *if single or drug combination*, InChIKey only|

### `curatedData` files
TBD

| key |
| --- |
| curatedDataType |

### `report` files
TBD

| key |
| --- |
| diagnosis |


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

