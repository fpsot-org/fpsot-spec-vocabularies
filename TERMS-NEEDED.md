# Terms needed

Entries for the term base of `fpsot-spec-writing` (`termbase/terms.yaml`), in its format.
This specification uses them as `{abbr-skos}`, `{abbr-rdf}`, `{abbr-json-ld}` and `{abbr-csv}`.

```yaml
  - id: csv
    kind: abbreviation
    en: {short: "CSV", full: "comma-separated values", definition: "A plain text format for tables, with one record per line and commas between the fields."}
    fr: {short: "CSV", full: "valeurs séparées par des virgules", definition: "Format de texte brut pour les tableaux, avec un enregistrement par ligne et des virgules entre les champs."}
    source: {name: "Grand dictionnaire terminologique", url: "https://vitrinelinguistique.oqlf.gouv.qc.ca/fiche-gdt/fiche/8362519/fichier-csv", checked: "2026-11-05"}
  - id: json-ld
    kind: abbreviation
    en: {short: "JSON-LD", full: "JSON for Linking Data", definition: "A W3C format that writes linked data as JSON, so that JSON tools can read it."}
    fr: {short: "JSON-LD", full: "JSON for Linking Data", definition: "Format du W3C qui écrit des données liées en JSON, pour que les outils JSON puissent les lire."}
    source: {name: "W3C, JSON-LD 1.1 (no GDT record found; TERMIUM Plus could not be read)", url: "https://www.w3.org/TR/json-ld11/", checked: "2026-11-05"}
  - id: rdf
    kind: abbreviation
    en: {short: "RDF", full: "Resource Description Framework", definition: "The W3C model that describes resources as statements, each made of a subject, a property and a value."}
    fr: {short: "RDF", full: "Resource Description Framework", definition: "Modèle du W3C qui décrit des ressources par des énoncés, chacun formé d'un sujet, d'une propriété et d'une valeur."}
    source: {name: "W3C, RDF 1.1 Concepts and Abstract Syntax (no GDT record found; TERMIUM Plus could not be read)", url: "https://www.w3.org/TR/rdf11-concepts/", checked: "2026-11-05"}
  - id: skos
    kind: abbreviation
    en: {short: "SKOS", full: "Simple Knowledge Organization System", definition: "The W3C model for publishing code lists, classifications and thesauri as linked data."}
    fr: {short: "SKOS", full: "Simple Knowledge Organization System", definition: "Modèle du W3C qui sert à publier des listes de codes, des classifications et des thésaurus sous forme de données liées."}
    source: {name: "W3C, SKOS Reference (no GDT record found; TERMIUM Plus could not be read)", url: "https://www.w3.org/TR/skos-reference/", checked: "2026-11-05"}
```

The French full form of CSV comes from the Grand dictionnaire terminologique record « fichier CSV », which glosses CSV as « valeurs séparées par des virgules ».
No record was found in the Grand dictionnaire terminologique for SKOS, RDF or JSON-LD, and TERMIUM Plus refused automated reads.
These entries keep the English full form in French, as the term base does for ARIA.
The project lead should check these forms.
