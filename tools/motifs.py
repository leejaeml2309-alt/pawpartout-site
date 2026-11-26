"""Pawpartout section geometries, hand-built as SVG (no image generation).
Every motif lives in a 0..100 viewBox and is drawn as polished metal via
userSpaceOnUse gradients (same coordinate space for every motif)."""
import math
PHI=(1+5**.5)/2; GA=math.pi*(3-5**.5)  # golden angle
F=lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')

METALS={ # hi, light, mid, deep, shadow
 'gold':    ('#fff6d2','#f3d98f','#d6b25e','#9a722b','#5c3f10'),
 'silver':  ('#ffffff','#e6eaf0','#b3bbc8','#737c8d','#3c4250'),
 'platinum':('#fbfdff','#e4ebf3','#c6d0dc','#8d99ab','#4a5466'),
 'copper':  ('#ffe0c6','#f0a978','#c9713f','#87401c','#4a200c'),
 'rose':    ('#fff0ea','#efbfb0','#c98c7b','#8c5448','#4d2a24'),
}
METAL_NAME={'gold':'Gold','silver':'Silver','platinum':'Platinum','copper':'Copper','rose':'Rose bronze'}

def gradients():
    out=[]
    for m,(hi,l,mid,dp,sh) in METALS.items():
        # diagonal polished band: dark-light-dark-light, like a turned ring
        out.append(f'<linearGradient id="m-{m}" gradientUnits="userSpaceOnUse" x1="8" y1="0" x2="92" y2="100">'
                   f'<stop offset="0" stop-color="{l}"/><stop offset=".22" stop-color="{hi}"/><stop offset=".42" stop-color="{mid}"/>'
                   f'<stop offset=".58" stop-color="{dp}"/><stop offset=".78" stop-color="{l}"/><stop offset="1" stop-color="{mid}"/></linearGradient>')
        out.append(f'<radialGradient id="mr-{m}" gradientUnits="objectBoundingBox" cx=".35" cy=".3" r=".75">'
                   f'<stop offset="0" stop-color="{hi}"/><stop offset=".45" stop-color="{l}"/><stop offset=".8" stop-color="{mid}"/><stop offset="1" stop-color="{dp}"/></radialGradient>')
    return ''.join(out)

WMUL=1.0
def J(d,w=1.6,extra=''):
    """jewel stroke: drop shadow + metal stroke + fine highlight"""
    w=w*WMUL
    return (f'<path d="{d}" fill="none" stroke="#01040d" stroke-opacity=".55" stroke-width="{F(w+.6)}" transform="translate(.5 .8)" stroke-linecap="round" stroke-linejoin="round"{extra}/>'
            f'<path d="{d}" fill="none" stroke="var(--mg)" stroke-width="{F(w)}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="{F(w*.28)}" transform="translate(-.25 -.35)" stroke-linecap="round" stroke-linejoin="round"{extra}/>')
def JF(d):
    """jewel fill (solid metal shape)"""
    return (f'<path d="{d}" fill="#01040d" fill-opacity=".5" transform="translate(.5 .8)"/>'
            f'<path d="{d}" fill="var(--mg)"/>')
def circ(cx,cy,r):
    return f'M{F(cx-r)} {F(cy)}a{F(r)} {F(r)} 0 1 0 {F(2*r)} 0a{F(r)} {F(r)} 0 1 0 {F(-2*r)} 0z'
def dot(cx,cy,r): return circ(cx,cy,r)
def leaf(x1,y1,x2,y2,bulge=.32):
    """vesica leaf between two points"""
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1; nx,ny=-dy*bulge,dx*bulge
    return f'M{F(x1)} {F(y1)}Q{F(mx+nx)} {F(my+ny)} {F(x2)} {F(y2)}Q{F(mx-nx)} {F(my-ny)} {F(x1)} {F(y1)}z'

# ---------------- motifs ----------------
def m_seed():  # Seed of Life + six leaf tips (PPC, Blog, the core)
    r=15; d=circ(50,50,r)+''.join(circ(50+r*math.cos(k*math.pi/3),50+r*math.sin(k*math.pi/3),r) for k in range(6))
    lv=''.join(leaf(50+31*math.cos(a),50+31*math.sin(a),50+45*math.cos(a),50+45*math.sin(a),.42) for a in [k*math.pi/3+math.pi/6 for k in range(6)])
    return J(d+circ(50,50,30.5),1.5)+JF(lv)

def m_hex():   # beehive: 7 hexagons, a six-petal flower in the heart cell (Paw Shop)
    s=13.2; out=''
    def hx(cx,cy,s):
        return 'M'+'L'.join(f'{F(cx+s*math.cos(math.pi/6+k*math.pi/3))} {F(cy+s*math.sin(math.pi/6+k*math.pi/3))}' for k in range(6))+'z'
    cells=[(0,0)]+[(s*3**.5*math.cos(k*math.pi/3),s*3**.5*math.sin(k*math.pi/3)) for k in range(6)]
    d=''.join(hx(50+x,50+y,s-1.3) for x,y in cells)
    fl=''.join(leaf(50,50,50+8.6*math.cos(k*math.pi/3-math.pi/2),50+8.6*math.sin(k*math.pi/3-math.pi/2),.36) for k in range(6))
    return J(d,1.5)+JF(fl+dot(50,50,1.6))

def m_phyllo(n=110,inner=0,c=3.55):  # sunflower: golden-angle florets + ring of petals (Gifts)
    out=''
    pts=''
    for i in range(1,n):
        r=c*math.sqrt(i)
        if r>36: break
        if r<inner: continue
        a=i*GA; pts+=dot(50+r*math.cos(a),50+r*math.sin(a),.55+r*.034)
    pet=''.join(leaf(50+37*math.cos(k*2*math.pi/21),50+37*math.sin(k*2*math.pi/21),50+48*math.cos(k*2*math.pi/21),50+48*math.sin(k*2*math.pi/21),.3) for k in range(21))
    return JF(pts)+J(pet,.8)

def m_waves():  # ripples / waves inside a circle (Paw News)
    d=''
    for j,y in enumerate([34,44,54,64]):
        amp=5.2-j*.4; seg=''
        x0=14; seg=f'M{x0} {y}'
        for k in range(6):
            xa=x0+k*12
            seg+=f'Q{F(xa+3)} {F(y-amp*(1 if k%2==0 else -1))} {F(xa+6)} {y}T{F(xa+12)} {y}' if False else f'C{F(xa+3)} {F(y-amp)} {F(xa+9)} {F(y-amp)} {F(xa+12)} {y}' if k%2==0 else f'C{F(xa+3)} {F(y+amp)} {F(xa+9)} {F(y+amp)} {F(xa+12)} {y}'
        d+=seg
    return J(circ(50,50,44),1.4)+J(d,1.5)+JF(leaf(50,7,50,17,.45)+leaf(50,83,50,93,.45))

def m_nautilus():  # logarithmic spiral with chamber walls (Books)
    b=math.log(PHI)/(math.pi/2); pts=[]; walls=''
    for i in range(0,421):
        t=i/420*4.2*math.pi; r=2.2*math.exp(b*t*.92)
        pts.append((50+r*math.cos(t),52+r*math.sin(t)))
    d='M'+'L'.join(f'{F(x)} {F(y)}' for x,y in pts)
    for k in range(6,22):
        t=k*.6; r=2.2*math.exp(b*t*.92); r2=2.2*math.exp(b*(t+2*math.pi)*.92)
        if r2>44: continue
        walls+=f'M{F(50+r*math.cos(t))} {F(52+r*math.sin(t))}Q{F(50+(r+r2)/2*math.cos(t+.35))} {F(52+(r+r2)/2*math.sin(t+.35))} {F(50+r2*math.cos(t))} {F(52+r2*math.sin(t))}'
    return J(d,1.8)+J(walls,.9)

def m_fern():  # fractal frond (Camping & Road trip)
    out=''
    stem=[]
    for i in range(41):
        t=i/40; x=50+14*math.sin(t*1.6)-7; y=92-t*80; stem.append((x,y))
    d='M'+'L'.join(f'{F(x)} {F(y)}' for x,y in stem)
    lv=''
    for k in range(2,38,3):
        x,y=stem[k]; t=k/40; L=(1-t)*24/PHI+3
        for sgn in (-1,1):
            a=math.radians(-90+sgn*(58-t*18))
            lv+=leaf(x,y,x+L*math.cos(a),y+L*math.sin(a),.28)
    lv+=leaf(*stem[38],*stem[40],.5)
    return J(d,1.8)+JF(lv)

def m_pinecone():  # cone scales on two spiral families (Pet-friendly stays)
    out=''; sc=''
    for i in range(1,70):
        r=math.sqrt(i)/math.sqrt(70); a=i*GA
        x=50+r*28*math.cos(a)*(1-.25*r); y=56+r*38*math.sin(a)
        s=1.2+3.2*(1-r*.5)
        # tear/scale pointing outward-down
        sc+=leaf(x,y-s,x,y+s,.55)
    outline=f'M50 14C69 22 80 44 78 62C76 82 62 94 50 95C38 94 24 82 22 62C20 44 31 22 50 14z'
    stem='M50 14C50 9 52 6 56 4'
    return J(outline+stem,1.4)+JF(sc)

def m_burst():  # golden-angle starburst (Events & festivals)
    d=''; dots=''
    for i in range(1,34):
        a=i*GA; L=14+ (i%5)*5.5+ (i/34)*12
        L=min(L,45)
        x0,y0=50+6*math.cos(a),50+6*math.sin(a); x1,y1=50+L*math.cos(a),50+L*math.sin(a)
        d+=f'M{F(x0)} {F(y0)}L{F(x1)} {F(y1)}'; dots+=dot(x1,y1,1.1+(i%3)*.35)
    return J(d,.9)+JF(dots+circ(50,50,4.5))

def m_golden():  # Fibonacci squares + quarter-arc spiral (Travel memories: photo frames)
    # golden rectangle 86 x 53.2 centered
    W=86; H=W/PHI; x,y=50-W/2,50-H/2
    rects=''; arcs=''; cx,cy,w,h=x,y,W,H; dirn=0
    for k in range(7):
        if dirn==0: s=h; rects+=f'M{F(cx)} {F(cy)}h{F(s)}v{F(s)}h{F(-s)}z'; arcs+=f'M{F(cx)} {F(cy+s)}A{F(s)} {F(s)} 0 0 1 {F(cx+s)} {F(cy)}'; cx+=s; w-=s
        elif dirn==1: s=w; rects+=f'M{F(cx)} {F(cy)}h{F(s)}v{F(s)}h{F(-s)}z'; arcs+=f'M{F(cx)} {F(cy)}A{F(s)} {F(s)} 0 0 1 {F(cx+s)} {F(cy+s)}'; cy+=s; h-=s
        elif dirn==2: s=h; rects+=f'M{F(cx+w-s)} {F(cy)}h{F(s)}v{F(s)}h{F(-s)}z'; arcs+=f'M{F(cx+w)} {F(cy)}A{F(s)} {F(s)} 0 0 1 {F(cx+w-s)} {F(cy+s)}'; w-=s
        else: s=w; rects+=f'M{F(cx)} {F(cy+h-s)}h{F(s)}v{F(s)}h{F(-s)}z'; arcs+=f'M{F(cx+s)} {F(cy+h)}A{F(s)} {F(s)} 0 0 1 {F(cx)} {F(cy+h-s)}'; h-=s
        dirn=(dirn+1)%4
    return J(rects,.8)+J(arcs,2)

def m_flake():  # six-fold crystal (24/7 vet: clarity, care)
    d=''
    for k in range(6):
        a=k*math.pi/3-math.pi/2; ca,sa=math.cos(a),math.sin(a)
        d+=f'M{F(50+6*ca)} {F(50+6*sa)}L{F(50+42*ca)} {F(50+42*sa)}'
        for t,L in ((18,9),(28,7),(36,4.5)):
            px,py=50+t*ca,50+t*sa
            for sg in (-1,1):
                b=a+sg*math.pi/3; d+=f'M{F(px)} {F(py)}L{F(px+L*math.cos(b))} {F(py+L*math.sin(b))}'
    hexa='M'+'L'.join(f'{F(50+6*math.cos(k*math.pi/3))} {F(50+6*math.sin(k*math.pi/3))}' for k in range(6))+'z'
    return J(d+hexa,1.5)

def m_hexafoil():  # Flower of Life petals with a heart (Adoption)
    r=20; pet=''
    for k in range(6):
        a=k*math.pi/3-math.pi/2
        pet+=leaf(50,50,50+2*r*math.cos(a)*.98,50+2*r*math.sin(a)*.98,.29)
    heart='M50 58c-6-4.4-9.6-7.4-9.6-11.4a4.8 4.8 0 0 1 9.6-1.6a4.8 4.8 0 0 1 9.6 1.6c0 4-3.6 7-9.6 11.4z'
    return J(pet+circ(50,50,2*r+3),1.3)+JF(heart)

def m_rings():  # interlocking circles (Forum: voices that overlap)
    r=17; d=''.join(circ(50+12*math.cos(a),52+12*math.sin(a),r) for a in (-math.pi/2,math.pi/6,5*math.pi/6))
    return J(d+circ(50,50,43),1.5)+JF(leaf(50,5,50,13,.45))

def m_phyllo_ring(): return m_phyllo(n=260,inner=27.6,c=2.35)
def m_rule():
    d=circ(60,15,9)+circ(75,15,9)+circ(90,15,9)
    lv=leaf(46,15,30,15,.3)+leaf(104,15,120,15,.3)+leaf(52,9,44,3,.35)+leaf(98,9,106,3,.35)+leaf(52,21,44,27,.35)+leaf(98,21,106,27,.35)
    return J(d,1.1)+JF(lv+dot(75,15,1.8)+dot(24,15,1.4)+dot(126,15,1.4))

MOTIFS={'seed':m_seed,'hex':m_hex,'phyllo':m_phyllo,'waves':m_waves,'nautilus':m_nautilus,'fern':m_fern,
        'pinecone':m_pinecone,'burst':m_burst,'golden':m_golden,'flake':m_flake,'hexafoil':m_hexafoil,'rings':m_rings,'phyllo-ring':m_phyllo_ring,'rule':m_rule}

# the 12 petals in rosace order, plus the motif + metal of each
SECTIONS=[
 # key, label, sub, href(None=soon), motif, metal, why
 ('ppc','PetPolicyCheck','Pet travel rules','https://petpolicycheck.com/','seed','gold','The master frame: the Seed of Life is the rosace itself.'),
 ('news','Paw News','Rule updates','https://petpolicycheck.com/news/','waves','platinum','News travels in waves; platinum for cool, factual information.'),
 ('blog','Blog','Tickets & Tails','https://ticketsntails.com/','seed','gold','A door like PetPolicyCheck, so the same Seed of Life.'),
 ('books','Books','Future Noctis','/books/','nautilus','gold','The nautilus grows chamber by chamber, like chapters.'),
 ('shop','Paw Shop','Gear for pets','/shop/','hex','copper','Beehive cells: an ordered store of good things.'),
 ('forum','Forum','EN · KO','https://petpolicycheck.com/forum/','rings','silver','Interlocking circles: many voices, one conversation.'),
 ('adoption','Adoption','Open now','https://petpolicycheck.com/adoptions/','hexafoil','rose','Flower of Life petals around a heart.'),
 ('camping','Camping & Road trip','Coming soon',None,'fern','copper','A fern frond: self-similar growth, the outdoors.'),
 ('stays','Pet-friendly stays','Coming soon',None,'pinecone','rose','A pine cone: shelter, cabins, scales on two spirals.'),
 ('events','Events & festivals','Coming soon',None,'burst','gold','A golden-angle burst: fireworks without chaos.'),
 ('memories','Travel memories','Coming soon',None,'golden','silver','Golden rectangles are photo frames; the spiral is the journey.'),
 ('vet','24/7 vet emergencies','Coming soon',None,'flake','platinum','A crystal: clarity and calm when it matters.'),
]
EXTRA=[('gifts','Gifts for pets','Inside Paw Shop','/shop/gifts/','phyllo','rose','Sunflower phyllotaxis: the golden angle, a gift that keeps unfolding.')]

SMALL=('seed','hex','phyllo','waves','nautilus','fern','pinecone','burst','golden','flake','hexafoil','rings')
def symbols():
    """<symbol> per motif, metal applied by the user via CSS var --mg; '-s' = heavier strokes for icon sizes"""
    global WMUL
    WMUL=2.6
    small=''.join(f'<symbol id="g-{k}-s" viewBox="0 0 100 100">{MOTIFS[k]()}</symbol>' for k in SMALL)
    WMUL=1.0
    return small+''.join(f'<symbol id="g-{k}" viewBox="{"0 0 150 30" if k=="rule" else "0 0 100 100"}">{f()}</symbol>' for k,f in MOTIFS.items())

def sprite():
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
            + gradients() + symbols() + '</defs></svg>')

def icon(motif,metal,cls='',size=None,small=False):
    if small: motif+='-s'
    sz=f' width="{size}" height="{size}"' if size else ''
    return f'<svg class="mo {cls}" viewBox="0 0 100 100"{sz} style="--mg:url(#m-{metal})" aria-hidden="true" focusable="false"><use href="#g-{motif}"/></svg>'
