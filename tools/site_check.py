#!/usr/bin/env python3
"""Daily check of the live galene.ie: pages up, links 200, HTTPS cert, required/forbidden claims per tools/site_facts.json, placeholder count.
Exit 1 if anything fails (so a scheduler can alert). Usage: python3 tools/site_check.py [--base https://galene.ie]"""
import json, re, sys, os, ssl, socket, html, datetime, urllib.request, urllib.error
BASE = sys.argv[sys.argv.index('--base')+1] if '--base' in sys.argv else 'https://galene.ie'
HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, 'site_facts.json')))
fails, warns = [], []

def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'galene-site-check'}), timeout=25) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e: return e.code, ''
    except Exception as e: return 0, str(e)

def text(h):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', h, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', h))

hrefs = set()
for path, rule in F['pages'].items():
    code, body = fetch(BASE + path)
    if code != 200: fails.append(f'{path}: HTTP {code}'); continue
    t = text(body)
    for s in rule['must']:
        if s not in t: fails.append(f'{path}: missing "{s}"')
    for s in rule['must_not']:
        if s in body: fails.append(f'{path}: contains "{s}"')
    for ph in F['placeholders']:
        n = t.count(ph)
        if n: warns.append(f'{path}: {n} x "{ph}"')
    for l in re.findall(r'(?:href|src)="([^"#]+)"', body):
        if l.startswith(('mailto:', 'tel:')): continue
        hrefs.add(l if l.startswith('http') else BASE + l)
for l in sorted(hrefs):
    code, _ = fetch(l)
    if 'amazon.' in l:
        if code in (0, 404): fails.append(f'Amazon link {l}: HTTP {code} (listing missing?)')
        continue
    if code not in (200, 301, 302): fails.append(f'link {l}: HTTP {code}')
host = BASE.split('//')[1].split('/')[0]
try:
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.create_connection((host, 443), timeout=20), server_hostname=host) as s:
        exp = datetime.datetime.strptime(s.getpeercert()['notAfter'], '%b %d %H:%M:%S %Y %Z')
    days = (exp - datetime.datetime.utcnow()).days
    (fails if days < F['cert_min_days'] else warns if days < 30 else []).append(f'TLS certificate expires in {days} days ({exp:%d %b %Y})')
except Exception as e: fails.append(f'TLS check failed: {e}')
print(f'# galene.ie site check {datetime.date.today():%d %b %Y}')
print(f'Pages {len(F["pages"])}, links {len(hrefs)}. FAIL {len(fails)}, warnings {len(warns)}.')
for x in fails: print('FAIL ' + x)
for x in warns: print('warn ' + x)
sys.exit(1 if fails else 0)
