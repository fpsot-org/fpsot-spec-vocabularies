# SPDX-License-Identifier: Apache-2.0
"""Checks a SKOS scheme in Turtle against the testable MUST rules of the FPSOT
vocabularies specification, and checks that a LinkML enum matches the scheme.

Usage:
  check-scheme.py SCHEME.ttl [MODEL.yaml ENUM]   check; prints findings, exit 1 if any
  check-scheme.py --csv SCHEME.ttl               print the CSV file of VOC-052
  check-scheme.py --jsonld SCHEME.ttl            print the JSON-LD file of VOC-050

Needs rdflib and PyYAML (both come with LinkML).
"""
import csv
import json
import re
import sys

import yaml
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, SKOS, XSD

KEBAB = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
NOTE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]+\.[0-9]+\.[0-9]+ ?:")
LANGS = ("en", "fr")


def plain_notations(g, c):
    return [n for n in g.objects(c, SKOS.notation)
            if isinstance(n, Literal) and n.language is None and n.datatype in (None, XSD.string)]


def texts(g, s, p, lang):
    return [str(o) for o in g.objects(s, p) if isinstance(o, Literal) and o.language == lang]


def deprecated(g, c):
    return any(o.toPython() is True for o in g.objects(c, OWL.deprecated))


def check(g):
    out = []
    schemes = list(g.subjects(RDF.type, SKOS.ConceptScheme))
    if len(schemes) != 1:
        return [f"VOC-001: expected one concept scheme, found {len(schemes)}"]
    scheme = schemes[0]
    base = str(scheme)
    concepts = sorted(g.subjects(RDF.type, SKOS.Concept))
    collections = sorted(g.subjects(RDF.type, SKOS.Collection)) + sorted(g.subjects(RDF.type, SKOS.OrderedCollection))
    if not base.startswith("https://"):
        out.append(f"VOC-002: scheme URI {base} does not use https")
    name = base.rstrip("/").rsplit("/", 1)[-1]
    if not KEBAB.match(name):
        out.append(f"VOC-002: scheme name {name} is not kebab-case")
    # Scheme description, VOC-010, VOC-015, VOC-035, VOC-053.
    for lang in LANGS:
        if len(texts(g, scheme, SKOS.prefLabel, lang)) != 1:
            out.append(f"VOC-010: scheme needs exactly one prefLabel@{lang}")
        if not texts(g, scheme, SKOS.definition, lang):
            out.append(f"VOC-053: scheme needs a definition@{lang}")
    for p, rule in ((DCTERMS.publisher, "VOC-053"), (DCTERMS.license, "VOC-053"), (DCTERMS.modified, "VOC-035")):
        if g.value(scheme, p) is None:
            out.append(f"{rule}: scheme lacks {p}")
    version = g.value(scheme, OWL.versionInfo)
    if version is None or not SEMVER.match(str(version)):
        out.append(f"VOC-035: scheme version {version} is not a semantic version")
    codes = {}
    labels = {lang: {} for lang in LANGS}
    for c in concepts:
        cs = str(c)
        if (c, SKOS.inScheme, scheme) not in g:
            out.append(f"VOC-001: {cs} is not in the scheme")
        notes = plain_notations(g, c)
        if len(notes) != 1:
            out.append(f"VOC-005: {cs} needs exactly one plain notation, has {len(notes)}")
            continue
        code = str(notes[0])
        if code in codes:
            out.append(f"VOC-005: code {code} is used twice")
        codes[code] = c
        if cs != f"{base}/concepts/{code}":
            out.append(f"VOC-003: {cs} is not the scheme URI, /concepts/, then the code {code}")
        for lang in LANGS:
            pref = texts(g, c, SKOS.prefLabel, lang)
            if len(pref) != 1:
                out.append(f"VOC-010: {cs} needs exactly one prefLabel@{lang}")
            elif pref[0] in labels[lang]:
                out.append(f"VOC-012: {cs} and {labels[lang][pref[0]]} share the label {pref[0]!r}@{lang}")
            else:
                labels[lang][pref[0]] = cs
            if not texts(g, c, SKOS.definition, lang):
                out.append(f"VOC-015: {cs} needs a definition@{lang}")
            kinds = [set(texts(g, c, p, lang)) for p in (SKOS.prefLabel, SKOS.altLabel, SKOS.hiddenLabel)]
            if (kinds[0] & kinds[1]) or (kinds[0] & kinds[2]) or (kinds[1] & kinds[2]):
                out.append(f"VOC-013: {cs} has one text in two label kinds@{lang}")
            for n in texts(g, c, SKOS.changeNote, lang):
                if not NOTE.match(n):
                    out.append(f"VOC-034: change note of {cs} does not start with a date and a version: {n!r}")
        broader = set(g.objects(c, SKOS.broader))
        if not broader and (c, SKOS.topConceptOf, scheme) not in g:
            out.append(f"VOC-020: {cs} has no broader concept and is not a top concept")
        if (c, SKOS.topConceptOf, scheme) in g and (scheme, SKOS.hasTopConcept, c) not in g:
            out.append(f"VOC-020: scheme does not state hasTopConcept {cs}")
        for b in broader:
            if (b, SKOS.narrower, c) not in g:
                out.append(f"VOC-021: {b} does not state narrower {cs}")
            if (b, SKOS.inScheme, scheme) not in g:
                out.append(f"VOC-021: broader concept {b} of {cs} is outside the scheme")
        for n in g.objects(c, SKOS.narrower):
            if (n, SKOS.broader, c) not in g:
                out.append(f"VOC-021: {n} does not state broader {cs}")
        if deprecated(g, c):
            if not list(g.objects(c, SKOS.changeNote)):
                out.append(f"VOC-031: deprecated {cs} has no change note")
            if g.value(c, DCTERMS.modified) is None:
                out.append(f"VOC-034: deprecated {cs} has no dct:modified")
        for r in g.objects(c, DCTERMS.isReplacedBy):
            if (r, DCTERMS.replaces, c) not in g:
                out.append(f"VOC-031: {r} does not state replaces {cs}")
            if not deprecated(g, c):
                out.append(f"VOC-031: {cs} is replaced but not deprecated")
        if list(g.objects(c, OWL.sameAs)):
            out.append(f"VOC-043: {cs} uses owl:sameAs")
        exact = set(g.objects(c, SKOS.exactMatch))
        if exact & (set(g.objects(c, SKOS.broadMatch)) | set(g.objects(c, SKOS.relatedMatch))):
            out.append(f"VOC-043: {cs} has an exact match that is also a broad or related match")
        for p in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch, SKOS.narrowMatch, SKOS.relatedMatch):
            for m in g.objects(c, p):
                if (m, SKOS.inScheme, scheme) in g:
                    out.append(f"VOC-043: {cs} maps to {m} in its own scheme")
                if not any(str(m).startswith(str(ref)) for ref in g.objects(scheme, DCTERMS.references)):
                    out.append(f"VOC-044: {cs} maps to {m}, whose scheme is not named with dct:references")
    # VOC-022: no cycle in broader links. VOC-023: related not on a broader chain.
    def ancestors(c):
        seen, todo = set(), list(g.objects(c, SKOS.broader))
        while todo:
            b = todo.pop()
            if b not in seen:
                seen.add(b)
                todo.extend(g.objects(b, SKOS.broader))
        return seen
    for c in concepts:
        up = ancestors(c)
        if c in up:
            out.append(f"VOC-022: {c} is its own broader concept")
        for r in g.objects(c, SKOS.related):
            if r in up or c in ancestors(r):
                out.append(f"VOC-023: {c} and {r} are related and on one broader chain")
    for col in collections:
        if not str(col).startswith(f"{base}/collections/"):
            out.append(f"VOC-003: collection {col} is not under {base}/collections/")
        for lang in LANGS:
            if len(texts(g, col, SKOS.prefLabel, lang)) != 1:
                out.append(f"VOC-010: collection {col} needs exactly one prefLabel@{lang}")
    return out


def check_enum(g, model_path, enum_name):
    out = []
    model = yaml.safe_load(open(model_path, encoding="utf-8"))
    prefixes = model.get("prefixes", {})
    enum = model["enums"][enum_name]
    scheme = next(g.subjects(RDF.type, SKOS.ConceptScheme))
    if enum.get("enum_uri") != str(scheme):
        out.append(f"VOC-061: enum_uri {enum.get('enum_uri')} is not the scheme URI {scheme}")
    version = str(g.value(scheme, OWL.versionInfo))
    if f"release {version}" not in enum.get("description", ""):
        out.append(f"VOC-063: enum description does not name release {version}")

    def expand(curie):
        p, _, local = curie.partition(":")
        return prefixes[p] + local if p in prefixes else curie

    pvs = enum.get("permissible_values", {})
    concepts = {str(plain_notations(g, c)[0]): c for c in g.subjects(RDF.type, SKOS.Concept)}
    for code, c in concepts.items():
        pv = pvs.get(code)
        if pv is None:
            out.append(f"VOC-062: enum lacks the code {code}")
            continue
        if expand(pv.get("meaning", "")) != str(c):
            out.append(f"VOC-061: meaning of {code} is not {c}")
        if deprecated(g, c) != bool(pv.get("deprecated")):
            out.append(f"VOC-062: deprecated mark of {code} does not match the scheme")
        repl = list(g.objects(c, DCTERMS.isReplacedBy))
        if len(repl) == 1 and expand(pv.get("deprecated_element_has_exact_replacement", "")) != str(repl[0]):
            out.append(f"VOC-062: {code} lacks its replacement {repl[0]}")
    for code in pvs:
        if code not in concepts:
            out.append(f"VOC-062: enum code {code} is not in the scheme")
    return out


def sort_values(node):
    """Sorts the values of each property, so that the JSON-LD output is stable."""
    for k, v in node.items():
        if isinstance(v, list):
            node[k] = sorted(v, key=lambda x: json.dumps(x, sort_keys=True))
    return node


def write_csv(g):
    w = csv.writer(sys.stdout, lineterminator="\r\n")
    w.writerow(["uri", "code", "labelEn", "labelFr", "definitionEn", "definitionFr", "broader", "deprecated", "replacedBy"])
    for c in sorted(g.subjects(RDF.type, SKOS.Concept)):
        def one(p, lang):
            v = texts(g, c, p, lang)
            return v[0] if v else ""
        w.writerow([str(c), str(plain_notations(g, c)[0]),
                    one(SKOS.prefLabel, "en"), one(SKOS.prefLabel, "fr"),
                    one(SKOS.definition, "en"), one(SKOS.definition, "fr"),
                    " ".join(sorted(str(b) for b in g.objects(c, SKOS.broader))),
                    "true" if deprecated(g, c) else "false",
                    " ".join(sorted(str(r) for r in g.objects(c, DCTERMS.isReplacedBy)))])


def main(argv):
    if len(argv) == 3 and argv[1] in ("--csv", "--jsonld"):
        g = Graph().parse(argv[2], format="turtle")
        if argv[1] == "--csv":
            write_csv(g)
        else:
            keep = ("skos", "dct", "owl", "xsd")
            context = {p: str(ns) for p, ns in g.namespaces() if p in keep}
            doc = json.loads(g.serialize(format="json-ld", context=context))
            doc["@graph"] = sorted((sort_values(n) for n in doc["@graph"]), key=lambda n: n["@id"])
            print(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if len(argv) not in (2, 4):
        print(__doc__, file=sys.stderr)
        return 2
    g = Graph().parse(argv[1], format="turtle")
    findings = check(g)
    if len(argv) == 4:
        findings += check_enum(g, argv[2], argv[3])
    for f in findings:
        print(f)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
