# NF Open Science Initiative metadata schema
This document describes the metadata requirements for all NF specific projects

### All files
These keys are required of all files in the NF-OSI projects

| key   |
 -------------
| resourceType |
| fileFormat   |
| fundingAgency|
| consortium   |

The following requirement apply to subsets of data.

### `experimentalData` files
If `resourceType` is `experimentalData` we also require:

| key |
-----
| assay |
| dataType |
| dataSubtype |
| platform |
| specimenID |
| individualID |
| species |
| diagnosis |
| tumorType |

#### Files that are Sequencing
All sequencing files (`assay` is one of `rnaSeq,exomeSeq,wholeGenomeSeq`...)
require these annotations:


### `curatedData` files

### `report` files
