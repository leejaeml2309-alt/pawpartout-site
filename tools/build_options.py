"""Preview-only pages for the options sheet and the geometry map (not part of site/)."""
import os, sys, io, contextlib
sys.path.insert(0,os.path.dirname(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import build as B
from motifs import SECTIONS, EXTRA, METAL_NAME, icon
OUT=os.path.join(B.ROOT,'options-preview')
toys=[p for p in B.P if p['category']=='toys-enrichment'][:3]
CSS={'a':'',
'b':'''/* B · Orbit: centered, dense ornament, medallion cards */
.pp-head-in{flex-direction:column;justify-content:center;gap:4px;padding:14px 0 6px;position:relative}
.pp-brand{flex-direction:column;gap:6px}.pp-brand .medal{width:64px;height:64px}.pp-brand b{font-size:1.9rem}
.pp-back{position:absolute;right:28px;top:20px}
.pp-rail ul{max-width:1100px}
.pp-rail .ic{width:46px;height:46px;padding:7px;border-radius:50%;background:radial-gradient(circle at 50% 35%,#12306a,#050e26 75%);box-shadow:0 0 0 1.5px #d6b25e,0 0 0 4px #071330,0 0 0 5px #d6b25e44}
.pp-rail a[aria-current]{box-shadow:none;background:none}.pp-rail a[aria-current] .ic{box-shadow:0 0 0 2px #f3b48a,0 0 0 5px #071330,0 0 0 6.5px #f3b48a,0 0 22px #f3b48a66}
.pp-hero{grid-template-columns:1fr;text-align:center;justify-items:center;position:relative}
.pp-hero .pp-medal{order:-1;max-width:220px}
.pp-hero::before{content:"";position:absolute;left:50%;top:50%;width:900px;height:900px;transform:translate(-50%,-50%);border-radius:50%;
 background:repeating-radial-gradient(circle,#d6b25e14 0 1px,transparent 1px 38px);pointer-events:none;z-index:-1}
.pp-eyebrow{justify-content:center}.pp-intro{margin:0 auto}
.pp-card{border-radius:50% 50% 26px 26px/22% 22% 26px 26px}
.pp-card-in{background:repeating-radial-gradient(circle at 50% 0,#ffffff07 0 1px,transparent 1px 22px),linear-gradient(180deg,#0c1f45,#071330)}
.pp-well{width:74%;aspect-ratio:1;margin:26px auto 4px;border-radius:50%;box-shadow:0 0 0 6px #071330,0 0 0 7.5px #efbfb0,0 0 0 13px #071330,0 0 0 14px #efbfb066,inset 0 -18px 30px #b99f7a33}
.pp-well-img{inset:16%;width:68%;height:68%}
.pp-illus{bottom:12%}
.pp-body{text-align:center}.pp-meta{justify-content:center;gap:16px}.pp-actions{justify-content:center}
.pp-tip{text-align:left}''',
'c':'''/* C · Ledger: quiet, left-aligned, ornament only on rules and corners */
.pp-head{border-image:linear-gradient(90deg,#d6b25e66,#d6b25e66) 1}
.pp-head-in{min-height:60px}.pp-brand .medal{box-shadow:none;background:none;padding:0;width:30px;height:30px}.pp-brand b{font-size:1.25rem}
.pp-back{border:0;background:none}
.pp-rail{border-top:0}
.pp-rail ul{display:flex;justify-content:flex-start;gap:0;padding:0 28px;max-width:1180px}
.pp-rail li{flex:none}
.pp-rail a,.pp-rail span.soon{flex-direction:row;min-height:44px;padding:0 10px;border-radius:0;gap:6px}
.pp-rail .ic{width:16px;height:16px}.pp-rail .t{font-size:.74rem;white-space:nowrap}
.pp-rail span.soon{display:none}
.pp-rail a[aria-current]{background:none;box-shadow:inset 0 -2px 0 #f3b48a}
.pp-hero{grid-template-columns:1fr;padding-bottom:0}.pp-hero .pp-medal,.pp-hero .pp-hero-portrait{display:none}
.pp-hero h1{font-size:3.2rem}
.pp-hero>div{border-left:2px solid #efbfb0;padding-left:26px}
.pp-card{border-radius:8px;padding:0;background:none;box-shadow:none;border-top:2px solid #efbfb0}
.pp-card-in{border-radius:0 0 8px 8px;background:#0a1a3c}
.pp-well{margin:0;border-radius:0;aspect-ratio:16/10;box-shadow:none}
.pp-well .lin{inset:auto 10px 10px auto;width:34px;height:34px;opacity:.9}
.pp-illus{left:12px;transform:none}
.pp-grid{gap:20px}'''}
NAME={'a':'A · Jewel case','b':'B · Orbit','c':'C · Ledger'}
for k,css in CSS.items():
    body=f'''<section class="pp-hero metal-copper" aria-labelledby="h1"><div>
<p class="pp-eyebrow"><svg viewBox="0 0 100 100" style="--mg:url(#m-copper)" aria-hidden="true"><use href="#g-hex"/></svg>Paw Shop · Gifts for pets</p>
<h1 id="h1"><span class="mtext">Gifts for pets</span></h1>
<p class="pp-sub">A small Christmas shelf for the journey, and for home.</p></div>
<div class="pp-medal metal-copper" style="max-width:260px"><span class="halo"></span>{icon('hex','copper')}</div></section>
{B.rule('rose')}
<div class="pp-grid metal-rose">{''.join(B.card(p) for p in toys)}</div>'''
    h=B.page(NAME[k]+' · options','preview','/shop/gifts/','shop',body,extra=f'<style>{css}</style>' if css else '')
    open(f'{OUT}/{k}.html','w').write(h)

# geometry map
rows=SECTIONS[:5]+EXTRA+SECTIONS[5:]
fam={'gold':'Core & stories','platinum':'Information & care','silver':'Community & memories','copper':'Gear & outdoors','rose':'Warmth & home'}
cells=''.join(f'''<li class="metal-{mt}"><span class="big">{icon(mo,mt)}</span><span class="sm">{icon(mo,mt,small=True)}</span>
<b>{B.e(lab)}</b><i>{B.e({'seed':'Seed of Life','hex':'Beehive hexagons','phyllo':'Sunflower phyllotaxis','waves':'Sine wave on the rosace','nautilus':'Chambered nautilus','sierpinski':'Sierpinski triangle','metatron':"Metatron's Cube",'pinecone':'Pine-cone phyllotaxis','burst':'Golden-angle burst','golden':'Golden rectangles','flake':'Six-fold crystal','hexafoil':'Flower of Life petals','rings':'Vesica Piscis'}[mo])} · {METAL_NAME[mt]}</i><small>{B.e(why)}</small></li>''' for k,lab,sub,href,mo,mt,why in rows)
legend=''.join(f'<span class="metal-{m}"><em style="background:linear-gradient(160deg,var(--m))"></em>{METAL_NAME[m]}: {fam[m]}</span>' for m in fam)
gm=f'''<!doctype html><html lang="en-US"><head><meta charset="utf-8"><title>Section geometry map</title><link rel="stylesheet" href="/pp.css">
<style>body{{padding:34px 40px}}h1{{font:400 2.4rem var(--disp);margin:0}}.lead{{color:var(--mut);margin:4px 0 18px}}
.lg{{display:flex;flex-wrap:wrap;gap:10px 22px;margin:0 0 22px;font-size:.86rem}}.lg span{{display:flex;align-items:center;gap:8px}}.lg em{{width:22px;height:22px;border-radius:50%;display:block}}
ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,1fr);gap:16px}}
li{{position:relative;padding:16px 16px 18px;border-radius:120px 120px 14px 14px/80px 80px 14px 14px;background:#0a1a3c;border:1px solid #ffffff14;display:flex;flex-direction:column;align-items:center;text-align:center}}
.big{{width:150px;height:150px;display:block}}.sm{{position:absolute;right:14px;top:120px;width:30px;height:30px}}
b{{font:400 1.2rem/1.2 var(--disp);color:var(--head);margin-top:8px}}i{{font-style:normal;font-size:.78rem;color:var(--mt);font-weight:600;margin:3px 0 6px}}small{{font-size:.78rem;color:var(--mut)}}</style></head>
<body>{B.sprite()}<h1 class="mtext" style="--m:var(--gold)">Pawpartout · one geometry per section</h1>
<p class="lead">The rosace / Seed of Life stays the master frame. Each section gets its own natural geometry, drawn as solid polished metal on navy (hand-built SVG, small icon size shown top-right of each).</p>
<p class="lg">{legend}</p><ul>{cells}</ul></body></html>'''
open(f'{OUT}/geometry-map.html','w').write(gm)
sheet='''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/pp.css"><style>body{padding:30px}h1{font:400 2.2rem var(--disp);margin:0 0 6px}
.row{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.row figure{margin:0}.row img{width:100%;display:block;border-radius:10px;border:1px solid #ffffff22}
figcaption{margin:12px 0 0}figcaption b{font:400 1.4rem var(--disp);color:var(--head)}figcaption p{margin:4px 0 0;color:var(--mut);font-size:.9rem}.rec{color:#071330;background:linear-gradient(170deg,#fff6d2,#f3d98f 45%,#d6b25e);font:700 .7rem var(--text);letter-spacing:.12em;text-transform:uppercase;padding:3px 10px;border-radius:99px;margin-left:8px;vertical-align:middle}</style></head><body>
<h1 class="mtext">Pawpartout skeleton · three directions</h1><p style="color:var(--mut);margin:0 0 20px">Same navy + metals, same content (Gifts header + first row of toys). They differ by structure, layout and ornament density.</p>
<div class="row">
<figure><img src="opt-a.png"><figcaption><b>A · Jewel case</b><span class="rec">Recommended</span><p>Medium density. Golden-ratio hero (1.618 : 1) with the section medallion, 12-petal rail with each section’s motif, arch-top cards like petals in a velvet case. Structured and readable for 36 long cards.</p></figcaption></figure>
<figure><img src="opt-b.png"><figcaption><b>B · Orbit</b><p>High density. Centered symmetry, coin medallions in the rail, concentric rings behind the hero, circular product wells with double metal rings. Most mandala-like, but heavy for long shopping pages and centered body text reads worse.</p></figcaption></figure>
<figure><img src="opt-c.png"><figcaption><b>C · Ledger</b><p>Low density. Text tabs, no hero medallion, flat cards with one metal top rule and a small corner motif. Calm and fast, but the sacred-geometry identity nearly disappears: too close to a normal store, and to PCC.</p></figcaption></figure>
</div></body></html>'''
open(f'{OUT}/sheet.html','w').write(sheet)
print('options ok')
