# Pawpartout™ — pawpartout.com

The hub of all our places for life and travel with cats and dogs: one gold rosace (a Flower of Life set in an
Art Nouveau mandala), five doors around it. Static site, no build step, no analytics, no ads.

## Brand rules (legal check, 24/11/2026)
- Write the name **Pawpartout™** in its visible brand uses: the rosace medallion, the h1, the header brand, the footer,
  and the first mention in the copy (markup: `Pawpartout<span class="tm">™</span>`). **Never use ®.**
  Plain « Pawpartout » is fine in `<title>`, meta/og/twitter tags, URLs and alt text.
- Nothing may resemble Paw Patrol, visually or in tone: no badge or shield logo, no red/blue cartoon look,
  no rescue-team / kids' wording. Keep the navy-and-gold Art Nouveau mandala and its calm, adult tone.
- No reference at all to the TV show « Passe-Partout ».

## Layout
- `site/` — everything that is published (GitHub Pages uploads this folder)
  - `index.html` — the page. SITE CONFIG block at the top: canonical + og:url (https://pawpartout.com/), and the
    pre-launch `noindex` line to delete at launch.
  - `style.css`, `site.js` — all styles and the rosace drawing; no external dependency
  - `fonts/` — Marcellus + Inter (woff2, OFL licences)
  - `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` — gold Seed of Life on navy
  - `404.html`, `robots.txt`, `sitemap.xml` (1 URL), `CNAME` (pawpartout.com), `.nojekyll`
- `.github/workflows/pages.yml` — build job (upload `site/`) then a separate deploy job
- `DEPLOY.md` — DNS records at Porkbun and launch steps

## The rosace (site.js)
Drawn in SVG with exact geometry, no images. Flower of Life: 19 circles of radius r on a hexagonal grid
(centre; 6 at r; 6 at 2r; 6 at r·√3) inside a circle of radius 3r, the Seed of Life (inner 7 circles) in a bolder band.
Around it: 20 flame petals with carved veins and 20 buds, 10 whiplash lyres, 60 pearls, a double outer band.
Gold relief: stacked strokes (cast shadow, dark lower edge, pale upper edge, gold-gradient body, polished ridge),
light from the top left. Above 640 px a feSpecularLighting filter and a blurred shadow are added; phones use the
filter-free stack with thicker bands. A slow sheen sweep runs on its own SVG layer and is not created under
prefers-reduced-motion. Door buttons and the centre medallion « Pawpartout™ » use a conic gold frame in CSS.

## Doors (absolute links)
Live: PetPolicyCheck (https://petpolicycheck.com/), Tickets & Tails (https://ticketsntails.com/),
Forum EN/KO (https://petpolicycheck.com/forum/). Coming soon, no link, no date: Interactive forum, The shop.
To open one: in index.html turn its `<div class="node soon">` (wheel) and `<div class="door soon">` (list) into
`<a class="node live" href="…">` / `<a class="door live" href="…">`.

## Story
Between `<!-- STORY:START -->` and `<!-- STORY:END -->` in index.html: replace the placeholder box with the Éditeur's
text, as `<div class="story-text"><p>…</p></div>`.

## Local preview
`cd site && python3 -m http.server 8725` then open http://localhost:8725/
