#!/usr/bin/env python3
"""Static validation of the Industrial Problem Atlas. No dependencies."""
import json
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
VALID_STATUS = {'concept', 'needs_data', 'pilot', 'validated'}
VALID_EVIDENCE = {'illustrative', 'public_source', 'authorized_observation', 'measured'}
FIELDS = ['id', 'title_fa', 'title_en', 'sector', 'status', 'evidence_level',
          'updated', 'summary_fa', 'problem_fa', 'why_it_matters', 'data_needed',
          'baseline_methods', 'advanced_options', 'evaluation', 'risks',
          'next_steps', 'student_challenge', 'org_questions', 'references']
LIST_FIELDS = {'data_needed', 'baseline_methods', 'advanced_options',
               'evaluation', 'risks', 'next_steps', 'org_questions'}
PAGES = ['index.html', 'problem.html', 'students.html',
         'organizations.html', 'methodology.html']


def ensure(condition, message, errors):
    if not condition:
        errors.append(message)


class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('a', 'script', 'link'):
            val = attrs.get('href') if tag != 'script' else attrs.get('src')
            if val:
                self.links.append(val)


def main():
    errors = []
    catalog = json.loads((ROOT / 'data/problems.json').read_text(encoding='utf-8'))
    items = catalog.get('problems', [])
    ensure(isinstance(items, list) and bool(items), 'Catalog must be a nonempty list', errors)
    ids = set()
    for idx, p in enumerate(items):
        label = f'problem #{idx+1}'
        for field in FIELDS:
            ensure(field in p, f'{label}: missing {field}', errors)
        if any(field not in p for field in FIELDS):
            continue
        ensure(re.fullmatch(r'IPA-\d{3,5}', p['id']) is not None,
               f'{label}: invalid id', errors)
        ensure(p['id'] not in ids, f'duplicate id {p["id"]}', errors)
        ids.add(p['id'])
        ensure(p['status'] in VALID_STATUS, f'{p["id"]}: invalid status', errors)
        ensure(p['evidence_level'] in VALID_EVIDENCE,
               f'{p["id"]}: invalid evidence level', errors)
        for field in FIELDS:
            if field in LIST_FIELDS or field == 'references':
                ensure(isinstance(p[field], list), f'{p["id"]}: {field} must be list', errors)
            else:
                ensure(isinstance(p[field], str) and p[field].strip(),
                       f'{p["id"]}: {field} must be nonempty string', errors)
        if p['status'] == 'validated':
            ensure(p['evidence_level'] == 'measured',
                   f'{p["id"]}: validated requires measured evidence', errors)
            ensure(len(p['references']) > 0,
                   f'{p["id"]}: validated requires references', errors)
        if p['status'] == 'pilot':
            ensure(p['evidence_level'] in {'measured', 'authorized_observation'},
                   f'{p["id"]}: pilot requires authorized/measured evidence', errors)
        try:
            parsed = date.fromisoformat(p['updated'])
            ensure(parsed <= date.today(), f'{p["id"]}: future review date', errors)
        except (ValueError, TypeError):
            errors.append(f'{p["id"]}: invalid ISO updated date')
        for ref in p['references']:
            ensure(isinstance(ref, dict) and all(key in ref for key in ('label', 'url', 'relation')),
                   f'{p["id"]}: reference requires label, url, relation', errors)
            if isinstance(ref, dict):
                url = ref.get('url', '')
                ensure(urlparse(url).scheme == 'https', f'{p["id"]}: reference must use https', errors)
        if p.get('evidence_level') == 'illustrative':
            ensure(p.get('status') == 'concept',
                   f'{p["id"]}: illustrative case cannot claim pilot/validation', errors)

    for page in PAGES:
        path = ROOT / page
        ensure(path.is_file(), f'missing page {page}', errors)
        if not path.is_file():
            continue
        html = path.read_text(encoding='utf-8')
        ensure('lang="fa"' in html and 'dir="rtl"' in html,
               f'{page}: missing Persian RTL metadata', errors)
        parser = LinkExtractor()
        parser.feed(html)
        for link in parser.links:
            target = urlparse(link)
            if target.scheme or link.startswith('#') or link.startswith('//'):
                continue
            file_path = unquote(target.path)
            if not file_path or file_path == './':
                continue
            linked = (ROOT / file_path).resolve()
            ensure(linked.is_relative_to(ROOT.resolve()) and linked.exists(),
                   f'{page}: missing local link {link}', errors)
    required = ['assets/app.js', 'assets/style.css', 'pilot/synthetic_sensor_demo.py',
                'RUN_LOCAL.cmd', 'RUN_DEMO.cmd', 'README.md', '.nojekyll']
    for rel in required:
        ensure((ROOT / rel).exists(), f'missing required file {rel}', errors)

    if errors:
        print(f'FAILED: {len(errors)} validation error(s)')
        for message in errors:
            print(' -', message)
        return 1
    print(f'PASS: {len(items)} case files validated; {len(PAGES)} pages/link checks passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
