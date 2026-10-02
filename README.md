# Cairn site

The public-facing website for [Cairn Linux](https://github.com/Cairn-Linux/cairn),
live at <https://cairnlinux.com>. The copy and visual design are provisional.
Cairn itself is pre-alpha; this website does not offer an operating-system
download.

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

The site is live at <https://cairnlinux.com>, served by Cloudflare.
Cloudflare's Workers Builds is connected to this repository: every change
to `main`, a merged pull request included, is published to cairnlinux.com
within moments, and every pull request gets a "Workers Builds: cairn-site"
check. **Merging is publishing.** Run the checks under "Verify" before a
merge, not after.

The deployment is set up in Cloudflare, not here: there is no workflow file
in this repository. It publishes **only `site/`**, with no build command.
There is no application server, database, environment variable or secret.
Never serve the repository root, which also holds contributor files and
tests. Changes to the host, domain, TLS or DNS go through Mason.

The page says it loads no analytics or tracking scripts, so keep
Cloudflare features that add scripts to it turned off: Bot Fight Mode,
JavaScript detections and Web Analytics. The browser test below runs
against a local copy and cannot see what Cloudflare adds; check the live
page instead, for example with
`curl -s https://cairnlinux.com/ | grep -c cdn-cgi`, which should print 0.

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
