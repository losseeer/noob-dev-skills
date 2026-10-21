#!/usr/bin/env python3
"""Validate schemas, page references, and bundled examples.

Run from inside scripts/ (it imports validate_artifact), or via absolute path.

    python validate_bundle.py            # validate schemas + rules + examples
    python validate_bundle.py --selftest # validate this checker itself
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Callable

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from validate_artifact import load_yaml, SCHEMA_FILES


def check_page_files(docs: dict) -> list[str]:
    files = docs.get("page_files") or set()
    failures: list[str] = []
    for page in (docs.get("current") or {}).get("pages") or []:
        if page.get("file") not in files:
            failures.append(
                f"pages: listed file {page.get('file')!r} does not exist in the example"
            )
    return failures


def check_upstream_gaps_declared(docs: dict) -> list[str]:
    """上游契约缺失时必须显式记一条 gap，否则就是把降级藏起来了。"""
    current = docs.get("current") or {}
    upstream = current.get("upstream") or {}
    failures: list[str] = []
    for key, entry in upstream.items():
        status = (entry or {}).get("status")
        if status not in ("not_found", "skipped"):
            continue
        gaps = current.get("gaps") or []
        declared = any(
            (gap or {}).get("kind") in ("interface", "acceptance", "requirement")
            and (gap or {}).get("reason")
            for gap in gaps
        )
        if not declared:
            failures.append(
                f"upstream.{key} is {status} but no gap records it: "
                "the prototype must state what it could not align against"
            )
    return failures


def check_pages_cover_something(docs: dict) -> list[str]:
    failures: list[str] = []
    for page in (docs.get("current") or {}).get("pages") or []:
        if not page.get("covers"):
            failures.append(
                f"pages: {page.get('file')!r} covers no requirement or acceptance"
            )
    return failures


ALL_CHECKS: list[Callable[[dict], list[str]]] = [
    check_page_files,
    check_upstream_gaps_declared,
    check_pages_cover_something,
]


def run_checks(docs: dict) -> list[str]:
    failures: list[str] = []
    for check in ALL_CHECKS:
        failures.extend(check(docs))
    return failures


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    schema_dir = root / "schemas"
    rules_dir = root / "rules"
    example_dir = root / "examples"

    failures: list[str] = []
    schemas = {
        path.name: load_yaml(path) for path in sorted(schema_dir.glob("*.yaml"))
    }
    for name, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            failures.append(f"schemas/{name}: invalid JSON Schema: {exc.message}")

    if not list(schema_dir.glob("*.yaml")):
        failures.append("schemas: no schema files found")
    if not list(rules_dir.glob("*.yaml")):
        failures.append("rules: no rule files found")

    for case_dir in sorted(path for path in example_dir.iterdir() if path.is_dir()):
        index_path = case_dir / "current.yaml"
        if not index_path.exists():
            failures.append(f"{index_path}: missing required example artifact")
            continue
        artifact = load_yaml(index_path)
        validator = Draft202012Validator(
            schemas["current.schema.yaml"], format_checker=FormatChecker()
        )
        for error in validator.iter_errors(artifact):
            pointer = "/".join(str(part) for part in error.path) or "$"
            failures.append(f"current.yaml:{pointer}: {error.message}")

        docs = {
            "current": artifact,
            "page_files": {
                path.name
                for path in (case_dir / "pages").rglob("*")
                if path.is_file()
            },
        }
        failures.extend(run_checks(docs))

    if failures:
        print("Bundle validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        "Bundle validation passed: schemas, page references, "
        "and examples are consistent."
    )
    return 0


BASE_CURRENT = {
    "version": 1,
    "as_of": "2026-10-21",
    "project": "demo",
    "upstream": {
        "interfaces": {
            "status": "found",
            "ref": ".project/design/tech/interfaces.yaml",
        }
    },
    "stack": "html",
    "pages": [
        {
            "name": "home",
            "file": "index.html",
            "covers": ["REQ-001"],
            "review_status": "pending",
        }
    ],
    "gaps": [],
    "status": "draft",
}

BASE_DOCS = {"current": BASE_CURRENT, "page_files": {"index.html"}}


def _mutate(**changes: object) -> dict:
    docs = copy.deepcopy(BASE_DOCS)
    for key, value in changes.items():
        docs[key] = copy.deepcopy(value)
    return docs


def selftest_cases() -> list[tuple[str, dict, list[str]]]:
    cases: list[tuple[str, dict, list[str]]] = [
        ("benign prototype should pass", BASE_DOCS, []),
    ]

    missing_file = copy.deepcopy(BASE_CURRENT)
    missing_file["pages"][0]["file"] = "gone.html"
    cases.append(
        (
            "page without file should fail",
            _mutate(current=missing_file, page_files={"index.html"}),
            ["gone.html"],
        )
    )

    no_interfaces = copy.deepcopy(BASE_CURRENT)
    no_interfaces["upstream"]["interfaces"] = {"status": "not_found"}
    cases.append(
        (
            "missing interfaces without a gap should fail",
            _mutate(current=no_interfaces),
            ["gap"],
        )
    )

    declared = copy.deepcopy(no_interfaces)
    declared["gaps"] = [
        {
            "kind": "interface",
            "ref": "tech/interfaces.yaml",
            "reason": "没有接口契约，页面状态只按用户描述做，未与错误码对齐",
        }
    ]
    cases.append(("missing interfaces with a declared gap should pass", _mutate(current=declared), []))

    uncovered = copy.deepcopy(BASE_CURRENT)
    uncovered["pages"][0]["covers"] = []
    cases.append(
        (
            "page covering nothing should fail",
            _mutate(current=uncovered),
            ["covers"],
        )
    )

    return cases


def selftest() -> int:
    passed = 0
    failed = 0
    for name, docs, expected_markers in selftest_cases():
        failures = run_checks(docs)
        missing = [
            marker
            for marker in expected_markers
            if not any(marker in failure for failure in failures)
        ]
        if expected_markers and not failures:
            print(f"  [FAIL] {name}: expected failures, got none")
            failed += 1
        elif not expected_markers and failures:
            print(f"  [FAIL] {name}: unexpected failures: {failures}")
            failed += 1
        elif missing:
            print(f"  [FAIL] {name}: did not detect {', '.join(missing)}")
            failed += 1
        else:
            print(f"  [ok  ] {name}")
            passed += 1

    print(f"selftest: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    raise SystemExit(main())
