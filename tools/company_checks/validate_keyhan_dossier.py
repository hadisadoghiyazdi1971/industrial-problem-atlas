#!/usr/bin/env python3
"""Validate the Keyhan Sanat Ghaem dossier without network access.

Invariant checks validate structure and evidence relationships without assuming
fixed counts. Snapshot checks compare explicitly historical 2026-10-30 receipt
counts and hashes. Neither mode modifies historical receipts.
"""
from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import json
import re
import threading
from collections import Counter
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
COMPANY = ROOT / "companies" / "keyhan-sanat-ghaem"
RESEARCH = COMPANY / "research"
SNAPSHOT_PATH = Path(__file__).with_name("keyhan_sanat_snapshot.json")
EVIDENCE_TYPES = {"FACT_PUBLIC", "ENGINEERING_INFERENCE", "OPPORTUNITY_HYPOTHESIS", "UNKNOWN"}


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.lang = None
        self.direction = None
        self.viewport = False
        self.refresh = None
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
            self.direction = attrs.get("dir")
        if tag in {"a", "link", "script"}:
            target = attrs.get("src") if tag == "script" else attrs.get("href")
            if target:
                self.links.append(target)
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = True
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refresh = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")


class Validation:
    def __init__(self, mode):
        self.mode = mode
        self.checks = []
        self.failures = []

    def check(self, name, condition, detail=None, group="invariant"):
        record = {"group": group, "name": name, "passed": bool(condition)}
        if detail is not None:
            record["detail"] = detail
        self.checks.append(record)
        if not condition:
            self.failures.append(f"{group}:{name}")


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def problem_hash(problem):
    payload = json.dumps(problem, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_local_links(validation, documents):
    links = []
    parser_cache = {}
    for path in documents:
        content = path.read_text(encoding="utf-8")
        parser = DocumentParser()
        parser.feed(content)
        parser_cache[path] = parser
        validation.check(f"rtl:{path.relative_to(ROOT)}", parser.lang == "fa" and parser.direction == "rtl")
        validation.check(f"viewport:{path.relative_to(ROOT)}", parser.viewport)
        links.extend((path, link) for link in parser.links)

    for path in COMPANY.rglob("*.md"):
        if "crawl_runs" in path.parts:
            continue
        links.extend((path, link) for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")))

    broken = []
    broken_fragments = []
    for source, link in links:
        target = urlsplit(link)
        if target.scheme or link.startswith("//"):
            continue
        path = (source.parent / unquote(target.path)).resolve() if target.path else source
        if not path.is_relative_to(ROOT) or not path.exists():
            broken.append(f"{source.relative_to(ROOT)}: {link}")
            continue
        if path.is_dir():
            path = path / "index.html"
        if target.fragment and path.suffix == ".html":
            parser = parser_cache.get(path)
            if parser is None:
                parser = DocumentParser()
                parser.feed(path.read_text(encoding="utf-8"))
                parser_cache[path] = parser
            if unquote(target.fragment) not in parser.ids:
                broken_fragments.append(f"{source.relative_to(ROOT)}: {link}")
    validation.check("local_links", not broken, {"checked": len(links), "broken": broken})
    validation.check("local_fragments", not broken_fragments, broken_fragments)


def validate_evidence(validation):
    sources = read_csv(RESEARCH / "SOURCES.csv")
    claims = read_csv(RESEARCH / "EVIDENCE_LEDGER.csv")
    source_ids = {row["source_id"]: row for row in sources}
    claim_ids = {row["claim_id"]: row for row in claims}
    validation.check("source_ids_unique", len(source_ids) == len(sources))
    validation.check("claim_ids_unique", len(claim_ids) == len(claims))
    required = {"claim_fa", "source_url", "exact_location", "observed_date", "evidence_type", "confidence", "source_id", "excerpt_or_paraphrase", "verification_limits"}
    validation.check("evidence_schema", all(required <= set(row) and all(row[key] for key in required) and row["evidence_type"] in EVIDENCE_TYPES for row in claims))
    validation.check("source_references", all(row["source_id"] in source_ids and row["source_url"] == source_ids[row["source_id"]]["url"] for row in claims))
    validation.check("parent_references", all(parent in claim_ids for row in claims for parent in row["parent_claim_ids"].split(";") if parent))

    visiting = set()
    visited = set()
    def visit(claim_id):
        if claim_id in visiting:
            raise ValueError("evidence cycle")
        if claim_id in visited:
            return
        visiting.add(claim_id)
        for parent in claim_ids[claim_id]["parent_claim_ids"].split(";"):
            if parent:
                visit(parent)
        visiting.remove(claim_id)
        visited.add(claim_id)
    try:
        for claim_id in claim_ids:
            visit(claim_id)
        acyclic = True
    except (KeyError, ValueError):
        acyclic = False
    validation.check("evidence_graph_acyclic", acyclic)
    validation.check("unknowns_marked_unverifiable", all(row["confidence"] == "NOT_PUBLICLY_VERIFIABLE" for row in claims if row["evidence_type"] == "UNKNOWN"))

    referenced = set()
    for path in COMPANY.rglob("*.md"):
        if "crawl_runs" not in path.parts:
            referenced.update(re.findall(r"\bE\d{2}\b", path.read_text(encoding="utf-8")))
    validation.check("document_evidence_ids", referenced <= set(claim_ids), sorted(referenced - set(claim_ids)))
    return sources, claims


def invariant_checks(validation):
    required = [
        COMPANY / "index.html",
        COMPANY / "management-brief.html",
        RESEARCH / "RESEARCH_REPORT_FA.md",
        RESEARCH / "EVIDENCE_LEDGER.csv",
        RESEARCH / "OPPORTUNITY_REGISTER.md",
        COMPANY / "proposals" / "IPA-004_PROPOSAL_FA.md",
        COMPANY / "outreach" / "DRAFT_EMAIL_FA.md",
    ]
    validation.check("required_files", all(path.is_file() for path in required), [str(path.relative_to(ROOT)) for path in required if not path.is_file()])
    documents = [COMPANY / "index.html", COMPANY / "management-brief.html", ROOT / "companies" / "index.html", ROOT / "cases" / "keyhan-sanat-ghaem.html"]
    validate_local_links(validation, documents)
    sources, claims = validate_evidence(validation)

    landing = (COMPANY / "index.html").read_text(encoding="utf-8")
    brief = (COMPANY / "management-brief.html").read_text(encoding="utf-8")
    validation.check("landing_links_management_brief", 'href="management-brief.html"' in landing)
    validation.check("landing_has_no_internal_research_links", not re.search(r'href="(?:research|proposals|outreach)/', landing))
    validation.check("management_brief_print_css", "@page" in brief and "size:A4" in brief and "@media print" in brief)
    validation.check("management_brief_decision_sections", all(text in brief for text in ["تصمیم مورد بررسی", "چه داده‌ای حداقل لازم است؟", "آزمون چقدر محدود است؟", "چه نتیجه‌ای سبب توقف می‌شود؟"]))
    validation.check("management_brief_limits_claims", all(text in brief for text in ["هیچ داده داخلی", "بدون فرمان به دستگاه", "بدون پیش‌فرض وجود مشکل"]))

    catalog = json.loads((ROOT / "data" / "problems.json").read_text(encoding="utf-8"))
    ipa004 = [problem for problem in catalog["problems"] if problem["id"] == "IPA-004"]
    validation.check("ipa004_identity", len(ipa004) == 1 and ipa004[0]["status"] == "concept" and ipa004[0]["evidence_level"] == "public_source" and ipa004[0]["case_url"] == "companies/keyhan-sanat-ghaem/")
    company_index = (ROOT / "companies" / "index.html").read_text(encoding="utf-8")
    validation.check("company_index_route", 'href="keyhan-sanat-ghaem/"' in company_index)
    legacy_parser = DocumentParser()
    legacy_parser.feed((ROOT / "cases" / "keyhan-sanat-ghaem.html").read_text(encoding="utf-8"))
    validation.check("historic_redirect", legacy_parser.canonical == "../companies/keyhan-sanat-ghaem/" and legacy_parser.refresh == "0; url=../companies/keyhan-sanat-ghaem/")

    bad_encoding = []
    for path in COMPANY.rglob("*"):
        if path.is_file() and "crawl_runs" not in path.parts and path.suffix.lower() in {".md", ".csv", ".html", ".json"}:
            text = path.read_text(encoding="utf-8")
            if "\ufffd" in text or re.search(r"\?{4,}", text):
                bad_encoding.append(str(path.relative_to(ROOT)))
    validation.check("utf8_text", not bad_encoding, bad_encoding)
    validation.check("no_copied_remote_documents", not any(path.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".har"} for path in COMPANY.rglob("*")))
    return sources, claims


def snapshot_checks(validation, sources, claims):
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    validation.check("source_count", len(sources) == snapshot["source_count"], {"actual": len(sources), "expected": snapshot["source_count"]}, "snapshot")
    validation.check("evidence_count", len(claims) == snapshot["evidence_count"], {"actual": len(claims), "expected": snapshot["evidence_count"]}, "snapshot")
    actual_types = dict(Counter(row["evidence_type"] for row in claims))
    validation.check("evidence_type_counts", actual_types == snapshot["evidence_types"], {"actual": actual_types, "expected": snapshot["evidence_types"]}, "snapshot")

    discovery = RESEARCH / "discovery" / snapshot["observed_date"]
    inventory = json.loads((discovery / "public_inventory.json").read_text(encoding="utf-8"))
    sitemap = json.loads((discovery / "page_sitemap_receipt.json").read_text(encoding="utf-8"))
    api = json.loads((discovery / "advertised_page_api_receipts.json").read_text(encoding="utf-8"))["requests"]
    catalog = json.loads((discovery / "catalog_review.json").read_text(encoding="utf-8"))
    validation.check("sitemap_snapshot", len(inventory["pages"]) == len(sitemap["urls"]) == snapshot["declared_sitemap_page_count"] and {row["url"] for row in inventory["pages"]} == set(sitemap["urls"]), group="snapshot")
    validation.check("api_receipt_snapshot", len(api) == snapshot["advertised_page_api_receipt_count"], group="snapshot")
    validation.check("catalog_snapshot", all(catalog[key] == value for key, value in snapshot["catalog"].items()), {key: catalog.get(key) for key in snapshot["catalog"]}, "snapshot")

    problems = json.loads((ROOT / "data" / "problems.json").read_text(encoding="utf-8"))["problems"]
    actual_hashes = {problem["id"]: problem_hash(problem) for problem in problems if problem["id"] in snapshot["unrelated_problem_sha256"]}
    validation.check("unrelated_problem_snapshot", actual_hashes == snapshot["unrelated_problem_sha256"], {"actual": actual_hashes, "expected": snapshot["unrelated_problem_sha256"]}, "snapshot")


def loopback_http_check(validation):
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    routes = ["/", "/companies/", "/companies/keyhan-sanat-ghaem/", "/companies/keyhan-sanat-ghaem/management-brief.html", "/problem.html?id=IPA-004", "/cases/keyhan-sanat-ghaem.html", "/data/problems.json", "/assets/style.css", "/assets/app.js"]
    results = []
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        for route in routes:
            with urlopen(base + route, timeout=5) as response:
                body = response.read()
                results.append({"route": route, "status": response.status, "bytes": len(body)})
        validation.check("loopback_http_routes", all(row["status"] == 200 and row["bytes"] > 0 for row in results), results)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["invariants", "snapshot", "all"], default="all")
    parser.add_argument("--skip-http", action="store_true", help="Skip loopback HTTP route checks.")
    parser.add_argument("--json-out", type=Path, help="Optional output path; historical receipts are never changed automatically.")
    args = parser.parse_args()
    validation = Validation(args.mode)
    sources, claims = invariant_checks(validation)
    if args.mode in {"snapshot", "all"}:
        snapshot_checks(validation, sources, claims)
    if not args.skip_http:
        loopback_http_check(validation)
    result = {
        "result": "PASS" if not validation.failures else "FAIL",
        "mode": args.mode,
        "scope": "Offline invariant and optional historical snapshot checks; no remote network, browser rendering or receipt mutation.",
        "checks": validation.checks,
        "failed_checks": validation.failures,
    }
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{result['result']}: {len(validation.checks)} checks; mode={args.mode}; failures={len(validation.failures)}")
    for failure in validation.failures:
        print("FAILED:", failure)
    raise SystemExit(bool(validation.failures))


if __name__ == "__main__":
    main()
