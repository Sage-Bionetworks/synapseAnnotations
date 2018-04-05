## About this project

Welcome! This project is for managing annotations and controlled vocabularies for use in Synapse. These have been developed with communities supported by Sage Bionetworks in mind, but are not restricted to that use. If you want the files in your projects to be discoverable in the same fashion as the Sage-supported communities, then feel free to use these!

## Contributing

This contributing document focuses on the guidelines for users related to the Sage Bionetworks supported communities - that is to say Sage Bionetworks employees and members of the communities who are responsible for metadata and annotations.

## Guidelines for proposing new terms

Our strategy is to rely on annotation terms and definitions that have already been made and standardized whenever possible for use with Sage Bionetworks supported communities. In general, we will not include terms in this repository that are not needed and vetted by our communities - but don't let that stop you from using this! Feel free to fork and include terminology that you require for your own use.

If you are proposing a new term, then we require a source for the definition. The first place to look for an existing term is the [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols). We have some preferred ontology term sources: EDAM, EFO, OBI, and NCIT. It's OK if your term comes from another source, but use the preferred sources whenever possible. You should use the term as defined in the source, or one of it's synonyms. If your term does not currently exist, or has a different definition than existing ones, then:

1. Provide a different source URL - this may be a Wikipedia entry, link to a commercial web site, or other URL.
1. If you are a Sage Bionetworks employee and cannot find a source URL, then use "Sage Bionetworks" as the `source` and your own definition.
2. If you are not (nor are you working with a Sage Bionetworks supported community) it is up to you for a strategy for controlling new terms to be added.

## Guidelines for specific term types 

In some situations (e.g. drug names), terms are not always well-captured by the ontologies found in the Ontology Lookup Service. We've defined some best practices for contributing these terms here.

### Contribution of drug terms

The preferred first-pass strategy for chemical name annotation is to search the EMBL-EBI ontology lookup service to find names, descriptions, and sources. Typically, the NCI Thesaurus will provide a suitable description for drugs and other biologically active molecules. In situations where the query molecule is not found in [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols), a helpful secondary location to find chemical descriptions is [MeSH](https://meshb.nlm.nih.gov/).

Example: 

```
{
        "value": "DEFACTINIB",
        "description": "An orally bioavailable, small-molecule focal adhesion kinase (FAK) inhibitor with potential antiangiogenic and antineoplastic activities.",
        "source": "http://purl.obolibrary.org/obo/NCIT_C79809"
},
```

In situations where novel molecules (such as newly-synthesized research compounds or proprietary pharmaceutical molecules) require annotation, the only suitable description and source might be the paper describing the synthesis or discovery, or information from the pharmaceutical company that created the identifier. 

Example:

```
{
        "value": "IPC-12345",
        "description": "An small-molecule target of importance 4 (TOI4) inhibitor with potential antineoplastic activities.",
        "source": "Important Pharma Company"
},
{
        "value": "BestChemist-00913",
        "description": "An investigational small molecule discovered by Best Chemist et al.",
        "source": "PubMed Link Goes Here"
},
```


## Contribution procedure

Again, this is focused on Sage Bionetworks supported communities and employees. This focuses on the logistical components to contributing - for the technical components, please see the [Development](https://github.com/Sage-Bionetworks/synapseAnnotations#development) section of the [README.md](README.md) document.

1. Propose a change, either through a Github [issue](https://github.com/Sage-Bionetworks/synapseAnnotations/issues) or [pull request](https://github.com/Sage-Bionetworks/synapseAnnotations/pulls). Your change should be as atomic as possible - e.g., don't lump together many unrelated changes into a single issue or pull request. You may be requested to split them out.
1. Label your issue or pull request with the appropriate labels. For example, if you are suggesting a new value be added to an existing key, then `create value` would be the appropriate label.
1. Assign the issue to yourself and anyone else who will be involved in completing it. At a minimum, the issue creator should be assigned initially.
1. If this is a pull request a review from someone in Github - this can be found under 'Reviewers' on the right side of the screen when viewing a Github issue. It's fine if they can review your pull request without meeting. Otherwise, set up a meeting on your own to meet with your reviewer.
1. If your reviewer has no problems with the change, then the change can be merged. 
The issue creator is responsible for merging. Note that you can use [keywords](https://help.github.com/articles/closing-issues-using-keywords/) to close issues via your pull request. See the [Development](https://github.com/Sage-Bionetworks/synapseAnnotations#development) section of the [README.md](README.md) document for the merging procedure.
1. If you and the reviewer decide that a larger discussion is necessary, the issue can be brought to the larger annotations working group for discussion.
