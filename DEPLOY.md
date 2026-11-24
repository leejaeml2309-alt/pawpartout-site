# Deploying pawpartout.com (GitHub Pages + Porkbun DNS)

Target launch: 25/11/2026, after Manager's review. Nothing has been pushed yet.

## 1. DNS records at Porkbun (domain pawpartout.com)
First, in Porkbun → Domain Management → pawpartout.com → DNS, **delete Porkbun's default records**: the parking
`ALIAS`/`A` record on the apex (pointing to Porkbun's parking page, often `pixie.porkbun.com`) and any default
`CNAME *` / `www` record. Otherwise they conflict with the records below.

Then add exactly these records (TTL 600 or Porkbun's default):

| Type  | Host (name)   | Answer / value          |
|-------|---------------|-------------------------|
| A     | (blank = apex) | 185.199.108.153        |
| A     | (blank = apex) | 185.199.109.153        |
| A     | (blank = apex) | 185.199.110.153        |
| A     | (blank = apex) | 185.199.111.153        |
| AAAA  | (blank = apex) | 2606:50c0:8000::153    |
| AAAA  | (blank = apex) | 2606:50c0:8001::153    |
| AAAA  | (blank = apex) | 2606:50c0:8002::153    |
| AAAA  | (blank = apex) | 2606:50c0:8003::153    |
| CNAME | www           | leejaeml2309-alt.github.io |

Check: `dig +short pawpartout.com A`, `dig +short pawpartout.com AAAA`, `dig +short www.pawpartout.com CNAME`
should return exactly the values above. (On the shared box, DNS is intercepted: check from another network or with
a public resolver, e.g. `dig @1.1.1.1 …`.)

## 2. Launch steps
1. Create the GitHub repo **leejaeml2309-alt/pawpartout-site** (public, empty: no README, no licence).
2. Push: `git remote add origin https://github.com/leejaeml2309-alt/pawpartout-site.git && git push -u origin main`.
3. Repo → Settings → Pages → Build and deployment → Source: **GitHub Actions**. The workflow
   `.github/workflows/pages.yml` runs on push (or run it by hand: Actions → Deploy Pawpartout → Run workflow).
   If a run fails with "No artifacts named github-pages", re-run the same commit.
4. Settings → Pages → Custom domain: **pawpartout.com** → Save. (`site/CNAME` already contains it.) GitHub runs a DNS check.
5. Once the DNS check passes, tick **Enforce HTTPS**. The certificate is issued automatically and **can take up to
   about an hour after DNS resolves**; until then the box may be greyed out or show a certificate error.
6. Check live: https://pawpartout.com/ (with `?cb=<random>` to skip caches), https://www.pawpartout.com/ redirects to
   the apex, https://pawpartout.com/nope shows the 404, /robots.txt and /sitemap.xml load.
7. **Remove noindex** at launch: delete the `<meta name="robots" content="noindex,nofollow">` line in `site/index.html`
   (marked "PRE-LAUNCH") — the one in `404.html` can stay. Commit, push, and re-check the live page source.
8. Optional afterwards: add the domain property in Google Search Console and submit https://pawpartout.com/sitemap.xml.
