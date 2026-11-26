"""Pawpartout section geometries, hand-built as SVG (no image generation).
Every motif lives in a 0..100 viewBox and is drawn as polished metal via
userSpaceOnUse gradients (same coordinate space for every motif)."""
import math
PHI=(1+5**.5)/2; GA=math.pi*(3-5**.5)  # golden angle
F=lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')

METALS={ # hi, light, mid, deep, shadow
 'gold':    ('#fff3c0','#e8c05a','#d4a13a','#a06a18','#7a5410'),
 'silver':  ('#f5f7fa','#e8eef4','#c5d0dc','#8a9aa8','#4a5560'),
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
def JC(d,w=.55,op=.4,dash=None,scale=.42):
    """Construction stroke in the same metal (no jewel shadow, so it stays clean).
    scale=.42 (default) keeps lines thin at icon size; scale=1 lets them track WMUL
    when a motif must stay readable at 30px (Paw News rosace)."""
    w=w*max(1.0,WMUL*scale)
    ds=f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="{d}" fill="none" stroke="var(--mg)" stroke-opacity="{op}" '
            f'stroke-width="{F(w)}" stroke-linecap="round" stroke-linejoin="round"{ds}/>')
def JD(cx,cy,r=1.1,op=.55):
    """Construction point: a small filled disc in the same metal."""
    r=r*max(1.0,WMUL*.35)
    return f'<path d="{circ(cx,cy,r)}" fill="var(--mg)" fill-opacity="{op}"/>'
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

def m_waves():  # sine wave constructed on the Seed of Life (Paw News)
    """One sine period across the rosace. Amplitude = Seed radius (tangent to the
    top of the left circle and the bottom of the right). The Seed of Life is drawn
    in a stronger platinum so it still reads at 30px; the wave stays the dominant
    motif. At icon size (WMUL>1) the 60°/90° grid is dropped, leaving the seven
    circles, the outer circumcircle and the axis."""
    r=16
    # seven Seed circles (centre + 6) as one path, plus the outer circumcircle
    seed=circ(50,50,r)+''.join(circ(50+r*math.cos(k*math.pi/3),50+r*math.sin(k*math.pi/3),r) for k in range(6))
    outer=circ(50,50,2*r)
    T,A=4*r,r
    x0=50-2*r
    axis=f'M{F(x0-3)} 50H{F(x0+T+3)}'
    d=f'M{F(x0)} 50'+''.join(f'L{F(x0+T*i/180)} {F(50-A*math.sin(2*math.pi*i/180))}' for i in range(1,181))
    small=WMUL>=1.8
    if small:
        # Thicker, higher-contrast Seed; no grid. scale=1 so stroke tracks WMUL fully.
        return (JC(seed,1.25,.84,scale=1)+JC(outer,.9,.62,scale=1)+JC(axis,.8,.55,scale=1)
                +JD(50,50,1.7,.85)+J(d,2.2))
    # Card size: stronger Seed than v1, a light 90° construction only (no 60° net)
    angs=(0,90,180,270,360)
    horiz=''.join(f'M{F(x0-2)} {F(50-A*math.sin(math.radians(a)))}H{F(x0+T+2)}' for a in angs)
    verts=''.join(f'M{F(x0+T*(a/360))} {F(50-A-2)}V{F(50+A+2)}' for a in angs)
    dots=''.join(JD(x0+T*(a/360),50-A*math.sin(math.radians(a)),1.25,.78) for a in angs)
    radii=''.join(f'M50 50L{F(50+r*math.cos(math.radians(a)-math.pi/2))} {F(50+r*math.sin(math.radians(a)-math.pi/2))}'
                  for a in (0,90,180,270))
    angmk=f'M{F(50+5)} 50A5 5 0 0 0 50 {F(50-5)}'
    return (JC(seed,1.15,.78)+JC(outer,.8,.5)+JC(axis,.7,.52)+JC(horiz,.4,.28)+JC(verts,.4,.28)
            +JC(radii,.55,.4)+JC(angmk,.65,.55)+JD(50,50,1.5,.75)+dots+J(d,2.2))

def m_nautilus():  # chambered nautilus (Books): several turns, curved septa, golden-rectangle filigree
    """A slower-than-φ logarithmic spiral so three and a half turns wind visibly to the
    centre inside the viewBox. Curved septa join each point to the previous turn on the
    same ray (bowed toward the aperture). Behind, a light golden-rectangle construction
    in filigree. At icon size: three turns, fewer septa, no filigree, so the shell stays
    legible at 30px. Distinct from Travel memories (a silver rectangle whose spiral is
    the frame) and from Blog (Metatron’s Cube)."""
    small=WMUL>=1.8
    turns=3.0 if small else 3.5
    n_septa=8 if small else 16
    r_in,r_out,rot,bulge=2.2,42.0,-0.55,0.36 if small else 0.42
    tmax=2*math.pi*turns
    gro=math.log(r_out/r_in)/tmax
    n=520
    raw=[]
    for i in range(n+1):
        t=tmax*i/n
        r=r_in*math.exp(gro*t)
        ang=t+rot
        raw.append((r*math.cos(ang),r*math.sin(ang)))
    xs=[p[0] for p in raw]; ys=[p[1] for p in raw]
    minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
    pad=7
    sc=min((100-2*pad)/(maxx-minx),(100-2*pad)/(maxy-miny))
    ox=50-(minx+maxx)/2*sc
    oy=50-(miny+maxy)/2*sc
    def P(x,y): return (ox+x*sc, oy+y*sc)
    pts=[P(x,y) for x,y in raw]
    spiral='M'+'L'.join(f'{F(x)} {F(y)}' for x,y in pts)
    pole=P(0,0)
    walls=''
    t0,t1=2*math.pi+0.15,tmax-0.25
    if n_septa>1 and t1>t0:
        for i in range(n_septa):
            t=t0+(t1-t0)*i/(n_septa-1)
            r1=r_in*math.exp(gro*t)
            r0=r_in*math.exp(gro*(t-2*math.pi))
            a1=t+rot
            rm=(r0+r1)/2
            x0,y0=P(r0*math.cos(a1),r0*math.sin(a1))
            x1,y1=P(r1*math.cos(a1),r1*math.sin(a1))
            xc,yc=P(rm*math.cos(a1+bulge),rm*math.sin(a1+bulge))
            walls+=f'M{F(x0)} {F(y0)}Q{F(xc)} {F(yc)} {F(x1)} {F(y1)}'
    out=''
    if not small:
        # filigree: Fibonacci squares of a golden rectangle, faint, behind the shell
        W=80; H=W/PHI
        x0r,y0r=50-W/2,50-H/2
        cx,cy,w,h=x0r,y0r,W,H
        dirn=0; rects=''; arcs=''
        for _ in range(6):
            if dirn==0:
                s=h; rects+=f'M{F(cx)} {F(cy)}h{F(s)}v{F(s)}h{F(-s)}z'
                arcs+=f'M{F(cx)} {F(cy+s)}A{F(s)} {F(s)} 0 0 1 {F(cx+s)} {F(cy)}'
                cx+=s; w-=s
            elif dirn==1:
                s=w; rects+=f'M{F(cx)} {F(cy)}h{F(s)}v{F(s)}h{F(-s)}z'
                arcs+=f'M{F(cx)} {F(cy)}A{F(s)} {F(s)} 0 0 1 {F(cx+s)} {F(cy+s)}'
                cy+=s; h-=s
            elif dirn==2:
                s=h; rects+=f'M{F(cx+w-s)} {F(cy)}h{F(s)}v{F(s)}h{F(-s)}z'
                arcs+=f'M{F(cx+w)} {F(cy)}A{F(s)} {F(s)} 0 0 1 {F(cx+w-s)} {F(cy+s)}'
                w-=s
            else:
                s=w; rects+=f'M{F(cx)} {F(cy+h-s)}h{F(s)}v{F(s)}h{F(-s)}z'
                arcs+=f'M{F(cx+s)} {F(cy+h)}A{F(s)} {F(s)} 0 0 1 {F(cx)} {F(cy+h-s)}'
                h-=s
            dirn=(dirn+1)%4
        frame=f'M{F(x0r)} {F(y0r)}h{F(W)}v{F(H)}h{F(-W)}z'
        out+=JC(frame+rects,.55,.32)+JC(arcs,.5,.22)
    out+=J(walls,1.05 if not small else .95)+J(spiral,1.95)+JD(pole[0],pole[1],1.4,.85)
    return out

def m_sierpinski():  # Sierpinski triangle (Camping & Road trip)
    """Equilateral triangle subdivided at midpoints (depth 4). Construction: circumcircle,
    altitude, vertices and midpoints, first two generations of medial triangles. The
    remaining upright triangles are solid metal. Depth 4 stays crisp at 30px and at card size
    (a Barnsley fern was clearer at 150px but collapsed to a leaf-icon at 30px)."""
    s=80; h=s*3**.5/2
    top=(50,50-2*h/3); bl=(50-s/2,50+h/3); br=(50+s/2,50+h/3)
    def mid(p,q): return ((p[0]+q[0])/2,(p[1]+q[1])/2)
    up=[]
    def rec(a,b,c,d):
        if d==0: up.append((a,b,c)); return
        ab,bc,ca=mid(a,b),mid(b,c),mid(c,a)
        rec(a,ab,ca,d-1); rec(ab,b,bc,d-1); rec(ca,bc,c,d-1)
    rec(top,bl,br,4)
    fill=''.join(f'M{F(a[0])} {F(a[1])}L{F(b[0])} {F(b[1])}L{F(c[0])} {F(c[1])}z' for a,b,c in up)
    outer=f'M{F(top[0])} {F(top[1])}L{F(bl[0])} {F(bl[1])}L{F(br[0])} {F(br[1])}z'
    mab,mbc,mca=mid(top,bl),mid(bl,br),mid(br,top)
    mid1=f'M{F(mab[0])} {F(mab[1])}L{F(mbc[0])} {F(mbc[1])}L{F(mca[0])} {F(mca[1])}z'
    mid2=''
    for a,b,c in ((top,mab,mca),(mab,bl,mbc),(mca,mbc,br)):
        ab,bc,ca=mid(a,b),mid(b,c),mid(c,a)
        mid2+=f'M{F(ab[0])} {F(ab[1])}L{F(bc[0])} {F(bc[1])}L{F(ca[0])} {F(ca[1])}z'
    alt=f'M{F(top[0])} {F(top[1])}V{F(bl[1])}'
    R=2*h/3
    pts=(JD(*top,1.2,.65)+JD(*bl,1.2,.65)+JD(*br,1.2,.65)
         +JD(*mab,1.1,.6)+JD(*mbc,1.1,.6)+JD(*mca,1.1,.6)+JD(50,50,1.15,.55))
    return (JC(circ(50,50,R),.5,.28)+JC(alt,.45,.32,dash='1.2 1.6')
            +JC(outer,.7,.42)+JC(mid1,.6,.4)+JC(mid2,.4,.28)+pts
            +f'<path d="{fill}" fill="var(--mg)"/>'+J(outer,1.5))

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

def m_rings():  # Vesica Piscis (Forum: two voices meeting)
    """Two circles, each through the other's centre. Construction: the axis of centres,
    the chord through the intersection points, the two equilateral triangles, and 60°
    arcs at each centre. The vesica (intersection) is solid metal."""
    r=27
    c1x,c1y,c2x,c2y=50,50-r/2,50,50+r/2
    dx=(3**.5/2)*r; iL,iR=50-dx,50+dx
    circles=circ(c1x,c1y,r)+circ(c2x,c2y,r)
    axis=f'M50 {F(c1y-r-1.5)}V{F(c2y+r+1.5)}'
    chord=f'M{F(iL-3)} 50H{F(iR+3)}'
    tri=(f'M{F(c1x)} {F(c1y)}L{F(c2x)} {F(c2y)}L{F(iL)} 50Z'
         f'M{F(c1x)} {F(c1y)}L{F(c2x)} {F(c2y)}L{F(iR)} 50Z')
    def pt(cx,cy,a,rad): return F(cx+rad*math.cos(a)),F(cy+rad*math.sin(a))
    def arc(cx,cy,a0,a1,rad):
        x0,y0=pt(cx,cy,a0,rad); x1,y1=pt(cx,cy,a1,rad)
        return f'M{x0} {y0}A{F(rad)} {F(rad)} 0 0 1 {x1} {y1}'
    ar=7
    arcs=(arc(c1x,c1y,5*math.pi/6,math.pi/2,ar)+arc(c1x,c1y,math.pi/6,math.pi/2,ar)
         +arc(c2x,c2y,-5*math.pi/6,-math.pi/2,ar)+arc(c2x,c2y,-math.pi/6,-math.pi/2,ar))
    ves=(f'M{F(iL)} 50A{F(r)} {F(r)} 0 0 1 {F(iR)} 50A{F(r)} {F(r)} 0 0 1 {F(iL)} 50z')
    return (JC(axis+chord,.55,.45)+JC(tri,.45,.26)+JC(arcs,.75,.52)+JC(circles,.7,.38)
            +JD(c1x,c1y,1.45,.72)+JD(c2x,c2y,1.45,.72)+JD(iL,50,1.45,.72)+JD(iR,50,1.45,.72)
            +JD(50,50,1.05,.5)+JF(ves)+J(circles,1.55))

def m_phyllo_ring(): return m_phyllo(n=260,inner=27.6,c=2.35)
def m_rule():
    d=circ(60,15,9)+circ(75,15,9)+circ(90,15,9)
    lv=leaf(46,15,30,15,.3)+leaf(104,15,120,15,.3)+leaf(52,9,44,3,.35)+leaf(98,9,106,3,.35)+leaf(52,21,44,27,.35)+leaf(98,21,106,27,.35)
    return J(d,1.1)+JF(lv+dot(75,15,1.8)+dot(24,15,1.4)+dot(126,15,1.4))

def m_metatron():  # Metatron's Cube (Blog): 13 circles of the Fruit of Life, joined by lines
    """Centre + 6 at 2r + 6 at 4r (pointy-top). Circles are externally tangent, not the
    overlapping Seed of Life. At card size every centre is joined to every other (the
    classic cube). At icon size the line set is reduced (spokes, inner and outer hexagons,
    the hexagram, and laterals) so all 13 circles stay visible at 30px. Distinct from
    Books (nautilus) and from PetPolicyCheck (Seed of Life)."""
    r=9.0
    angs=[k*math.pi/3-math.pi/2 for k in range(6)]
    mid=[(50+2*r*math.cos(a),50+2*r*math.sin(a)) for a in angs]
    out=[(50+4*r*math.cos(a),50+4*r*math.sin(a)) for a in angs]
    pts=[(50,50)]+mid+out
    circles=''.join(circ(x,y,r) for x,y in pts)
    def segs(pairs):
        d=''
        for i,j in pairs:
            x1,y1=pts[i]; x2,y2=pts[j]
            d+=f'M{F(x1)} {F(y1)}L{F(x2)} {F(y2)}'
        return d
    small=WMUL>=1.8
    if not small:
        pairs=[(i,j) for i in range(13) for j in range(i+1,13)]
        return JC(circles,1.05,.9)+J(segs(pairs),.7)+J(circles,1.35)
    spokes=[(0,7+k) for k in range(6)]
    inner_hex=[(1+k,1+(k+1)%6) for k in range(6)]
    outer_hex=[(7+k,7+(k+1)%6) for k in range(6)]
    tri_a=[(1,3),(3,5),(5,1)]; tri_b=[(2,4),(4,6),(6,2)]
    laterals=[]
    for k in range(6):
        laterals.append((1+k,7+(k+1)%6)); laterals.append((1+k,7+(k-1)%6))
    pairs=sorted({tuple(sorted(p)) for p in spokes+inner_hex+outer_hex+tri_a+tri_b+laterals})
    return JC(circles,1.15,.92,scale=1)+J(segs(pairs),.85)+J(circles,1.45)

MOTIFS={'seed':m_seed,'hex':m_hex,'phyllo':m_phyllo,'waves':m_waves,'nautilus':m_nautilus,'sierpinski':m_sierpinski,
        'pinecone':m_pinecone,'burst':m_burst,'golden':m_golden,'flake':m_flake,'hexafoil':m_hexafoil,'rings':m_rings,'metatron':m_metatron,'phyllo-ring':m_phyllo_ring,'rule':m_rule}

# the 12 petals in rosace order, plus the motif + metal of each
SECTIONS=[
 # key, label, sub, href(None=soon), motif, metal, why
 ('ppc','PetPolicyCheck','Pet travel rules','https://petpolicycheck.com/','seed','gold','The master frame: the Seed of Life is the rosace itself.'),
 ('news','Paw News','Rule updates','https://petpolicycheck.com/news/','waves','platinum','A sine wave constructed on the rosace: news travels as a measured oscillation.'),
 ('blog','Blog','Tickets & Tails','https://ticketsntails.com/','metatron','gold','Metatron\'s Cube: thirteen circles joined by straight lines — a story with its own architecture, not a spiral.'),
 ('books','Books','Future Noctis','/books/','nautilus','gold','A chambered nautilus: a logarithmic spiral of several turns, curved septa, and a golden-rectangle construction.'),
 ('shop','Paw Shop','Gear for pets','/shop/','hex','copper','Beehive cells: an ordered store of good things.'),
 ('forum','Forum','EN · KO','https://petpolicycheck.com/forum/','rings','silver','Vesica Piscis: two circles through each other\'s centres; two voices meeting.'),
 ('adoption','Adoption','Open now','https://petpolicycheck.com/adoptions/','hexafoil','rose','Flower of Life petals around a heart.'),
 ('camping','Camping & Road trip','Coming soon',None,'sierpinski','copper','A Sierpinski triangle: a crisp fractal built from midpoints, the same rule at every scale.'),
 ('stays','Pet-friendly stays','Coming soon',None,'pinecone','rose','A pine cone: shelter, cabins, scales on two spirals.'),
 ('events','Events & festivals','Coming soon',None,'burst','gold','A golden-angle burst: fireworks without chaos.'),
 ('memories','Travel memories','Coming soon',None,'golden','silver','Golden rectangles are photo frames; the spiral is the journey.'),
 ('vet','24/7 vet emergencies','Coming soon',None,'flake','platinum','A crystal: clarity and calm when it matters.'),
]
EXTRA=[('gifts','Gifts for pets','Inside Paw Shop','/shop/gifts/','phyllo','rose','Sunflower phyllotaxis: the golden angle, a gift that keeps unfolding.')]

SMALL=('seed','hex','phyllo','waves','nautilus','sierpinski','pinecone','burst','golden','flake','hexafoil','rings','metatron')
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
