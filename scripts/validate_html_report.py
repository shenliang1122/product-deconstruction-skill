#!/usr/bin/env python3
"""Validate a standalone evidence-driven HTML report without an HTML4 parser."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

PLACEHOLDER_PATTERNS = (
    re.compile(r"\b(?:TODO|TBD|PLACEHOLDER)\b", re.IGNORECASE),
    re.compile(r"\{\{[^{}]+\}\}"),
)

SECRET_PATTERNS = (
    ("Bearer token", re.compile(r"Authorization\s*:\s*Bearer\s+\S+", re.IGNORECASE)),
    ("client secret", re.compile(r"client[_-]?secret\s*[:=]\s*['\"]?[^\s'\"<]+", re.IGNORECASE)),
    ("access token", re.compile(r"access[_-]?token\s*[:=]\s*['\"]?[^\s'\"<]+", re.IGNORECASE)),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\b")),
)


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.ids: list[str] = []
        self.refs: list[tuple[str, str, int]] = []
        self.has_charset = False
        self.has_viewport = False

    def handle_decl(self, decl: str) -> None:
        return

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        line, _ = self.getpos()
        attr_map = {key.lower(): value for key, value in attrs}
        element_id = attr_map.get("id")
        if element_id:
            self.ids.append(element_id)
        for key in ("href", "src"):
            value = attr_map.get(key)
            if value:
                self.refs.append((key, value, line))
        if tag == "meta":
            if (attr_map.get("charset") or "").lower() == "utf-8":
                self.has_charset = True
            if (attr_map.get("name") or "").lower() == "viewport":
                self.has_viewport = True
        if tag not in VOID_TAGS:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        tag = tag.lower()
        if tag not in VOID_TAGS and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        line, _ = self.getpos()
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"line {line}: unexpected closing </{tag}>")
            return
        open_tag, open_line = self.stack[-1]
        if open_tag == tag:
            self.stack.pop()
            return
        candidates = [index for index, item in enumerate(self.stack) if item[0] == tag]
        if not candidates:
            self.errors.append(
                f"line {line}: closing </{tag}> has no matching opening tag "
                f"(current <{open_tag}> opened on line {open_line})"
            )
            return
        index = candidates[-1]
        unclosed = self.stack[index + 1 :]
        self.errors.append(
            f"line {line}: closing </{tag}> before "
            + ", ".join(f"<{name}> from line {start}" for name, start in unclosed)
        )
        del self.stack[index:]


def is_local_reference(value: str) -> bool:
    if value.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return False
    split = urlsplit(value)
    return not split.scheme and not split.netloc


def validate(report_path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = report_path.read_text(encoding="utf-8")
    parser = ReportParser()
    parser.feed(text)
    parser.close()

    errors.extend(parser.errors)
    for tag, line in parser.stack:
        errors.append(f"line {line}: unclosed <{tag}>")

    if not re.search(r"<!doctype\s+html", text, re.IGNORECASE):
        errors.append("missing <!doctype html>")
    if not parser.has_charset:
        errors.append("missing <meta charset=\"utf-8\">")
    if not parser.has_viewport:
        errors.append("missing viewport meta tag")

    duplicate_ids = sorted(item for item, count in Counter(parser.ids).items() if count > 1)
    if duplicate_ids:
        errors.append("duplicate id values: " + ", ".join(duplicate_ids))

    missing_refs: list[str] = []
    local_refs = 0
    for attr, value, line in parser.refs:
        if not is_local_reference(value):
            continue
        local_refs += 1
        path_part = unquote(urlsplit(value).path)
        target = (report_path.parent / path_part).resolve()
        if not target.exists():
            missing_refs.append(f"line {line}: {attr}=\"{value}\"")
    if missing_refs:
        errors.append("missing local references:\n  " + "\n  ".join(missing_refs))

    placeholders = []
    for pattern in PLACEHOLDER_PATTERNS:
        placeholders.extend(match.group(0) for match in pattern.finditer(text))
    if placeholders:
        unique = sorted(set(placeholders))
        errors.append("unfinished placeholders: " + ", ".join(unique[:12]))

    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"possible embedded secret: {label}")

    if "@media print" not in text:
        warnings.append("no print stylesheet detected")
    if not re.search(r"@media\s*\([^)]*max-width", text, re.IGNORECASE):
        warnings.append("no narrow-screen media query detected")
    if "【尚未确认】" not in text and "尚未确认" not in text:
        warnings.append("no visible unknown-evidence language detected")

    stats = {
        "bytes": len(text.encode("utf-8")),
        "lines": text.count("\n") + 1,
        "ids": len(parser.ids),
        "local_references": local_refs,
        "external_references": len(parser.refs) - local_refs,
    }
    return errors, warnings, stats


def main() -> int:
    argument_parser = argparse.ArgumentParser(
        description="Validate a standalone evidence-driven HTML report."
    )
    argument_parser.add_argument("report", type=Path, help="Path to the HTML report")
    args = argument_parser.parse_args()
    report_path = args.report.expanduser().resolve()

    if not report_path.is_file():
        print(f"FAIL: report not found: {report_path}", file=sys.stderr)
        return 2
    if report_path.suffix.lower() not in {".html", ".htm"}:
        print(f"FAIL: expected an HTML file: {report_path}", file=sys.stderr)
        return 2

    try:
        errors, warnings, stats = validate(report_path)
    except UnicodeDecodeError as exc:
        print(f"FAIL: report is not UTF-8: {exc}", file=sys.stderr)
        return 1

    print(f"Report: {report_path}")
    print(
        "Stats: "
        + ", ".join(f"{name}={value}" for name, value in stats.items())
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: HTML structure and local evidence references are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
