# SPDX-License-Identifier: Apache-2.0
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'site'
class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []; self.refs = []; self.main = 0; self.h1 = 0
    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if 'id' in a: self.ids.append(a['id'])
        self.main += tag == 'main'
        self.h1 += tag == 'h1'
        assert tag != 'script', 'This site needs no scripts'
        for key in ('href', 'src'):
            if key in a: self.refs.append(a[key])

page = Check()
page.feed((ROOT / 'index.html').read_text())
assert page.main == page.h1 == 1
assert len(page.ids) == len(set(page.ids))
for ref in page.refs:
    if ref.startswith('#'): assert ref[1:] in page.ids, ref
    elif ref.startswith('https://'): pass
    else: assert (ROOT / ref).is_file(), ref
assert 'no installer' in (ROOT / 'index.html').read_text().lower() or 'no public installer' in (ROOT / 'index.html').read_text().lower()
print('PASS: semantic landmarks, unique IDs, local assets and fragment links')
