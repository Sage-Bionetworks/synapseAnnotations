# README

This subfolder contains our annotation controlled vocabularies, schemas, and
code to generate schemas based on existing JSON files.

To translate our original JSON files to JSON-LD and then to JSON Schema requires
the following steps:

1. Run `sage_annotations_2_biothings.py`. Running this on a single [input JSON file](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L55)
will take that file, add it to the Biothings schema, and save the result to a
file with the same base file name as the original (e.g. `sageCommunity.json`
becomes `sageCommunity.jsonld`). The script can also append additional data to a
JSON-LD file. To do this:
    1. Uncomment [this line](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L60) and set `base_schema_org_file` to the name of the file you want to extend
    1. Uncomment [this line](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L65)
    1. If desired, edit [this line](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/sage_annotations_2_biothings.py#L172) to provide a new filename for export.
1. When you have generated the JSON-LD file(s), hand-edit them to add additional
  information, such as `requiresChild: true` for nodes that will become required
  properties in the JSON Schema.
1. Then, run `jsonld_2_jsonschema.py`, replacing [`base_schema_org_file`](https://github.com/Sage-Bionetworks/synapseAnnotations/blob/d1d2a65105c6c1f3cbc62e58b20abc800d0c9c9e/synapseAnnotations/jsonld_2_jsonschema.py#L18) with the name of the file you wish to convert. `jsonld_2_jsonschema.py` takes JSON-LD files and generates JSON Schemas.

`data/` contains the original JSON files describing annotations, JSON-LD files
that extend the Biothings schema with our annotations, and JSON Schema files
derived from JSON-LD.

`masterSage.jsonld` contains the output from running step 1 above on
`experimentalData.json` and `sageCommunity.json`.
`masterSageTargetRequirements.jsonld` and `masterSageMoreRequirements.jsonld`
have examples of nodes that have some requirements.

