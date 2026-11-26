"""Builds the Pawpartout shop preview: /shop/, /shop/gifts/, /privacy/, /affiliate-disclosure/.
Content source: /workspace/gifts-for-pets-20261125/products.json (== live PCC Gifts 59df486a, checked)."""
import json, html, shutil, os, sys
sys.path.insert(0,os.path.dirname(__file__)); sys.path.insert(0,'/workspace/gifts-gen')
from motifs import sprite, icon, SECTIONS
from art import defs as art_defs, use as art_use
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SITE=f'{ROOT}/site'
SRC='/workspace/gifts-for-pets-20261125'; PCC_IMG='/workspace/ppc-gifts-illus-20261126/site/img/gifts'
e=html.escape
V='?v=20261127a'
d=json.load(open(f'{SRC}/products.json')); P=d['products']; CATS=d['categories']
SLUG={'toys-enrichment':'toys','beds-cushions':'beds','travel-accessories':'travel','premium-treats':'treats'}
DISC='As an Amazon Associate I earn from qualifying purchases.'
INTRO='Let’s be honest: your pet has been a very good boy (or girl) all year, give or take one shredded couch. Here are the gifts we’d actually wrap, grouped by need, each with an honest card and a tip that actually helps.'
OFFICIAL_LABEL={'gocat-da-bird':'Official site','bedsure-sherpa-bed':'Official site','bedsure-round-sherpa-cat-bed':'Official pet beds page','coolaroo-original-elevated-bed':'Official elevated beds page'}
ICON={'coolaroo-original-elevated-bed':'pad','bedsure-round-sherpa-cat-bed':'softbowl','chuckit-travel-pillow-bed':'pillow',
 'kh-thermo-kitty-bed':'pillow','kh-kitty-sill':'pad','furhaven-thermanap':'pad','best-friends-calming-donut':'pillow','furhaven-sofa-bed':'rollbed','bedsure-sherpa-bed':'pad',
 'sleepypod-air':'softbag','kurgo-tru-fit-harness':'harness','kurgo-collaps-a-bowl':'bowl','ruffwear-front-range-harness':'harness',
 'kurgo-heather-half-hammock':'softbag','petmate-two-door-kennel':'pod','sherpa-original-deluxe':'softbag','petsafe-come-with-me-kitty':'harness','ruffwear-roamer-leash':'bow',
 'purebites-chicken-dog':'bites','purebites-chicken-cat':'tub','wellness-kittles-chicken-cranberry':'bites',
 'greenies-original-regular':'bites','zukes-mini-naturals-chicken':'pouch','blue-bits-chicken':'pouch','temptations-classic-chicken':'tub','inaba-churu-variety':'gift2','feline-greenies-chicken':'pouch'}
ICVB={'stuff':(100,120),'cup':(110,110),'puzzle':(140,100),'banana':(140,90),'gift':(120,110),'gift2':(90,120),'bow':(100,70),'rollbed':(150,100),'pad':(150,100),'pillow':(150,100),
 'softbag':(150,110),'pod':(150,110),'bowl':(120,90),'softbowl':(120,100),'harness':(150,110),'pouch':(100,120),'bites':(120,90),'tub':(100,120)}
ILLUS={
 'kong-classic':'Generic red rubber stuffable dog chew toy with three stacked rounded tiers and a treat opening',
 'west-paw-toppl':'Generic tangerine-orange rubber treat cup for dogs with large oval openings and inner nubs',
 'nina-ottosson-hide-n-slide':'Generic tan rectangular dog treat puzzle board with swiveling round lids and a row of sliding blocks',
 'yeowww-chi-cat-a-banana':'Generic yellow cotton-twill catnip toy shaped like a banana with brown tips',
 'catstages-rainy-day-puzzle':'Generic round white cat food puzzle with light blue raindrop-shaped swivel lids, a center wheel and pegs',
 'chuckit-ultra-ball':'Two generic orange-and-blue rubber fetch balls for dogs',
 'gocat-da-bird':'Generic cat wand toy: a slim black rod with a speckled gray-and-white feather lure on a swivel',
 'catstages-tower-of-tracks':'Generic three-level white and gray ball-track tower for cats with six colorful balls',
 'outward-hound-hide-a-squirrel':'Generic brown plush tree trunk dog toy with three small plush squirrels peeking out of holes',
}
BAND_IMG={
 'toys':"Future the shih tzu trots off with a rubber chew toy while Lili the tortoiseshell cat stares, unimpressed.",
 'beds':"Lili the tortoiseshell cat has taken over a dog bed; Future the shih tzu sits beside it, resigned.",
 'travel':"Lilou the black-and-white cat hides inside a soft pet carrier while Future the shih tzu sniffs at it.",
 'treats':"Future the shih tzu greedily devours a spilled pouch and jar of treats while Lili the tortoiseshell cat and Lilou the black-and-white cat stare down at him, unimpressed.",
}
# geometry per gift category (inside the Gifts / phyllotaxis universe)
CATMO={'toys':('burst','rose'),'beds':('pinecone','rose'),'travel':('golden','rose'),'treats':('phyllo','rose')}
from PIL import Image

def head(title,desc,path,extra=''):
    url='https://pawpartout.com'+path
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pawpartout">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#071330">
<!-- No ads on Pawpartout. -->
<!-- ANALYTICS PLACEHOLDER: none yet (Marc to decide). If approved, paste the measurement snippet here on every page and update /privacy/ first. -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/marcellus-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/pp.css{V}">
{extra}</head>
'''
def header(cur):
    items=[]
    for k,lab,sub,href,mo,mt,_ in SECTIONS:
        ic=f'<span class="ic">{icon(mo,mt,small=True)}</span>'
        t=f'<span class="t">{e(lab)}</span>'
        if href:
            ac=' aria-current="page"' if k==cur else ''
            items.append(f'<li class="metal-{mt}"><a href="{href}"{ac}>{ic}{t}</a></li>')
        else:
            items.append(f'<li><span class="soon" title="Coming soon">{ic}{t}</span></li>')
    return f'''<header class="pp-head">
<div class="pp-wrap pp-head-in">
<a class="pp-brand" href="/" aria-label="Pawpartout home: the rosace"><span class="medal">{icon('seed','gold')}</span><b class="mtext">Pawpartout<span class="tm">™</span></b></a>
<a class="pp-back" href="/#wheel"><svg viewBox="0 0 100 100" style="--mg:url(#m-gold)" aria-hidden="true"><use href="#g-seed"/></svg><span class="lg">Back to the rosace</span><span class="sm">Rosace</span></a>
</div>
<nav class="pp-rail" aria-label="Pawpartout sections"><ul>{''.join(items)}</ul></nav>
</header>
<script>(function(){{var u=document.querySelector('.pp-rail ul'),c=u&&u.querySelector('[aria-current]');if(c&&u.scrollWidth>u.clientWidth)u.scrollLeft=c.parentNode.offsetLeft-(u.clientWidth-c.parentNode.offsetWidth)/2}})();</script>'''
def rule(metal='gold'):
    return f'<div class="pp-rule metal-{metal}" aria-hidden="true"><svg viewBox="0 0 150 30" style="--mg:url(#m-{metal})"><use href="#g-rule"/></svg></div>'
def footer():
    return f'''<footer class="pp-foot">
{rule('gold')}
<div class="pp-wrap pp-foot-in">
<div><a class="pp-brand" href="/"><span class="medal">{icon('seed','gold')}</span><b class="mtext">Pawpartout<span class="tm">™</span></b></a>
<p class="about">One door to every place we build for travelling and living with cats and dogs.</p></div>
<div><h2>Explore</h2><ul>
<li><a href="/">The rosace</a></li><li><a href="/shop/">Paw Shop</a></li><li><a href="/shop/gifts/">Gifts for pets</a></li><li><a href="/books/">Books</a></li></ul></div>
<div><h2>Our sites &amp; fine print</h2><ul>
<li><a href="https://petpolicycheck.com/">PetPolicyCheck</a></li><li><a href="https://ticketsntails.com/">Tickets &amp; Tails</a></li>
<li><a href="/privacy/">Privacy</a></li><li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li></ul></div>
</div>
<div class="pp-wrap"><p class="legal"><span>© 2026 Pawpartout™ · No ads, ever.</span><span>{DISC}</span></p></div>
</footer>'''
import re
def small(h): return re.sub(r'(aria-hidden="true"><use href="#g-)([a-z]+)("/>)',r'\1\2-s\3',h)
def page(title,desc,path,cur,body,extra=''):
    return small(head(title,desc,path,extra)+f'''<body>
<a class="skip" href="#main">Skip to content</a>
{sprite()}
{art_defs() if 'pp-well-art' in body or 'hx' in body else ''}
{header(cur)}
<main id="main" class="pp-wrap">
{body}
</main>
{footer()}
</body>
</html>
''')
def species(p):
    s=set(p['species']); return 'Dogs and cats' if s=={'dog','cat'} else ('Dogs' if s=={'dog'} else 'Cats')
def well(p):
    lab=f'<span class="pp-illus"><svg viewBox="0 0 100 100" style="--mg:url(#m-rose)" aria-hidden="true"><use href="#g-hexafoil"/></svg>Illustration</span>'
    lin=f'<svg class="lin" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice" style="--mg:url(#m-rose)" aria-hidden="true"><use href="#g-phyllo"/></svg>'
    if p['id'] in ILLUS:
        w,h=Image.open(f'/workspace/gifts-gen/illus/out/{p["id"]}.webp').size
        inner=f'<img class="pp-well-img" src="/shop/img/illus/{p["id"]}.webp{V}" width="{w}" height="{h}" alt="{e(ILLUS[p["id"]])}" loading="lazy" decoding="async">'
    else:
        k=ICON[p['id']]; w,h=ICVB[k]
        inner=f'<svg class="pp-well-art" viewBox="0 0 {w} {h}" role="img" aria-label="Drawn illustration of the product type">{art_use(k,0,0,w,h)}</svg>'
    return f'<div class="pp-well">{lin}{inner}{lab}</div>'
def card(p):
    vn=p.get('variant_note','')
    vn_html=f'<details class="pp-size"><summary>Linked size &amp; options</summary><p>{e(vn)}</p></details>' if vn else ''
    leafic='<svg viewBox="0 0 100 100" style="--mg:url(#m-rose)" aria-hidden="true"><use href="#g-hexafoil"/></svg>'
    return f'''<article class="pp-card" id="{e(p['id'])}"><div class="pp-card-in">
{well(p)}
<div class="pp-body">
<div class="pp-meta"><span class="pp-seller" title="Sold by">{e(p.get('seller_badge','Amazon'))}</span><span>{species(p)}</span></div>
<h3 class="pp-name">{e(p['name'])}</h3>
<p class="pp-brandn">{e(p['brand'])}</p>
<p class="pp-text">{e(p['card'])}</p>
<p class="pp-tip">{leafic}<strong>Tip:</strong> {e(p['usage_tip'])}</p>
{vn_html}
<div class="pp-actions"><a class="pp-btn" href="{e(p['amazon_url'])}" rel="sponsored nofollow noopener" target="_blank" data-asin="{e(p['asin'])}">Check price on Amazon<span class="sr"> (opens in a new tab)</span></a><a class="pp-off" href="{e(p['official_url'])}" rel="noopener" target="_blank">{e(OFFICIAL_LABEL.get(p['id'],'Official product page'))}<span class="sr"> (opens in a new tab)</span></a></div>
</div></div></article>'''

# ---------------- images ----------------
os.makedirs(f'{SITE}/shop/img/illus',exist_ok=True)
for k in ILLUS: shutil.copy(f'/workspace/gifts-gen/illus/out/{k}.webp',f'{SITE}/shop/img/illus/{k}.webp')
for f in os.listdir(PCC_IMG):
    if f.endswith('.webp') and '1152' not in f: shutil.copy(f'{PCC_IMG}/{f}',f'{SITE}/shop/img/{f}')

def portrait(cls='pp-hero-portrait',sizes='(max-width:720px) 140px, 220px'):
    return (f'<div class="{cls} metal-rose">{icon("phyllo-ring","rose")}<figure><img src="/shop/img/gifts-hero-trio-640.webp{V}" '
            f'srcset="/shop/img/gifts-hero-trio-640.webp{V} 640w, /shop/img/gifts-hero-trio-960.webp{V} 960w" sizes="{sizes}" width="640" height="480" '
            f'alt="Painted Christmas portrait of Future the shih tzu, Lili the tortoiseshell cat and little Lilou the black-and-white cat, beside wrapped gifts." decoding="async"></figure></div>')

# ---------------- /shop/gifts/ ----------------
jump=[]; secs=[]
for i,c in enumerate(CATS,1):
    slug=SLUG[c['id']]; items=[p for p in P if p['category']==c['id']]; mo,mt=CATMO[slug]
    jump.append(f'<li><a href="#{slug}">{icon(mo,mt,small=True)}<span>{e(c["label"])}</span><b>{len(items)}</b></a></li>')
    secs.append(f'''<section class="pp-sec metal-rose" aria-labelledby="{slug}" id="sec-{slug}">
{rule('rose') if i>1 else ''}
<div class="pp-band">
<div class="num">{icon(mo,mt)}<b>{i}</b></div>
<div><p class="k">{len(items)} gifts</p><h2 id="{slug}">{e(c['label'])}</h2><p class="bl">{e(c['blurb'])}</p></div>
<figure><img src="/shop/img/gifts-band-{slug}-400.webp{V}" srcset="/shop/img/gifts-band-{slug}-400.webp{V} 400w, /shop/img/gifts-band-{slug}-720.webp{V} 720w" sizes="(max-width:720px) 90vw, 220px" width="720" height="405" alt="{e(BAND_IMG[slug])}" loading="lazy" decoding="async"></figure>
</div>
<div class="pp-grid">
{chr(10).join(card(p) for p in items)}
</div>
</section>''')
gifts_body=f'''<p class="pp-crumbs"><a href="/">Pawpartout</a> › <a href="/shop/">Paw Shop</a> › Gifts for pets</p>
<section class="pp-hero metal-rose" aria-labelledby="h1">
<div>
<p class="pp-eyebrow"><svg viewBox="0 0 100 100" style="--mg:url(#m-rose)" aria-hidden="true"><use href="#g-phyllo"/></svg>Paw Shop · Christmas shelf 2026</p>
<h1 id="h1"><span class="mtext">Gifts for pets</span></h1>
<p class="pp-sub">A small Christmas shelf for the journey, and for home.</p>
<p class="pp-intro">{e(INTRO)}</p>
</div>
{portrait()}
</section>
<p class="pp-disc metal-rose"><svg viewBox="0 0 100 100" style="--mg:url(#m-rose)" aria-hidden="true"><use href="#g-hexafoil"/></svg><strong>{DISC}</strong> Links on this page are affiliate links. <a href="/affiliate-disclosure/">How that works</a>.</p>
<nav class="pp-jump metal-rose" aria-label="Gift categories"><ul>{''.join(jump)}</ul></nav>
{''.join(secs)}
{rule('rose')}
<p class="pp-note"><a href="/shop/">← Back to Paw Shop</a></p>
<p class="pp-note"><strong>{DISC}</strong> Buying through these links may earn us a commission at no extra cost to you, and it never changes what we pick or say. Amazon prices and photos are not shown here; each button opens the current Amazon listing. We have not tested these products ourselves: product details come from each maker’s official page. Pictures are illustrations of the product type, not photos of the exact item. <a href="/affiliate-disclosure/">Affiliate disclosure</a>.</p>'''
os.makedirs(f'{SITE}/shop/gifts',exist_ok=True)
open(f'{SITE}/shop/gifts/index.html','w').write(page('Gifts for pets: a Christmas shelf for dogs and cats · Pawpartout',
 'Thirty-six Christmas gifts for dogs and cats, grouped by need: toys and enrichment, beds, travel gear and premium treats. Honest notes and a practical tip on every card.',
 '/shop/gifts/','shop',gifts_body))

# ---------------- /shop/ ----------------
DOORS=[('toys','Toys & enrichment','stuff','Puzzles, chews, fetch and catnip classics.'),
       ('beds','Beds & comfort','rollbed','Travel beds, warm mats and window seats.'),
       ('travel','Travel','softbag','Cabin bags, harnesses, leashes and bowls.'),
       ('treats','Treats','bites','Single-ingredient bites and crowd-pleasers.')]
cnt={SLUG[c['id']]:sum(1 for p in P if p['category']==c['id']) for c in CATS}
doors=''.join(f'''<li class="metal-copper"><a class="pp-door" href="/shop/gifts/#{s}"><span class="hx"><svg viewBox="0 0 {ICVB[k][0]} {ICVB[k][1]}" aria-hidden="true">{art_use(k,0,0,*ICVB[k])}</svg></span>
<h3>{e(t)}</h3><p>{e(dsc)} {cnt[s]} picks.</p><span class="go">Open the shelf →</span></a></li>''' for s,t,k,dsc in DOORS)
shop_body=f'''<p class="pp-crumbs"><a href="/">Pawpartout</a> › Paw Shop</p>
<section class="pp-hero metal-copper" aria-labelledby="h1">
<div>
<p class="pp-eyebrow"><svg viewBox="0 0 100 100" style="--mg:url(#m-copper)" aria-hidden="true"><use href="#g-hex"/></svg>Paw Shop</p>
<h1 id="h1"><span class="mtext">Paw Shop</span></h1>
<p class="pp-sub">Gear and gifts for dogs and cats, one honest card at a time.</p>
<p class="pp-intro">Every pick comes with a plain-spoken card, a tip that actually helps and a link to the maker’s official page. Prices stay on the seller’s site, never here, so what you see there is always current.</p>
</div>
<div class="pp-medal metal-copper"><span class="halo"></span>{icon('hex','copper')}</div>
</section>
<p class="pp-disc metal-copper"><svg viewBox="0 0 100 100" style="--mg:url(#m-copper)" aria-hidden="true"><use href="#g-hex"/></svg><strong>{DISC}</strong> Shop links are affiliate links. <a href="/affiliate-disclosure/">How that works</a>.</p>
{rule('copper')}
<a class="pp-feature metal-rose" href="/shop/gifts/">
{portrait('ph','(max-width:720px) 120px, 160px')}
<div><p class="pp-eyebrow"><svg viewBox="0 0 100 100" style="--mg:url(#m-rose)" aria-hidden="true"><use href="#g-phyllo"/></svg>Christmas shelf · 2026</p>
<h2><span class="mtext">Gifts for pets</span></h2>
<p>Thirty-six gifts for dogs and cats, grouped by need, each with an honest card and a tip that actually helps.</p>
<span class="pp-btn">Open the gift shelf</span></div>
</a>
{rule('copper')}
<h2 class="sr">Shop by need</h2>
<ul class="pp-doors">{doors}</ul>
<p class="pp-note">For now, each door opens its shelf inside Gifts for pets. Pictures are illustrations of the product type.</p>'''
os.makedirs(f'{SITE}/shop',exist_ok=True)
open(f'{SITE}/shop/index.html','w').write(page('Paw Shop: gear and gifts for dogs and cats · Pawpartout',
 'Toys, beds, travel gear and treats for dogs and cats, each with an honest card, a practical tip and a link to the maker’s official page.',
 '/shop/','shop',shop_body))

# ---------------- legal pages ----------------
UPD='Last updated November 27, 2026.'
priv=f'''<p class="pp-crumbs"><a href="/">Pawpartout</a> › Privacy</p>
<section class="pp-hero metal-gold" aria-labelledby="h1"><div>
<p class="pp-eyebrow"><svg viewBox="0 0 100 100" style="--mg:url(#m-gold)" aria-hidden="true"><use href="#g-seed"/></svg>Fine print</p>
<h1 id="h1"><span class="mtext">Privacy</span></h1>
<p class="pp-sub">What happens to your data on pawpartout.com, in plain words.</p></div>
<div class="pp-medal metal-gold" style="max-width:220px"><span class="halo"></span>{icon('seed','gold')}</div></section>
<div class="pp-prose">
<p class="upd">{UPD}</p>
<h2>The short version</h2>
<p>Pawpartout™ has no accounts, no sign-up forms and no ads. We do not ask for your name, email or payment details anywhere on pawpartout.com.</p>
<h2>Hosting</h2>
<p>The site is a set of static pages hosted on GitHub Pages. Like any web host, GitHub may record technical data such as your IP address when your browser requests a page, for security and to keep the service running. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub General Privacy Statement</a>.</p>
<h2>Analytics and cookies</h2>
<p>The rosace home page, Paw Shop, Gifts for pets and these fine-print pages set no cookies and load no analytics. Fonts are served from pawpartout.com itself.</p>
<p>The Books page currently uses Google Analytics to count visits. Google’s handling of that data is described in the <a href="https://policies.google.com/privacy" rel="noopener">Google Privacy Policy</a>. If we add analytics anywhere else, we will update this page first.</p>
<h2>Links to other sites</h2>
<p>Buttons such as “Check price on Amazon” and the maker links take you to other websites, including Amazon, the product makers, PetPolicyCheck and Tickets &amp; Tails. Those sites have their own privacy policies. Amazon may use cookies to record that you arrived through one of our affiliate links; see our <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p>
</div>'''
aff=f'''<p class="pp-crumbs"><a href="/">Pawpartout</a> › Affiliate disclosure</p>
<section class="pp-hero metal-copper" aria-labelledby="h1"><div>
<p class="pp-eyebrow"><svg viewBox="0 0 100 100" style="--mg:url(#m-copper)" aria-hidden="true"><use href="#g-hex"/></svg>Fine print</p>
<h1 id="h1"><span class="mtext">Affiliate disclosure</span></h1>
<p class="pp-sub">How Pawpartout earns from the links on its shop pages.</p></div>
<div class="pp-medal metal-copper" style="max-width:220px"><span class="halo"></span>{icon('hex','copper')}</div></section>
<div class="pp-prose">
<p class="upd">{UPD}</p>
<p><strong>{DISC}</strong></p>
<h2>Which links</h2>
<p>The “Check price on Amazon” buttons in Paw Shop and Gifts for pets, and the Amazon buttons on the Books page, are Amazon affiliate links. If you buy through one of them, we may earn a commission. You pay the same price.</p>
<p>Affiliate links are marked for search engines with <code>rel="sponsored"</code>. Links to makers’ official pages are not affiliate links.</p>
<h2>What it does not change</h2>
<p>A commission never changes what we pick or what a card says. We do not show Amazon prices or photos: each button opens the current Amazon listing, where the price and availability are up to date.</p>
<p>We have not tested these products ourselves. Product details come from each maker’s official page. Pictures on the cards are illustrations of the product type, not photos of the exact item.</p>
<h2>No ads</h2>
<p>Pawpartout shows no advertising. Affiliate links are the only way the shop pages earn money.</p>
</div>'''
for path,t,dsc,b in (('privacy','Privacy · Pawpartout','How pawpartout.com handles data: no accounts, no ads, static hosting on GitHub Pages.',priv),
                     ('affiliate-disclosure','Affiliate disclosure · Pawpartout','How Pawpartout earns from Amazon affiliate links on its shop pages, and what that never changes.',aff)):
    os.makedirs(f'{SITE}/{path}',exist_ok=True)
    open(f'{SITE}/{path}/index.html','w').write(page(t,dsc,f'/{path}/',None,b))

# ---------------- sitemap ----------------
urls=['/','/books/','/shop/','/shop/gifts/','/privacy/','/affiliate-disclosure/']
open(f'{SITE}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
  ''.join(f'  <url>\n    <loc>https://pawpartout.com{u}</loc>\n    <lastmod>{"2026-11-26" if u in ("/","/books/") else "2026-11-27"}</lastmod>\n  </url>\n' for u in urls)+'</urlset>\n')
print('built')
