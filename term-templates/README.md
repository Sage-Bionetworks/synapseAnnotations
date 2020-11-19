# Term templates

This folder contains templates that can guide you in adding new terms that are
formatted correctly.

* `template-string.json`: template for a term that can be a string of 1-50
  characters.
* `template-enum.json`: template for a term with a specific set of allowable
  values. Note that we do not use JSON Schema's `"enum"` keyword and instead use
  the `"anyOf"` keyword with an array of constants (`"const"`) so that we can
  keep descriptions and source URLs together with each value.
* `template-number.json`: template for a term that is a number.
* `template-boolean.json`: template for a term that can be true or false.

These are just examples that show a few possibilities. For more information on
writing JSON Schema, see the following documentation:
https://json-schema.org/understanding-json-schema/index.html
