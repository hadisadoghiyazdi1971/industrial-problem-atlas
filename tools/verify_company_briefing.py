#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from pathlib import Path
from html.parser import HTMLParser
import json,re,sys, urllib.parse
root=Path(__file__).resolve().parent.parent
brief=root/'companies/keyhan-sanat-ghaem/briefing'
need=['index.html','evidence.html','opportunities.html','pilot.html','collaboration.html']
fail=[]
class C(HTMLParser):
 def __init__(self):super().__init__();self.anchors=[];self.ids=set();self.links=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id'in d:self.ids.add(d['id'])
  if tag=='a' and 'href'in d:self.links.append(d['href'])
for p in need:
 f=brief/p
 if not f.exists():fail.append('Missing '+str(f));continue
 s=f.read_text(encoding='utf8')
 if '<html lang="fa" dir="rtl">' not in s:fail.append(p+' RTL/language')
 if 'viewport' not in s:fail.append(p+' mobile viewport')
 v=C();v.feed(s)
 for h in v.links:
  if h.startswith(('https://','http://','mailto:','#')):continue
  url,_,fragment=h.partition('#');local=(f.parent/url) if url else f
  local=local.resolve()
  if h=='../../../':continue  # parent repo homepage exists only after overlay
  if local.is_dir():local=local/'index.html'
  if not local.is_file():fail.append(f'{p} broken link: {h}');continue
  if fragment and local.suffix=='.html':
   t=C();t.feed(local.read_text(encoding='utf8'))
   if urllib.parse.unquote(fragment) not in t.ids:fail.append(f'{p} missing anchor: {h}')
 for req in ['assets/briefing.css','assets/briefing.js']:
  if not (brief/req).is_file():fail.append('missing '+req)
profile=json.loads((brief/'data/public_profile.json').read_text(encoding='utf8'))
ids=[x['id'] for x in profile['claims']]
if len(ids)!=len(set(ids)):fail.append('duplicate public claim ids')
evid=(brief/'evidence.html').read_text(encoding='utf8')
for x in profile['claims']:
 if not x['source_url'].startswith('https://www.ksgco.com/') and not x['source_url'].startswith('https://www.ksgco.com?'):
  fail.append('unapproved source host '+x['id'])
 if f'id="{x["id"]}"' not in evid:fail.append('missing evidence card '+x['id'])
if '<script' not in (brief/'pilot.html').read_text():fail.append('demo missing')
if fail:
 print('FAILED:',*fail,sep='\n - ');sys.exit(1)
print(f'PASS: {len(need)} layered pages, {len(ids)} sourced claims, relative page links and anchors valid.')
