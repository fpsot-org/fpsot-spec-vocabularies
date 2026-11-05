# Changelog

All notable changes to this specification are listed here.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `AGENTS.md`, a book per language (`spec/<lang>/book.adoc`) ending with the glossary, and a document history on each page.
- Example requirement TPL-001 and an example comparison row in `jurisdictions/baseline.yaml`.
- `.gitignore` for the files that the continuous integration writes.

### Changed

- The continuous integration runs the documentation checks, and releases can attach the PDF books.
- Pages include the term base attributes. The guide page has a page type.
- The French conformance section quotes RFC 8174 and points to WRT-011.
- `NOTICE` spells out FPSOT. `NOTICES.md` names the Code of Conduct contact.
