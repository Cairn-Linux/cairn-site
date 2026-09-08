# Cairn site

The public-facing website for [Cairn Linux](https://github.com/Cairn-Linux/cairn).
The copy and visual design are provisional. Cairn itself is pre-alpha; this
website does not offer an operating-system download.

## Preview

From the repository root:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8080. There is no build step or runtime dependency.

## Edit

- `site/index.html`: page content and semantic layout.
- `site/assets/style.css`: responsive styles.
- `site/assets/mark.svg`: existing project mark, unchanged.
- `brand/tokens.json`: reference snapshot of the upstream brand tokens.

The OS repository remains authoritative for product claims and brand tokens.
Keep status language conservative and link to its roadmap. Propose brand
changes for approval rather than silently changing the identity here.
Typography prefers locally installed Atkinson Hyperlegible Next and falls
back to Arial/sans-serif. No font service or tracking script is loaded.

## Deploy

Publish **only `site/`** to any static HTTPS host. There is no application
server, database, environment variable or secret to configure. Do not serve
the repository root, which also contains contributor files and tests.

For a static-host Git integration, choose `main`, no build command, and
`site` as the publish/output directory. Disable framework detection if it
tries to build a JavaScript app. On GitHub Pages, use a Pages workflow that
uploads `site/`; do not select the repository root as the source.

No deployment integration is enabled in this repository. Choose the host,
custom domain, TLS and DNS cutover with Mason before enabling publication.
Do not add an automatic deploy-on-push workflow without that approval.

## Verify

```sh
python3 tests/check_site.py
```

For the browser smoke test, install the pinned test-only dependencies in a
virtual environment and install Chromium:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-test.txt
.venv/bin/playwright install chromium
.venv/bin/python tests/browser_smoke.py
```

This starts a loopback HTTP server, checks desktop/mobile rendering,
internal navigation and FAQ controls, and saves screenshots under
`test-results/`. It does not deploy or contact third-party sites.

## Design contributions

We welcome help with the website and Cairn's OS interface. They are separate
implementations: this site is HTML/CSS; the OS uses Qt/QML. Begin with the
[product design specification](https://github.com/Cairn-Linux/cairn/blob/main/docs/DESIGN.md).
Mason owns product decisions, merges and deployment. Use a branch and PR for
changes, and sign off commits (`git commit -s`).

## License

Website code is Apache-2.0. Copy and brand tokens are CC BY-SA 4.0.
The Cairn name and mark remain project trademarks; see `NOTICE` and the
upstream brand policy. No blanket license to alter the mark is granted.
