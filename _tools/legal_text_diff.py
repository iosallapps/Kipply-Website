"""Visible-text diff of the legal and support pages, main content and whole body,
between main (before) and the working tree (after)."""
import os
import subprocess, re, difflib, sys
from html.parser import HTMLParser
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.out=[]; self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','svg','head'): self.skip+=1
        if tag in ('p','li','h1','h2','h3','h4','br','div','ul','tr','summary','details','hr'): self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style','svg','head'): self.skip-=1
        if tag in ('p','li','h1','h2','h3','h4','div','ul','summary','details'): self.out.append('\n')
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

def visible(html):
    p = Text(); p.feed(html)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in ''.join(p.out).split('\n')]
    return [l for l in lines if l]

def part(html, which):
    if which == 'main':
        return re.search(r'<main id="main">(.*?)</main>', html, re.S).group(1)
    return re.search(r'<body>(.*?)</body>', html, re.S).group(1)

ok = True
report = []
for name in ('terms.html', 'privacy.html', 'support.html'):
    before = subprocess.run(['git','-C',SITE,'show',f'main:{name}'], capture_output=True, text=True, check=True).stdout
    after = open(f'{SITE}/{name}', encoding='utf-8').read()
    for which in ('main', 'body'):
        a = visible(part(before, which)); b = visible(part(after, which))
        diff = list(difflib.unified_diff(a, b, f'main:{name} ({which})', f'redesign-130:{name} ({which})', lineterm='', n=0))
        same = a == b
        report.append(f'{name} [{which}]: {"IDENTICAL" if same else "DIFFERS"} ({len(a)} lines before, {len(b)} after)')
        if which == 'main' and not same: ok = False
        if diff: report.extend(diff); report.append('')
open(f'{SITE}/.redesign-preview/checks/legal-text-diff.txt','w').write('\n'.join(report)+'\n')
print('\n'.join(l for l in report if l.startswith(('terms','privacy','support'))))
print('MAIN TEXT UNCHANGED' if ok else 'MAIN TEXT CHANGED')
