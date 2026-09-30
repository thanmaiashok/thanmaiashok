"""Pixel vines that overgrow the edges of SVG cards (Minecraft-style), deterministic per seed."""
import random, re, os, sys, zlib
U = 6
COL = {"D": "#2f5229", "M": "#4a7a3c", "L": "#69a04f"}

def _strand(cells, rnd, x, y, n, leaf=0.4, dirs=(0, 0, 0, 1, -1), inward=1, blob=0.0):
    cx = x
    for i in range(n):
        c = "L" if (i % 3 == 1) else "M"
        if i == n - 1: c = "D"
        cells[(cx, y + i * U)] = c
        if 0 < i < n - 1 and rnd.random() < leaf:
            lx = cx + inward * U
            cells[(lx, y + i * U)] = rnd.choice(["D", "M", "L"])
            if rnd.random() < blob:
                cells[(lx, y + (i + 1) * U)] = rnd.choice(["D", "M"])
                cells[(lx + inward * U, y + i * U)] = "D"
        if i > 0 and rnd.random() < 0.2: cx += rnd.choice(dirs) * U

def _moss(cells, rnd, x, y, w=None):
    w = w or rnd.randint(3, 6)
    for dx in range(w):
        h = rnd.randint(1, 4 if 0 < dx < w - 1 else 2)
        for k in range(h):
            cells[(x + dx * U, y - k * U)] = rnd.choice(["D", "M", "M", "L"]) if k else "D"

def vines(W, H, seed, kind="card", right_top=True, left_top=True, edge_only=False):
    rnd = random.Random(zlib.crc32(str(seed).encode()))
    cells = {}
    small = H < 70
    cap = max(2, int(H * (0.7 if small else 0.6) / U))
    # long strands clinging to both side edges (the main overgrown look)
    for side in (0, 1):
        for _ in range(rnd.randint(2, 4) if not small else rnd.randint(1, 2)):
            n = rnd.randint(min(4, cap), min(18, cap))
            k = 0 if edge_only else rnd.randrange(0, 3)
            x = k * U if side == 0 else W - U - k * U
            y = rnd.randrange(0, max(1, int(H * 0.22 / U))) * U
            _strand(cells, rnd, x, y, n, leaf=0.55, dirs=(0, 0, 0, 0, 1 if side == 0 else -1),
                    inward=1 if side == 0 else -1, blob=0.0 if edge_only else 0.35)
    # medium strands hanging from the top near the corners
    for zone, ok in (() if edge_only else (((30, 120), left_top), ((W - 150, W - 30), right_top))):
        if not ok: continue
        for _ in range(rnd.randint(1, 3)):
            x = rnd.randrange(zone[0] // U, zone[1] // U) * U
            _strand(cells, rnd, x, 0, rnd.randint(2, min(5, cap)), leaf=0.3)
    # moss fringe along the top edge
    for _ in range(max(2, int(W / 45))):
        x = rnd.randrange(0, W // U) * U
        _strand(cells, rnd, x, 0, rnd.randint(1, 2 if edge_only else 3), leaf=0.0)
    # moss on the bottom edge
    for x0 in (rnd.randrange(0, 8) * U, W - 6 * U - rnd.randrange(0, 8) * U):
        _moss(cells, rnd, x0, H - U)
    for _ in range(rnd.randint(0, 2)):
        _moss(cells, rnd, rnd.randrange(8, max(9, W // U - 8)) * U, H - U, rnd.randint(2, 4))
    return "".join(f'<rect x="{x}" y="{y}" width="{U}" height="{U}" fill="{COL[c]}"/>'
                   for (x, y), c in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])) if -U < x < W and -U < y < H)

def inject(path, kind="card", **kw):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'<g[^>]*id="vines">.*?</g>', '', s, flags=re.S)
    m = re.search(r'<svg[^>]*\bwidth="(\d+(?:\.\d+)?)"[^>]*\bheight="(\d+(?:\.\d+)?)"', s)
    W, H = int(float(m.group(1))), int(float(m.group(2)))
    seed = os.path.basename(path)
    if os.path.basename(path) == "features.svg":
        cells = re.findall(r'<g class="f"[^>]*><rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="#1d1e21"', s)
        parts = s.split("</g>")
        # append vines inside each feature cell group (last </g> pieces)
        out, ci = [], 0
        for p in parts[:-1]:
            if ci < len(cells) and '<g class="f"' in p:
                x, y, w, h = map(int, cells[ci]); ci += 1
                p += f'<g transform="translate({x} {y})" id="vines">' + vines(w, h, seed + str(ci)) + "</g>"
            out.append(p)
        s = "</g>".join(out + [parts[-1]])
    else:
        s = s.replace("</svg>", f'<g id="vines">{vines(W, H, seed, kind, **kw)}</g></svg>')
    open(path, "w", encoding="utf-8").write(s)
    return True


def toasts(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'<g[^>]*id="vines">.*?</g>', '', s, flags=re.S)
    add = "".join(f'<g transform="translate({6+i*298} 4)" id="vines">' + vines(288, 64, f"toast{i}", edge_only=True, right_top=False) + "</g>" for i in range(3))
    open(path, "w", encoding="utf-8").write(s.replace("</svg>", add + "</svg>"))

def apply_all(assets_dir, prefix):
    for f in sorted(os.listdir(assets_dir)):
        if not f.startswith(prefix) or not f.endswith(".svg"): continue
        n = f[len(prefix):]
        p = os.path.join(assets_dir, f)
        if n.startswith("card-") or n.startswith("pub-") or n in ("chat.svg", "contrib.svg"):
            inject(p, "card", edge_only=True, right_top=False)
        elif n == "toasts.svg": toasts(p)
        elif n.startswith("banner-"): inject(p, "banner", edge_only=True)
