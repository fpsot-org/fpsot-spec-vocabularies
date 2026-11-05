# Changelog

All notable changes to this specification are listed here.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-05

### Added

- Schemes, concepts and codes: one SKOS concept scheme per vocabulary, stable `https` URIs built from the code, one plain notation per concept, codes that never change (VOC-001 to VOC-008).
- Labels and definitions: one preferred label in English and one in French, language tags, no clashes, alternative and hidden labels, definitions, reviewed changes (VOC-010 to VOC-016).
- Hierarchy and collections: top concepts, broader and narrower links in both directions, no cycles, related links, collections and display order (VOC-020 to VOC-025).
- Lifecycle and versions: no deletion, deprecation with replacements, fixed meanings, behavior of systems, change notes, Semantic Versioning, versioned files, open and closed schemes (VOC-030 to VOC-037).
- Mappings: reuse of authority schemes, SKOS mapping properties, published outside URIs, forbidden links, outside releases checked (VOC-040 to VOC-044).
- Publishing: Turtle and JSON-LD files, Turtle as the source, a CSV file with fixed columns, scheme description, automatic checks, resolvable URIs (VOC-050 to VOC-055).
- Binding in data models: LinkML enums whose values point to concept URIs, deprecated values, generated enums, stored codes, `CodeValue` for large schemes (VOC-060 to VOC-065).
- An example scheme of document types in Turtle, JSON-LD and CSV, its LinkML binding, a checking script and a test script in `model/`.
- Comparison data with an international baseline, Canada and Québec rows.
- A how-to guide, the agent skill, `llms.txt` and a book per language.

[Unreleased]: https://github.com/fpsot-org/fpsot-spec-vocabularies/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fpsot-org/fpsot-spec-vocabularies/releases/tag/v0.1.0
