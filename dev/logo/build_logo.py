import math, sys

NAVY_TOP = "#25446E"
NAVY_BOT = "#1B3354"
WHITE = "#FFFFFF"
HALO = 11  # écart sombre autour des serpents

def catmull(points, n=24):
    """Spline Catmull-Rom passant par les points -> liste dense."""
    pts = [points[0]] + points + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
        for j in range(n):
            t = j / n
            t2, t3 = t*t, t*t*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    out.append(points[-1])
    return out

def ribbon(center, w0, w1):
    """Contour d'un ruban d'épaisseur variable (w0 -> w1) le long d'une courbe."""
    n = len(center)
    left, right = [], []
    for i, (x, y) in enumerate(center):
        a = center[max(i-1, 0)]; b = center[min(i+1, n-1)]
        dx, dy = b[0]-a[0], b[1]-a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy/L, dx/L
        t = i/(n-1)
        w = (w0 + (w1-w0)*t) / 2
        left.append((x+nx*w, y+ny*w)); right.append((x-nx*w, y-ny*w))
    tail = center[-1]; pre = center[-4]
    dx, dy = tail[0]-pre[0], tail[1]-pre[1]; L = math.hypot(dx, dy) or 1
    tip = (tail[0]+dx/L*w1*0.9, tail[1]+dy/L*w1*0.9)
    pts = left + [tip] + right[::-1]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"

def mirror_pts(pts):
    return [(1024-x, y) for x, y in pts]

# Ligne médiane du serpent « gauche » (tête à gauche, sous l'aile)
snake_L = [(470,352),(432,360),(398,384),(386,414),(398,446),(440,466),(512,478),(574,500),(596,536),(588,574),(552,596),(512,604),(466,622),(446,656),(454,694),(486,720),(526,738),(556,764),(562,798),(548,828)]
snake_R = mirror_pts(snake_L)

def head(cx, cy, ang, s=1):
    """Tête en goutte orientée selon ang (degrés)."""
    return (f'<g transform="translate({cx},{cy}) rotate({ang})">'
            f'<path d="M-30,0 C-30,-19 -8,-24 14,-17 C30,-12 40,-5 42,0 C40,5 30,12 14,17 C-8,24 -30,19 -30,0 Z"/>'
            f'</g>')

def snake_group(center_pts, hx, hy, hang, clip=None):
    dense = catmull(center_pts, 20)
    d = ribbon(dense, 38, 16)
    c = f' clip-path="url(#{clip})"' if clip else ""
    return (f'<g{c}>'
            f'<path d="{d}" fill="none" stroke="var(--halo)" stroke-width="{HALO*2}" stroke-linejoin="round"/>'
            f'<g fill="none" stroke="var(--halo)" stroke-width="{HALO*2}">{head(hx,hy,hang)}</g>'
            f'<path d="{d}" fill="var(--glyph)"/>'
            f'<g fill="var(--glyph)">{head(hx,hy,hang)}</g>'
            f'</g>')

# Aile gauche : silhouette festonnée + deux fentes (miroir pour la droite)
WING_L = ("M132,238 C200,200 300,170 372,168 C426,166 462,186 470,220 C478,252 474,294 458,322 "
          "C410,328 330,334 280,346 C292,334 302,326 312,320 C268,312 226,302 190,300 "
          "C198,292 206,286 214,282 C186,272 158,258 132,238 Z")
SLITS_L = ["M214,282 C260,262 306,248 348,239", "M312,320 C334,304 356,290 380,279"]

def wing_svg():
    one = (f'<path d="{WING_L}" fill="var(--glyph)" stroke="var(--glyph)" stroke-width="9" stroke-linejoin="round"/>'
           + "".join(f'<path d="{d}" fill="none" stroke="var(--halo)" stroke-width="13" stroke-linecap="round"/>' for d in SLITS_L))
    return one + f'<g transform="translate(1024,0) scale(-1,1)">{one}</g>'

def scale_arm(cx, sign):
    """Bras de balance : rotule, chaînes et plateau, centrés sur cx."""
    inner = cx + sign*150   # extrémité intérieure du fléau (cachée par le serpent)
    x0, x1 = sorted([cx, inner])
    return (f'<rect x="{x0-4}" y="404" width="{x1-x0+8}" height="22" rx="11"/>'
            f'<circle cx="{cx}" cy="415" r="21"/>'
            f'<path d="M{cx},428 L{cx-80},642 M{cx},428 L{cx+80},642" fill="none" stroke="var(--glyph)" stroke-width="19" stroke-linecap="round"/>'
            f'<path d="M{cx-98},644 L{cx+98},644 C{cx+98},688 {cx+56},722 {cx},722 C{cx-56},722 {cx-98},688 {cx-98},644 Z"/>')

def glyph(clip_ids=("cross2",)):
    staff = "M495,206 L529,206 L521,880 C521,893 503,893 503,880 Z"
    return f'''
  <g fill="var(--glyph)">
    {scale_arm(232, +1)}
    {scale_arm(792, -1)}
    <path d="{staff}"/>
    <circle cx="512" cy="182" r="38"/>
  </g>
  {wing_svg()}
  {snake_group(snake_L, 452, 349, -8)}
  {snake_group(snake_R, 572, 349, 188)}
  {snake_group(snake_L, 452, 349, -8, clip="cross2")}
'''

def svg(rounded=True, size=1024, bg=True, mono=None):
    rx = 224 if rounded else 0
    glyph_col = mono or WHITE
    halo_col = "url(#bg)" if bg else "none"
    style = f'--glyph:{glyph_col};--halo:{NAVY_BOT if bg else "transparent"}'
    bgrect = f'<rect width="1024" height="1024" rx="{rx}" fill="url(#bg)"/>' if bg else ""
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="bg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1024">
      <stop offset="0" stop-color="{NAVY_TOP}"/>
      <stop offset="1" stop-color="{NAVY_BOT}"/>
    </linearGradient>
    <clipPath id="cross2"><rect x="400" y="570" width="224" height="64"/></clipPath>
  </defs>
  {bgrect}
  <g style="{style}">{glyph()}</g>
</svg>'''
    # rsvg ne gère pas les variables CSS : on les remplace par les valeurs
    halo = "url(#bg)" if bg else "#000000"
    s = s.replace("var(--glyph)", glyph_col).replace("var(--halo)", halo).replace(f' style="{style}"', "")
    return s

if __name__ == "__main__":
    out = sys.argv[1]
    open(f"{out}/hermes-logo.svg", "w").write(svg(rounded=True))
    open(f"{out}/hermes-icon-square.svg", "w").write(svg(rounded=False))
