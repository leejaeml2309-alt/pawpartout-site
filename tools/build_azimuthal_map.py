#!/usr/bin/env python3
"""Build the Pawpartout North-Pole azimuthal equidistant SVG.

Land polygons come from Natural Earth 110m, via world-atlas
(Copyright 2013-2019 Michael Bostock, ISC license — see
tools/data/world-atlas-LICENSE.txt). Projection, compass ring,
and styling are original to Pawpartout. No UN wreath or emblem.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "tools/data/countries-110m.json"
OUT_SVG = ROOT / "site/assets/vet-azimuthal-map.svg"
OUT_PREVIEW = Path("/tmp/az-preview/az-final.png")

# ViewBox and projection
VB = 200.0
CX = 100.0
CY = 100.0
R = 79.0  # geographic disk radius (south pole sits on this circle)
# Longitude that points toward +y (down the page): central North America.
LAM0 = -100.0
# Pulse pin: northern Great Plains / US–Canada corridor.
PIN = (-95.0, 46.5)

USA_ID = "840"
CAN_ID = "124"

def load_atlas():
    return json.loads(ATLAS_PATH.read_text())


def decode_arcs(atlas):
    sx, sy = atlas["transform"]["scale"]
    tx, ty = atlas["transform"]["translate"]
    out = []
    for arc in atlas["arcs"]:
        pts = []
        x = y = 0
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        out.append(pts)
    return out


def ring_from_arcs(idxs, decoded):
    ring = []
    for idx in idxs:
        pts = decoded[~idx][::-1] if idx < 0 else decoded[idx][:]
        if ring:
            pts = pts[1:]
        ring.extend(pts)
    if len(ring) >= 2 and ring[0] == ring[-1]:
        ring = ring[:-1]
    return ring


def geom_polygons(geom, decoded):
    """Return a list of polygons, each a list of rings (lon, lat)."""
    if geom["type"] == "Polygon":
        polys = [geom["arcs"]]
    else:
        polys = geom["arcs"]
    out = []
    for poly in polys:
        rings = [ring_from_arcs(ring, decoded) for ring in poly]
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            out.append(rings)
    return out


def project(lon, lat):
    r = (90.0 - lat) / 180.0 * R
    th = math.radians(lon - LAM0)
    return (CX + r * math.sin(th), CY + r * math.cos(th))


def ring_contains(ring_xy, x, y):
    inside = False
    n = len(ring_xy)
    for i in range(n):
        x1, y1 = ring_xy[i]
        x2, y2 = ring_xy[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            x_int = (x2 - x1) * (y - y1) / (y2 - y1 + 1e-15) + x1
            if x < x_int:
                inside = not inside
    return inside


def simplify(pts, min_d=0.18):
    if not pts:
        return pts
    out = [pts[0]]
    for p in pts[1:]:
        dx = p[0] - out[-1][0]
        dy = p[1] - out[-1][1]
        if dx * dx + dy * dy >= min_d * min_d:
            out.append(p)
    if len(out) >= 3:
        dx = out[0][0] - out[-1][0]
        dy = out[0][1] - out[-1][1]
        if dx * dx + dy * dy < min_d * min_d:
            out.pop()
    return out


def fmt(n):
    s = f"{n:.2f}"
    if s.endswith(".00"):
        return s[:-3]
    if s.endswith("0") and "." in s:
        return s[:-1]
    return s


def path_from_xy_rings(rings, invert=False):
    parts = []
    if invert:
        # Outer disk, then each ring as a hole (even-odd).
        segs = 96
        parts.append(f"M{fmt(CX + R)},{fmt(CY)}")
        for i in range(1, segs + 1):
            a = (i / segs) * 2 * math.pi
            parts.append(f"L{fmt(CX + R * math.cos(a))},{fmt(CY + R * math.sin(a))}")
        parts.append("Z")
    for ring in rings:
        xy = simplify([project(lon, lat) for lon, lat in ring])
        if len(xy) < 3:
            continue
        parts.append(f"M{fmt(xy[0][0])},{fmt(xy[0][1])}")
        for x, y in xy[1:]:
            parts.append(f"L{fmt(x)},{fmt(y)}")
        parts.append("Z")
    return "".join(parts)


def circle_path(r, n=96):
    parts = [f"M{fmt(CX + r)},{fmt(CY)}"]
    for i in range(1, n + 1):
        a = (i / n) * 2 * math.pi
        parts.append(f"L{fmt(CX + r * math.cos(a))},{fmt(CY + r * math.sin(a))}")
    parts.append("Z")
    return "".join(parts)


def collect(atlas):
    decoded = decode_arcs(atlas)
    world = []
    usa = []
    canada = []
    for g in atlas["objects"]["countries"]["geometries"]:
        cid = str(g.get("id") or "")
        name = g.get("properties", {}).get("name") or ""
        polys = geom_polygons(g, decoded)
        if cid == USA_ID:
            usa.extend(polys)
        elif cid == CAN_ID:
            canada.extend(polys)
        else:
            world.extend(polys)
    return world, usa, canada


def classify_poly(poly):
    """Return (rings, invert?). Invert if the outer ring encloses the North Pole
    in this projection (Antarctica: land is the outer band toward the rim)."""
    outer = [project(lon, lat) for lon, lat in poly[0]]
    invert = ring_contains(outer, CX, CY)
    return poly, invert


def paths_for(polys):
    """Split inverted polygons (Antarctica) so their disk-ring path is
    never evenodd-merged with the rest of the world."""
    regular, inverted = [], []
    for poly in polys:
        rings, invert = classify_poly(poly)
        d = path_from_xy_rings(rings, invert=invert)
        if not d:
            continue
        (inverted if invert else regular).append(d)
    return regular, inverted


def compass_ticks():
    """Return SVG for the decorative compass / rosace ring."""
    bits = []
    # Double antique-gold rings
    bits.append(
        f'<circle class="az-ring-outer" cx="{fmt(CX)}" cy="{fmt(CY)}" r="92.2" '
        f'fill="none" stroke="url(#az-gold)" stroke-width="1.35"/>'
    )
    bits.append(
        f'<circle class="az-ring-mid" cx="{fmt(CX)}" cy="{fmt(CY)}" r="88.35" '
        f'fill="none" stroke="#c8a258" stroke-width="0.7" stroke-opacity="0.95"/>'
    )
    bits.append(
        f'<circle class="az-ring-inner" cx="{fmt(CX)}" cy="{fmt(CY)}" r="80.4" '
        f'fill="none" stroke="#d9b775" stroke-width="0.45" stroke-opacity="0.7"/>'
    )
    # Ticks. 0° is the top of the *frame* (instrument), not geographic north.
    # Geographic meridians are already drawn inside the disk.
    def tick(deg, r0, r1, sw, color="#d9b775", cap="butt"):
        a = math.radians(deg - 90)  # 0 at top
        x0, y0 = CX + r0 * math.cos(a), CY + r0 * math.sin(a)
        x1, y1 = CX + r1 * math.cos(a), CY + r1 * math.sin(a)
        bits.append(
            f'<line x1="{fmt(x0)}" y1="{fmt(y0)}" x2="{fmt(x1)}" y2="{fmt(y1)}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="{cap}"/>'
        )

    for deg in range(0, 360, 5):
        if deg % 30 == 0:
            continue
        if deg % 15 == 0:
            tick(deg, 88.35, 91.7, 0.7, "#d9b775")
        else:
            tick(deg, 89.6, 91.15, 0.35, "rgba(217,183,117,0.7)")

    # 12 meridian-aligned major ticks, slightly longer
    for deg in range(0, 360, 30):
        tick(deg, 87.5, 92.55, 1.05, "#e8cb8c", "round")

    # Four cardinal jewels (frame N/E/S/W) — small diamonds, no letters
    for deg in (0, 90, 180, 270):
        a = math.radians(deg - 90)
        rm = 93.55
        x, y = CX + rm * math.cos(a), CY + rm * math.sin(a)
        # diamond in local radial frame
        radx, rady = math.cos(a), math.sin(a)
        txx, txy = -math.sin(a), math.cos(a)
        if deg == 0:
            # slightly larger pointer at the top, like a compass fleur
            p1 = (x + radx * 3.1, y + rady * 3.1)
            p2 = (x + txx * 1.35, y + txy * 1.35)
            p3 = (x - radx * 1.6, y - rady * 1.6)
            p4 = (x - txx * 1.35, y - txy * 1.35)
        else:
            p1 = (x + radx * 2.1, y + rady * 2.1)
            p2 = (x + txx * 1.15, y + txy * 1.15)
            p3 = (x - radx * 1.35, y - rady * 1.35)
            p4 = (x - txx * 1.15, y - txy * 1.15)
        pts = " ".join(f"{fmt(px)},{fmt(py)}" for px, py in (p1, p2, p3, p4))
        bits.append(f'<polygon points="{pts}" fill="#e8cb8c" stroke="#c8a258" stroke-width="0.25"/>')

    return "\n    ".join(bits)


def graticule():
    bits = []
    # Latitude circles
    for lat in (60, 30, 0, -30, -60):
        r = (90.0 - lat) / 180.0 * R
        op = "0.34" if lat == 0 else "0.22"
        sw = "0.7" if lat == 0 else "0.6"
        bits.append(
            f'<circle cx="{fmt(CX)}" cy="{fmt(CY)}" r="{fmt(r)}" fill="none" '
            f'stroke="rgba(217,183,117,{op})" stroke-width="{sw}"/>'
        )
    # 12 meridians
    for k in range(12):
        lon = LAM0 + k * 30
        x, y = project(lon, -90)
        bits.append(
            f'<line x1="{fmt(CX)}" y1="{fmt(CY)}" x2="{fmt(x)}" y2="{fmt(y)}" '
            f'stroke="rgba(217,183,117,0.22)" stroke-width="0.6"/>'
        )
    return "\n      ".join(bits)


def pin_group():
    x, y = project(*PIN)
    # Teardrop GPS pin: tip sits on the coordinate, bubble above (toward the pole).
    return f'''<g class="az-pin" transform="translate({fmt(x)} {fmt(y)})" aria-hidden="true">
        <circle class="az-ripple az-ripple-a" r="2.6" fill="none" stroke="#e0483d" stroke-width="0.65" pointer-events="none"/>
        <circle class="az-ripple az-ripple-b" r="2.6" fill="none" stroke="#e0483d" stroke-width="0.65" pointer-events="none"/>
        <g class="az-pin-mark" filter="url(#az-pin-shadow)">
          <path class="az-pin-body" d="M0,0C-.2-5.4-6.2-8.6-6.2-13.8A6.2,6.2 0 1 1 6.2-13.8C6.2-8.6.2-5.4,0,0Z" fill="#e0483d" stroke="#8f2a24" stroke-width="0.35" stroke-linejoin="round"/>
          <circle class="az-pin-dot" cx="0" cy="-13.8" r="2.15" fill="#fff"/>
        </g>
      </g>'''


def build_svg(world_regular, world_inverted, usa_paths, can_paths):
    world_d = "".join(world_regular)
    ant_d = "".join(world_inverted)
    usa_d = "".join(usa_paths)
    can_d = "".join(can_paths)
    px, py = project(*PIN)
    # soft glow centered on the NA highlight
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200" role="img" aria-labelledby="az-title az-desc">
  <!--
    Pawpartout North-Pole azimuthal equidistant world map.
    Land polygons derived from Natural Earth 110m via world-atlas
    (Copyright 2013-2019 Michael Bostock, ISC license).
    Projection and styling original to Pawpartout.
    No UN olive wreath, no UN emblem, no registered-mark symbols.
  -->
  <title id="az-title">United States and Canada on a North-Pole azimuthal world map</title>
  <desc id="az-desc">A circular North-Pole azimuthal equidistant map in navy and gold, with the United States and Canada highlighted. For use on the Pawpartout 24/7 vet emergencies page, covering the United States and Canada only.</desc>
  <defs>
    <linearGradient id="az-gold" x1="20" y1="8" x2="180" y2="190" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#e8c05a"/>
      <stop offset="0.22" stop-color="#fff3c0"/>
      <stop offset="0.45" stop-color="#d9b775"/>
      <stop offset="0.62" stop-color="#c8a258"/>
      <stop offset="0.82" stop-color="#e8c05a"/>
      <stop offset="1" stop-color="#c8a258"/>
    </linearGradient>
    <linearGradient id="az-silver" x1="78" y1="96" x2="124" y2="138" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f4f7fb"/>
      <stop offset="0.18" stop-color="#e4eaf1"/>
      <stop offset="0.52" stop-color="#bfc9d6"/>
      <stop offset="0.78" stop-color="#d8e0ea"/>
      <stop offset="1" stop-color="#eef2f6"/>
    </linearGradient>
    <radialGradient id="az-na-glow" cx="{fmt(px)}" cy="{fmt(py)}" r="28" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#e4eaf1" stop-opacity="0.32"/>
      <stop offset="0.55" stop-color="#c5d0dc" stop-opacity="0.1"/>
      <stop offset="1" stop-color="#c5d0dc" stop-opacity="0"/>
    </radialGradient>
    <filter id="az-pin-shadow" x="-120%" y="-80%" width="340%" height="260%">
      <feDropShadow dx="0" dy="0.9" stdDeviation="0.7" flood-color="#000010" flood-opacity="0.55"/>
    </filter>
    <clipPath id="az-disk">
      <circle cx="{fmt(CX)}" cy="{fmt(CY)}" r="{fmt(R)}"/>
    </clipPath>
  </defs>
  <g id="az-root">
    <circle class="az-ocean" cx="{fmt(CX)}" cy="{fmt(CY)}" r="{fmt(R)}" fill="#071330"/>
    <g class="az-clipped" clip-path="url(#az-disk)">
      <g class="az-graticule" fill="none">
        {graticule()}
      </g>
      <path class="az-world az-antarctica" d="{ant_d}" fill="rgba(217,183,117,0.22)" stroke="rgba(232,203,140,0.48)" stroke-width="0.35" stroke-linejoin="round" fill-rule="evenodd"/>
      <path class="az-world" d="{world_d}" fill="rgba(217,183,117,0.28)" stroke="rgba(232,203,140,0.58)" stroke-width="0.42" stroke-linejoin="round" fill-rule="evenodd"/>
      <circle class="az-na-glow" cx="{fmt(px)}" cy="{fmt(py)}" r="28" fill="url(#az-na-glow)"/>
      <g id="az-canada" class="az-na" data-country="canada">
        <path d="{can_d}" fill="url(#az-silver)" stroke="#f4f7fb" stroke-width="1.1" stroke-linejoin="round" fill-rule="evenodd"/>
      </g>
      <g id="az-usa" class="az-na" data-country="usa">
        <path d="{usa_d}" fill="url(#az-silver)" stroke="#f4f7fb" stroke-width="1.1" stroke-linejoin="round" fill-rule="evenodd"/>
      </g>
      {pin_group()}
    </g>
    {compass_ticks()}
  </g>
</svg>
'''
    return svg


def preview_png(world, usa, canada, path: Path):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    scale = 6
    S = int(VB * scale)
    im = Image.new("RGBA", (S, S), (6, 16, 40, 255))
    d = ImageDraw.Draw(im)

    def P(x, y):
        return x * scale, y * scale

    # ocean disk
    d.ellipse([P(CX - R, CY - R), P(CX + R, CY + R)], fill=(7, 19, 48, 255))

    def draw_polys(polys, fill, outline, ow=2):
        for poly in polys:
            rings, invert = classify_poly(poly)
            if invert:
                # mask: disk minus interior of outer ring
                # draw disk gold then punch? We'll draw the outer band by
                # polygon of circle + reversed coast — skip holes for preview.
                coast = [P(*project(lon, lat)) for lon, lat in rings[0]]
                circle = []
                for i in range(128):
                    a = i / 128 * 2 * math.pi
                    circle.append(P(CX + R * math.cos(a), CY + R * math.sin(a)))
                # even-odd: circle then coast
                mask = Image.new("L", (S, S), 0)
                md = ImageDraw.Draw(mask)
                md.polygon(circle, fill=255)
                md.polygon(coast, fill=0)
                layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
                ld = ImageDraw.Draw(layer)
                ld.bitmap((0, 0), Image.new("L", (S, S), 0))
                col = Image.new("RGBA", (S, S), fill)
                im.paste(col, mask=mask)
                d.line(coast + [coast[0]], fill=outline, width=ow)
                continue
            for i, ring in enumerate(rings):
                pts = [P(*project(lon, lat)) for lon, lat in ring]
                if i == 0:
                    d.polygon(pts, fill=fill)
                else:
                    d.polygon(pts, fill=(7, 19, 48, 255))
                d.line(pts + [pts[0]], fill=outline, width=ow)

    draw_polys(world, (217, 183, 117, 70), (217, 183, 117, 140), 1)
    draw_polys(usa, (230, 198, 130, 170), (232, 203, 140, 255), 3)
    draw_polys(canada, (230, 198, 130, 170), (232, 203, 140, 255), 3)

    # clip to disk
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([P(CX - R, CY - R), P(CX + R, CY + R)], fill=255)
    bg = Image.new("RGBA", (S, S), (6, 16, 40, 255))
    bg.paste(im, mask=mask)
    im = bg
    d = ImageDraw.Draw(im)
    # rings
    d.ellipse([P(CX - R, CY - R), P(CX + R, CY + R)], outline=(217, 183, 117, 200), width=3)
    d.ellipse([P(CX - 88.35, CY - 88.35), P(CX + 88.35, CY + 88.35)], outline=(200, 162, 88, 255), width=3)
    d.ellipse([P(CX - 92.2, CY - 92.2), P(CX + 92.2, CY + 92.2)], outline=(232, 203, 140, 255), width=5)
    px, py = P(*project(*PIN))
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(224, 83, 71, 255))
    path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(path)
    print("preview", path, im.size)


def main():
    atlas = load_atlas()
    world, usa, canada = collect(atlas)
    world_regular, world_inverted = paths_for(world)
    usa_paths, usa_inv = paths_for(usa)
    can_paths, can_inv = paths_for(canada)
    if usa_inv or can_inv:
        raise SystemExit("USA/Canada should not invert")
    svg = build_svg(world_regular, world_inverted, usa_paths, can_paths)
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUT_SVG.write_text(svg, encoding="utf-8")
    print("wrote", OUT_SVG, "bytes", OUT_SVG.stat().st_size)
    print("world", len(world_regular), "antarctica", len(world_inverted), "usa", len(usa_paths), "canada", len(can_paths))
    preview_png(world, usa, canada, OUT_PREVIEW)


if __name__ == "__main__":
    main()
