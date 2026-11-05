---
name: fpsot-vocabularies
description: Controlled vocabulary rules for FPSOT projects. Use when creating or changing a code list, a classification or a thesaurus, publishing it as SKOS, mapping it to another scheme, or binding a field of a LinkML model to it.
---

# FPSOT vocabularies

Summary of the FPSOT vocabularies specification. It adds no rules of its own.
The spec text in `spec/` wins on any difference. Each line cites its requirement ID and keeps its strength: must, should or may.

## Schemes, concepts and codes

- A controlled vocabulary must be one SKOS concept scheme, and each value must be a concept with `skos:inScheme` (VOC-001).
- The scheme URI must use `https` on a domain the publisher keeps, and should be `https://<host>/vocabularies/<scheme-name>`. The name must be an English plural noun in kebab-case. No version, status, language or extension may appear (VOC-002).
- A concept URI must be the scheme URI + `/concepts/` + its plain code. A collection URI must be the scheme URI + `/collections/` + name (VOC-003).
- A published URI must keep naming the same thing forever and must never be reused (VOC-004).
- Each concept must have exactly one plain-string `skos:notation`: the stored code, unique in the scheme. It departs on purpose from SKOS typed literals. Other code systems may add typed notations (VOC-005).
- Codes you define must be kebab-case English (NAM-060). Codes of other issuers must keep their exact form, such as `QC`. If the issuer may reuse codes, a scheme that mirrors its list must use plain codes you define, with the issuer's code as a typed notation; the other choice is to map to the issuer's scheme (VOC-006).
- A code must never change or move to another concept. A new code means a new concept and a deprecated old one, also when an issuer changes its code (VOC-007).
- A code you define must not encode hierarchy, order or other properties (VOC-008).

## Labels and definitions

- Each scheme, concept and collection must have exactly one `skos:prefLabel@en` and one `@fr` (VOC-010).
- Each label, definition and note must carry a tag per LOC-001 and LOC-002, and must exist in `en` and `fr`. Other languages and regional tags such as `@fr-CA` may be added; a regional label exists only when the wording differs (VOC-011).
- Two concepts of one scheme that are not deprecated must not share a preferred label in one language. A deprecated concept that keeps such a label should qualify it, such as "Building permit (before 2027)". An alternative label should not match another concept's preferred label (VOC-012).
- `altLabel` may hold synonyms, abbreviations and former labels. `hiddenLabel` may hold misspellings. One text must not be in two label kinds (VOC-013).
- Labels should be nouns in the reader's words, should start with a capital, must not end with a period, and should use term base terms (VOC-014).
- Each concept must have a `skos:definition` in English and French, in plain language. It should say what is covered and what is not. A scope note may add advice (VOC-015).
- Text may improve in any release if the meaning stays. A former preferred label should become an alternative label. A person must review each new or changed text before release (VOC-016).

## Hierarchy and collections

- Each concept without a broader concept must be a top concept, stated in both directions (VOC-020).
- Use `skos:broader` and `skos:narrower`, both stated, within one scheme only (VOC-021).
- Broader chains must have no cycle. A concept should have at most one broader concept, and may have more when it truly belongs under each (VOC-022).
- Broader must mean kind, part or instance. Other links must use `skos:related`, which must not join concepts on one broader chain (VOC-023).
- Groups that are not concepts must be `skos:Collection`, or `skos:OrderedCollection` when order matters. Data must not store a collection as a code (VOC-024).
- Display order must come from an ordered collection or from label collation per LOC-015, never from codes (VOC-025).

## Lifecycle and versions

- A published concept must never be deleted (VOC-030).
- To retire one: `owl:deprecated true`, a change note with the reason, and `dct:isReplacedBy` / `dct:replaces` when a replacement exists (VOC-031).
- The meaning of a concept must not change. A new meaning must be a new concept (VOC-032).
- Systems must accept and show deprecated codes in stored data, must not offer them for new data, and should offer the replacement (VOC-033).
- Each change must add a `skos:changeNote` in both languages, starting with the date and version, and set `dct:modified` (VOC-034).
- Each release must have a SemVer number in `owl:versionInfo` and a date in `dct:modified`. A scheme should never need a major release, and a major release still must not break VOC-004, VOC-007 or VOC-030 (VOC-035).
- Each release must stay available at `<scheme URI>/versions/<version>`. The scheme URI must serve the latest (VOC-036).
- The scheme must say whether minor releases add concepts. Enum checks apply when writing new data. Data read from others must be accepted and kept, even with codes unknown to the enum, unless the enum is first regenerated from the current release. Systems should read the current release for the label of a new code (VOC-037).

## Mappings

- Reuse an authority scheme first, such as a government reference standard or an EU Vocabularies table, and map a new scheme to it (should, VOC-040).
- Use the mapping property that fits: `exactMatch` only when the concepts are interchangeable in every use, otherwise `closeMatch`, `broadMatch`, `narrowMatch` or `relatedMatch` (VOC-041).
- Map to the URI the authority publishes. Never make up a URI in another body's domain. For lists without URIs, such as ISO 3166, map to a public scheme that carries the codes (VOC-042).
- Never use `owl:sameAs`. Never combine `exactMatch` with `broadMatch`, `narrowMatch` or `relatedMatch` for one pair. Never map within one scheme (VOC-043).
- Must name each outside scheme with `dct:references` and must record the release checked; should recheck after each outside release (VOC-044).

## Publishing

- Publish each release as Turtle and JSON-LD 1.1 with the same statements, in UTF-8, named `<scheme-name>.ttl` and `.jsonld` (VOC-050).
- Turtle should be the source under version control. Other files must be generated from the source (VOC-051).
- Publish a CSV per RFC 4180 with the columns `uri,code,labelEn,labelFr,definitionEn,definitionFr,broader,deprecated,replacedBy`, one row per concept (VOC-052).
- The scheme must state labels, definition, `dct:publisher`, `dct:license`, version and date. FPSOT schemes must use an open license (VOC-053).
- A release must pass automatic checks of the SKOS integrity conditions and of the testable MUST rules (VOC-054).
- Every URI must resolve over `https`, to a page in both languages for people and to RDF for programs (VOC-055).

## Binding in data models

- A LinkML field that holds a code must have as range an enum for its scheme, except under VOC-065. The enum check applies to new data; data read from others follows VOC-037 (VOC-060).
- Each permissible value's name must be the code, and its `meaning` the concept URI, with a declared prefix. The `enum_uri` must stay in the model's own namespace, and `see_also` must give the scheme URI (VOC-061).
- The enum must list every concept, deprecated ones with `deprecated` and, for one replacement, `deprecated_element_has_exact_replacement` (VOC-062).
- Generate the enum from the Turtle file. Its description must name the scheme release (VOC-063).
- JSON and tabular records must store the code, never the URI or label. RDF data may reference the concept URI. Screens must show the scheme's label (VOC-064).
- For very large or fast-changing schemes, a field may use `CodeValue`, and the system must then check codes against the scheme (VOC-065).
