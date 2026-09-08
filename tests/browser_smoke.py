# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
(root / 'test-results').mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root / 'site')))
Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}'
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width in [1440, 390, 320]:
            page = browser.new_page(viewport={'width': width, 'height': 1000})
            errors = []; external = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('request', lambda r: external.append(r.url) if not r.url.startswith(url) else None)
            response = page.goto(url)
            assert response.status == 200
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert page.locator('main').count() == 1
            assert page.locator('main #progress').count() == 1
            assert page.locator('img').evaluate_all('(els)=>els.every(e=>e.complete && e.naturalWidth>0)')
            page.get_by_role('link', name='Meet Cairn', exact=True).click()
            assert page.evaluate('location.hash') == '#idea'
            for summary in page.locator('summary').all():
                summary.click()
                assert summary.evaluate('(e)=>e.parentElement.open')
                summary.click()
            page.locator('.skip').focus()
            assert page.locator('.skip').evaluate('(e)=>e.getBoundingClientRect().top>=0')
            page.locator('.skip').evaluate('(e)=>e.blur()')
            page.evaluate('scrollTo(0,0)')
            page.screenshot(path=str(root / 'test-results' / f'{width}.png'), full_page=True)
            assert not errors and not external, (errors, external)
            print(f'PASS HTTP browser smoke: {width}px, no overflow/errors/external requests; links, images, FAQ, focus')
            page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
