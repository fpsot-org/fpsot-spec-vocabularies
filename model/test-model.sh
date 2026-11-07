#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
#
# Tests the example scheme and its LinkML binding:
#   - document-types.ttl passes check-scheme.py, and the DocumentType enum matches it;
#   - document-types.jsonld and document-types.csv are generated from it;
#   - every data example in examples/valid/ passes LinkML validation, and every one
#     in examples/invalid/ fails;
#   - every scheme in examples/invalid/ fails check-scheme.py.
#
# Environment: LINKML (default linkml-validate), PYTHON (default python3, with rdflib
# and PyYAML, such as the Python of the LinkML install).
set -u
here="$(cd "$(dirname "$0")" && pwd)"
linkml=${LINKML:-linkml-validate}
python=${PYTHON:-python3}
model="$here/document-types.yaml"
fail=0
if ! $python -I "$here/check-scheme.py" "$here/document-types.ttl" "$model" DocumentType; then
  echo "FAIL: document-types.ttl or its enum does not pass the checks"; fail=1
fi
for ext in jsonld csv; do
  if ! $python -I "$here/check-scheme.py" "--$ext" "$here/document-types.ttl" | cmp -s - "$here/document-types.$ext"; then
    echo "FAIL: document-types.$ext is not generated from document-types.ttl"; fail=1
  fi
done
while IFS= read -r f; do
  if ! $linkml -s "$model" -C Examples "$f" >/dev/null 2>&1; then
    echo "FAIL: valid example rejected: $f"; $linkml -s "$model" -C Examples "$f" 2>&1 | tail -3; fail=1
  fi
done < <(find "$here/examples/valid" -name '*.yaml' | sort)
while IFS= read -r f; do
  if $linkml -s "$model" -C Examples "$f" >/dev/null 2>&1; then
    echo "FAIL: invalid example accepted: $f"; fail=1
  fi
done < <(find "$here/examples/invalid" -name '*.yaml' | sort)
while IFS= read -r f; do
  if $python -I "$here/check-scheme.py" "$f" >/dev/null 2>&1; then
    echo "FAIL: invalid scheme accepted: $f"; fail=1
  fi
done < <(find "$here/examples/invalid" -name '*.ttl' | sort)
[ $fail -eq 0 ] && echo "PASS"
exit $fail
