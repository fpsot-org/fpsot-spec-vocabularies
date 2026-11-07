# Instructions for agents

This repository holds the FPSOT vocabularies specification: how FPSOT projects publish controlled vocabularies as W3C SKOS concept schemes, with stable URIs and codes, English and French labels, deprecation, mappings, published files and LinkML bindings.

- The normative text is in `spec/en/` and `spec/fr/`. Every rule has an ID such as `VOC-001`.
- Follow `skill/SKILL.md` when you create or change a vocabulary, or bind a field to one, in any FPSOT project. The spec text wins on any difference.
- `model/` holds the example scheme and its LinkML binding. Run `model/test-model.sh` after you change them.
- Every page exists in English and in French, with the same file name and the same IDs.
- Terms and abbreviations come from the term base of `fpsot-spec-writing`. Add a missing term there first.
- This is a layer 1 specification. It may refer to layer 0 specifications and to the data types specification, never to a higher layer. It names API specifications by topic only.
- Do not copy text from outside standards. Summarize them in your own words and cite the exact version.
- Commits follow Conventional Commits and are signed. Pull requests are squash-merged.
