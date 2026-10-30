#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Idempotent, conservative links-only integration of a NEW briefing, without destroying Codex files."""
import sys,re,datetime,shutil
from pathlib import Path
root=Path(__file__).resolve().parent.parent
TARGET='companies/keyhan-sanat-ghaem/briefing/index.html'
if not (root/TARGET).is_file():
 print('ERROR: extract ZIP into the repository root first.');sys.exit(2)
items=[
 ('index.html','companies/keyhan-sanat-ghaem/briefing/','<section id="problems"', 'home'),
 ('companies/index.html','keyhan-sanat-ghaem/briefing/','</main>','companies'),
 ('companies/keyhan-sanat-ghaem/index.html','briefing/','<main','case')]
marker='data-ipa-briefing-v1="ksg"'
for rel,url,anchor,kind in items:
 path=root/rel
 if not path.exists(): print('SKIP (file not found):',rel);continue
 s=path.read_text(encoding='utf-8-sig')
 if marker in s:print('ALREADY LINKED:',rel);continue
 box=f"""\n<section {marker} style="max-width:1120px;margin:24px auto;padding:18px 22px;border:1px solid #b5dcda;background:#edf8f5;border-radius:14px;line-height:2"><strong style="color:#0b5963">پرونده اختصاصی شرکت کیهان صنعت قائم — مطالعه چندلایه</strong><p style="margin:8px 0">از معرفی کوتاه برای مدیر تا نقشه فرایند، شواهد پیونددار، پنج فرصت و پروتکل قابل آزمون؛ اطلاعات عمومی، نه ادعای مشاهده عملکرد داخلی شرکت.</p><a href="{url}" style="display:inline-block;border-radius:8px;padding:7px 15px;background:#0d7880;color:white;text-decoration:none;font-weight:bold">مشاهده سخن اختصاصی و شواهد ←</a></section>\n"""
 # Respect content and insert a single small banner; no replacing existing app.js/json or case texts.
 if kind=='home':
  m=re.search(r'<section\s+id=["\']problems["\']',s,re.I)
 elif kind=='case':
  m=re.search(r'<main\b[^>]*>',s,re.I)
 else:
  m=None
 if kind=='case' and m: pos=m.end()
 elif m: pos=m.start()
 else:
  m=re.search(r'</main\s*>',s,re.I)
  if not m: print('SKIP (main not found):',rel);continue
  pos=m.start()
 backup=Path.home()/'Documents'/'IndustrialAtlasLocalBackups'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')/rel
 backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,backup)
 new=s[:pos]+box+s[pos:]
 path.write_text(new,encoding='utf-8')
 print('LINKED:',rel,'BACKUP:',backup)
print('Finished. Review changes with GitHub Desktop; no commit or push performed.')
