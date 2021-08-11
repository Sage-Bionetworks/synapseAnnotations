## About this project

Welcome! This project is for managing annotations and controlled vocabularies for use in Synapse. These have been developed with communities supported by Sage Bionetworks in mind, but are not restricted to that use. If you want the files in your projects to be discoverable in the same fashion as the Sage-supported communities, then feel free to use these!

## Contributing

This contributing document focuses on the guidelines for users related to the Sage Bionetworks supported communities - that is to say Sage Bionetworks employees and members of the communities who are responsible for metadata and annotations.

## Format of new terms

Terms are stored in JSON Schema format. The `term-templates/` folder has more
examples, but the general format for a new term should be like this:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://repo-prod.prod.sagebase.org/repo/v1/schema/type/registered/sage.annotations-<MODULENAME>.<KEY>-0.0.1",
  "description": "<DESCRIPTION OF THE KEY>",
  "anyOf": [
    {
      "const": "<FIRST ALLOWABLE VALUE",
      "description": "<DESCRIPTION OF ALLOWABLE VALUE>",
      "source": "<URL OF VALUE'S SOURCE>"
    },
    {
      "const": "<SECOND ALLOWABLE VALUE",
      "description": "<DESCRIPTION OF ALLOWABLE VALUE>",
      "source": "<URL OF VALUE'S SOURCE>"
    }
  ]
}
```

This JSON should be stored in the `terms/` folder under the appropriate module,
and the file name should be the same as the key (e.g. the `assay` key is stored
as `assay.json`).

If you are adding a value to an existing term, you should edit the existing JSON
file. You **must** update the version number in the `$id` field if you are
changing the term's definition.

## Guidelines for proposing new terms

Our strategy is to rely on annotation terms and definitions that have already been made and standardized whenever possible for use with Sage Bionetworks supported communities. In general, we will not include terms in this repository that are not needed and vetted by our communities - but don't let that stop you from using this! Feel free to fork and include terminology that you require for your own use.

If you are proposing a new term, then we require a source for the definition. The first place to look for an existing term is the [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols). We have some preferred ontology term sources: EDAM, EFO, OBI, and NCIT. It's OK if your term comes from another source, but use the preferred sources whenever possible. You should use the term as defined in the source, or one of its synonyms. If your term does not currently exist, or has a different definition than existing ones, then:

1. Provide a different source URL - this may be a Wikipedia entry, link to a commercial web site, or other URL.
1. If you are a Sage Bionetworks employee and cannot find a source URL, then use "Sage Bionetworks" as the `source` and your own definition.
2. If you are not (nor are you working with a Sage Bionetworks supported community) it is up to you for a strategy for controlling new terms to be added.

## Guidelines for specific term types 

In some situations (e.g. drug names), terms are not always well-captured by the ontologies found in the Ontology Lookup Service. We've defined some best practices for contributing these terms here.

### Contribution of drug terms

The preferred first-pass strategy for chemical name annotation is to search the EMBL-EBI ontology lookup service to find names, descriptions, and sources. Typically, the NCI Thesaurus will provide a suitable description for drugs and other biologically active molecules. In situations where the query molecule is not found in [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols), a helpful secondary location to find chemical descriptions is [MeSH](https://meshb.nlm.nih.gov/).

Example: 

```json
{
        "const": "DEFACTINIB",
        "description": "An orally bioavailable, small-molecule focal adhesion kinase (FAK) inhibitor with potential antiangiogenic and antineoplastic activities.",
        "source": "http://purl.obolibrary.org/obo/NCIT_C79809"
},
```

In situations where novel molecules (such as newly-synthesized research compounds or proprietary pharmaceutical molecules) require annotation, the only suitable description and source might be the paper describing the synthesis or discovery, or information from the pharmaceutical company that created the identifier. 

Example:

```json
{
        "const": "IPC-12345",
        "description": "An small-molecule target of importance 4 (TOI4) inhibitor with potential antineoplastic activities.",
        "source": "Important Pharma Company"
},
{
        "const": "BestChemist-00913",
        "description": "An investigational small molecule discovered by Best Chemist et al.",
        "source": "PubMed Link Goes Here"
},
```
### Contribution of species terms

The preferred strategy for species name annotation is to search the [NCBI Taxonomy Browser](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Root) to find names, descriptions, and sources. The format of the description should be "`Species name` with taxonomy ID: `taxonomyID` and Genbank common name `common name`". The species name, taxonomyID, and Genbank common name can all be found in the NCBI Taxonomy Browser entry for the species.

For example:

```json
{
        "const": "Drosophila melanogaster",
        "description": "Drosophila melanogaster with taxonomy ID: 7227 and Genbank common name: fruit fly",
        "source": "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=7227"
}
```

### Contribution of file formats

We use the `fileFormat` key to indicate, well, the file format of a file uploaded to Synapse. Given the bias towards genomics files in Synapse, our source for file formats tends to come from [EDAM](http://edamontology.org/), [NCIT](http://www.ontobee.org/ontology/NCIT), but also Wikipedia and corporate web site descriptions. One thing to note is that the `value` to be contributed does not need to be the same as the commonly used file extension. For example, we describe GZipped files as `gzip`, while a GZipped file generally has an extension of `gz`.

## Contribution procedure

Again, this is focused on Sage Bionetworks supported communities and employees.

1. Propose a change, either through a Github [issue](https://github.com/Sage-Bionetworks/synapseAnnotations/issues) or [pull request](https://github.com/Sage-Bionetworks/synapseAnnotations/pulls). Your change should be as atomic as possible - e.g., don't lump together many unrelated changes into a single issue or pull request. You may be requested to split them out.
1. Label your issue or pull request with the appropriate labels. For example, if you are suggesting a new value be added to an existing key, then `create value` would be the appropriate label.
1. For pull requests, request a review from someone in Github - this can be found under 'Reviewers' on the right side of the screen when viewing a Github issue. At least one review is required for any changes to terms that part of the core vocabulary (i.e. non-project-specific terms); more reviews are even better. Everyone is welcome to review open PRs, even if they were not formally assigned through GitHub. 
