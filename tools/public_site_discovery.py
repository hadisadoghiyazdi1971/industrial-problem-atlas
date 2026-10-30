#!/usr/bin/env python3
"""Conservative public-site inventory. Standard-library only, no login or API guessing."""
from __future__ import annotations
import argparse
from collections import deque
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urldefrag, urlsplit, urlunsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.robotparser import RobotFileParser

AGENT = 'IndustrialProblemAtlas-PublicResearch/1.0 (https://h-sadoghi.github.io/)'
EXCLUDE = ('/wp-admin', '/admin', '/login', '/signin', '/checkout', '/cart', '/private', '/internal', '/xmlrpc')
SKIP = ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.woff', '.woff2', '.zip', '.rar', '.mp4', '.mp3')

def normalized(url):
    u=urlsplit(urldefrag(url)[0])
    return urlunsplit((u.scheme.lower(),u.netloc.lower(),u.path or '/', '', ''))

def allowed(url, hosts):
    u=urlsplit(url)
    return (u.scheme=='https' and u.hostname in hosts and not u.username and not u.password and
            not u.query and not u.fragment and not u.path.lower().endswith(SKIP) and
            not any(x in u.path.lower() for x in EXCLUDE))

class RestrictedRedirect(HTTPRedirectHandler):
    def __init__(self,hosts): super().__init__(); self.hosts=hosts
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not allowed(normalized(newurl),self.hosts): raise URLError('redirect outside public allowed domain')
        return super().redirect_request(req,fp,code,msg,headers,newurl)

class ReadPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title='';self.headings=[];self.links=[];self.public_api_links=[];self.capture=None;self.buf=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('title','h1','h2','h3'):self.capture=tag;self.buf=[]
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='link' and a.get('href'):
            rel=str(a.get('rel','')).lower();mime=str(a.get('type','')).lower()
            if 'api.w.org' in rel or 'json' in mime or 'xml' in mime:
                self.public_api_links.append({'href':a['href'],'rel':rel,'mime':mime})
    def handle_data(self,data):
        if self.capture:self.buf.append(data)
    def handle_endtag(self,tag):
        if self.capture==tag:
            s=re.sub(r'\s+',' ',''.join(self.buf)).strip()[:170]
            if s:
                if tag=='title': self.title=s
                else:self.headings.append(s)
            self.capture=None;self.buf=[]

def fetch(opener,url,maxbytes=800000):
    req=Request(url,headers={'User-Agent':AGENT,'Accept':'text/html, text/plain;q=0.8'})
    with opener.open(req,timeout=14) as response:
        data=response.read(maxbytes+1)
        if len(data)>maxbytes:raise ValueError('page too large')
        return data,response.headers.get_content_type(),response.headers.get_content_charset() or 'utf-8',response.geturl()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--company',default='companies/keyhan-sanat-ghaem/company.json')
    p.add_argument('--out',default=None)
    p.add_argument('--max-pages',type=int,default=25)
    p.add_argument('--delay',type=float,default=2.0)
    a=p.parse_args()
    if not 1<=a.max_pages<=60 or a.delay<1.5:p.error('max-pages 1..60 and delay >=1.5 required')
    root=Path(__file__).resolve().parents[1]
    cfg=Path(a.company)
    if not cfg.is_absolute():cfg=root/cfg
    company=json.loads(cfg.read_text(encoding='utf-8'))
    hosts=set(company['allowed_hosts_for_public_research'])
    seeds=[normalized(x) for x in company['research_seed_urls']]
    if not all(allowed(x,hosts) for x in seeds):p.error('seed outside allowed HTTPS hosts')
    out=Path(a.out) if a.out else cfg.parent/'research'/'crawl_runs'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out.mkdir(parents=True,exist_ok=True)
    opener=build_opener(RestrictedRedirect(hosts))
    policies={}
    for host in hosts:
        try:
            raw,_,_,_=fetch(opener,'https://'+host+'/robots.txt',200000)
            rp=RobotFileParser();rp.parse(raw.decode('utf-8','replace').splitlines());policies[host]=rp
        except HTTPError as e:
            if e.code in (404,410): policies[host]=None
            else:
                if any(urlsplit(x).hostname==host for x in seeds):raise SystemExit(f'robots.txt HTTP {e.code}: no crawl')
        except Exception:
            if any(urlsplit(x).hostname==host for x in seeds):raise SystemExit('Cannot verify robots.txt: no crawl')
    queue=deque(seeds);seen=set();pages=[];errors=[];last=0.0
    while queue and len(pages)<a.max_pages:
        url=normalized(queue.popleft())
        if url in seen or not allowed(url,hosts):continue
        seen.add(url);host=urlsplit(url).hostname
        if host not in policies:
            errors.append({'url':url,'error':'unverified_robots'});continue
        if policies[host] is not None and not policies[host].can_fetch(AGENT,url):
            errors.append({'url':url,'error':'robots_disallowed'});continue
        if last:time.sleep(max(0,a.delay-(time.monotonic()-last)))
        last=time.monotonic()
        try:
            raw,mime,charset,final=fetch(opener,url)
            if mime!='text/html':continue
            h=ReadPage();h.feed(raw.decode(charset,'replace'))
            pages.append({'url':url,'title':h.title,'headings':h.headings[:20],
                          'public_resource_links_advertised_not_queried':h.public_api_links[:20]})
            for link in h.links:
                if len(queue)>240:break
                candidate=normalized(urljoin(final,link))
                if allowed(candidate,hosts) and candidate not in seen:queue.append(candidate)
        except HTTPError as e:
            errors.append({'url':url,'error':'HTTP '+str(e.code)})
            if e.code in (401,403,429):break
        except Exception as e:
            errors.append({'url':url,'error':type(e).__name__+': '+str(e)[:100]})
    result={'company':company['slug'],'checked_utc':datetime.now(timezone.utc).isoformat(),
            'pages':pages,'errors':errors,'robots_status':{k:'present' if v else 'not_published' for k,v in policies.items()},
            'scope':'Public HTML inventory only; API links listed but not queried. No private data.'}
    target=out/'public_inventory.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Saved {target} — pages={len(pages)}, errors={len(errors)}')

if __name__=='__main__': main()
