"""Generates every SVG in assets/ (Minecraft theme). Run: python3 scripts/build_assets.py"""
import html, random, textwrap, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pixelfont import pixels, width

OUT = os.path.join(os.path.dirname(__file__), "..", "assets") + os.sep
os.makedirs(OUT, exist_ok=True)
MONO = "font-family=\"'DejaVu Sans Mono',Consolas,'Courier New',monospace\""
esc = html.escape

def save(name, body, w, h, style=""):
    open(OUT + "v6-" + name, "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">'
        f"<style>{style}</style>{body}</svg>")

def sprite(rows, pal, x, y, s):
    d = {}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".":
                d.setdefault(ch, []).append(f"M{x+c*s} {y+r*s}h{s}v{s}h-{s}z")
    return "".join(f'<path fill="{pal[k]}" d="{"".join(v)}"/>' for k, v in d.items())

# ---- 8x8 item sprites -------------------------------------------------
SPR = {
"compass": (["..iiii..", ".iwwwri.", "iwwwrwwi", "iwwrwwwi", "iwrwwwwi", "iwwwwwwi", ".iwwwwi.", "..iiii.."],
            dict(i="#7a7a7a", w="#d9d9d9", r="#d92b2b")),
"pickaxe": ([".cccc...", "c...hc..", "....hhc.", "...hh..c", "..hh....", ".hh.....", "hh......", "h......."],
            dict(c="#4aedd9", h="#8b5a2b")),
"sapling": ["...gg...", "..gGgg..", ".gggGg..", "..gGg...", "...g....", "...b....", "...b....", "..bbb..."],
"emerald": (["..eeee..", ".eEEEEe.", "eEwEEEEe", "eEEEEEde", "eEEEEded", ".eEEded.", "..edde..", "...ee..."],
            dict(e="#0d7a35", E="#17dd62", w="#c9ffd9", d="#0a5a28")),
"paper": (["..pppppp", ".pwwwwwp", ".pwbbwwp", ".pwwwwwp", ".pwbbbwp", ".pwwwwwp", ".pwbbwwp", "..pppppp"],
          dict(p="#c9b98a", w="#f1ead0", b="#8b8060")),
"redstone": (["........", "...rr...", "..rRRr..", ".rRRRRr.", ".rRRRRr.", "..rRRr..", "...rr...", "........"],
             dict(r="#7a0d0d", R="#e53030")),
"feather": (["......ww", ".....www", "....wwws", "...wwws.", "..wwws..", ".wwws...", "bws.....", "b......."],
            dict(w="#f5f5f5", s="#bdbdbd", b="#8b8b8b")),
"book": (["..bbbbb.", ".bppppwb", ".bpEEpwb", ".bpppwwb", ".bpEEpwb", ".bpppwwb", ".bbbbbbb", "........"],
         dict(b="#4b1f7a", p="#8a4fd6", E="#ffe066", w="#e8dcff")),
"eye": (["........", "..gggg..", ".gGGGGg.", "gGGkkGGg", "gGGkkGGg", ".gGGGGg.", "..gggg..", "........"],
        dict(g="#0f6b4a", G="#3ee0a1", k="#0a2a1f")),
"clock": (["..oooo..", ".oyyyyo.", "oyykyyyo", "oyykyyyo", "oyykkkyo", "oyyyyyyo", ".oyyyyo.", "..oooo.."],
          dict(o="#a86a00", y="#ffd23a", k="#3a2400")),
"potion": (["...gg...", "...gg...", "..gwwg..", ".gRRRRg.", "gRRRRRRg", "gRRrRRRg", ".gRRRRg.", "..gggg.."],
           dict(g="#cfd8dc", w="#eceff1", R="#d63a3a", r="#ff8a8a")),
"steve": (["hhhhhhhh", "hhhhhhhh", "sssssssh", "sbwsswbs", "sssnnsss", "ssmmmmss", "ssssssss", "..cccc.."],
          dict(h="#3b2414", s="#c68a5c", b="#3a4fd6", w="#ffffff", n="#8a5a3a", m="#5a3a24", c="#2aa5c2")),
"sword": (["......ss", ".....ss.", "....ss..", "g..ss...", ".gss....", "..gg....", ".bg.g...", "b......."],
          dict(s="#dfe4ea", g="#c9a227", b="#8b5a2b")),
"star": (["...yy...", "...yy...", "yyyyyyyy", ".yyyyyy.", "..yyyy..", ".yyyyyy.", ".yy..yy.", "yy....yy"],
         dict(y="#ffd23a")),
"sapling2": None,
}
def spr(name, x, y, s):
    v = SPR[name]
    if name == "sapling":
        return sprite(v, dict(g="#2f8f2f", G="#57c957", b="#7a4b25"), x, y, s)
    return sprite(v[0], v[1], x, y, s)

def slot(x, y, size):
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="#8b8b8b"/>'
            f'<rect x="{x}" y="{y}" width="{size}" height="3" fill="#373737"/><rect x="{x}" y="{y}" width="3" height="{size}" fill="#373737"/>'
            f'<rect x="{x}" y="{y+size-3}" width="{size}" height="3" fill="#ffffff"/><rect x="{x+size-3}" y="{y}" width="3" height="{size}" fill="#ffffff"/>')

# ---- header -----------------------------------------------------------
def header():
    rnd = random.Random(7)
    W, H, GY = 1000, 340, 268
    b = f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d8fe8"/><stop offset="1" stop-color="#b9d8ff"/></linearGradient></defs>'
    b += f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    # sun
    b += '<g class="sun"><rect x="820" y="36" width="56" height="56" fill="#fff3a0"/><rect x="828" y="44" width="40" height="40" fill="#ffe14d"/></g>'
    # clouds
    def cloud(x, y, s, cls):
        parts = [(0, 1, 5, 1), (1, 0, 3, 1), (0, 2, 5, 1)]
        return f'<g class="{cls}" transform="translate({x} {y})">' + "".join(
            f'<rect x="{px*s}" y="{py*s}" width="{pw*s}" height="{ph*s}" fill="#fff" opacity=".92"/>' for px, py, pw, ph in parts) + "</g>"
    b += cloud(60, 30, 20, "cl1") + cloud(520, 70, 16, "cl2") + cloud(300, 18, 12, "cl3")
    # far hills (stepped)
    hills = ""
    for i in range(0, W, 40):
        h = 40 + int(28 * (1 + __import__("math").sin(i / 130.0)))
        hills += f'<rect x="{i}" y="{GY-h}" width="40" height="{h}" fill="#6aa84f" opacity=".55"/>'
    b += hills
    # trees
    def tree(x, s=8):
        t = f'<rect x="{x+s*2}" y="{GY-s*5}" width="{s}" height="{s*5}" fill="#6b4423"/>'
        for (lx, ly, lw) in [(0, GY - s*8, 5), (1, GY - s*10, 3)]:
            t += f'<rect x="{x+lx*s}" y="{ly}" width="{lw*s}" height="{s*2}" fill="#2f7d32"/>'
        t += f'<rect x="{x+s}" y="{GY-s*8+s}" width="{s}" height="{s}" fill="#3f9b42"/>'
        return t
    b += tree(640) + tree(720, 10) + tree(560, 6)
    # ground
    b += f'<rect y="{GY}" width="{W}" height="{H-GY}" fill="#8a5a36"/>'
    for x in range(0, W, 16):
        for y in range(GY + 16, H, 16):
            if rnd.random() < .45:
                c = rnd.choice(["#7a4d2c", "#9a6a42", "#6b4224"])
                b += f'<rect x="{x}" y="{y}" width="16" height="16" fill="{c}"/>'
    b += f'<rect y="{GY}" width="{W}" height="16" fill="#5fa03a"/>'
    for x in range(0, W, 8):
        if rnd.random() < .5:
            b += f'<rect x="{x}" y="{GY}" width="8" height="8" fill="{rnd.choice(["#4f8a2f", "#6fb84a"])}"/>'
    b += f'<rect y="{GY+16}" width="{W}" height="8" fill="#4a7a2a"/>'
    # Steve, standing on the right
    u = 4; sx, sy = 826, GY - 32 * u
    def R(x, y, w, h, c): return f'<rect x="{sx + x*u}" y="{sy + y*u}" width="{w*u}" height="{h*u}" fill="{c}"/>'
    st = '<g class="steve">'
    hx = 4
    def HD(x, y, w, h, c): return R(hx + x, y, w, h, c)
    st += HD(0, 0, 8, 2, "#3b2a1c") + HD(0, 2, 8, 6, "#c68a5c") + HD(0, 2, 1, 2, "#3b2a1c") + HD(7, 2, 1, 2, "#3b2a1c")
    st += HD(1, 4, 2, 1, "#ffffff") + HD(5, 4, 2, 1, "#ffffff") + HD(2, 4, 1, 1, "#4a3aa8") + HD(5, 4, 1, 1, "#4a3aa8")   # eyes
    st += HD(3, 5, 2, 1, "#a9714b") + HD(2, 6, 4, 1, "#6b4229") + HD(3, 7, 2, 1, "#6b4229")                              # nose, mouth
    st += R(4, 8, 8, 12, "#2aa5b5") + R(7, 8, 2, 1, "#c68a5c")                                                         # shirt, neckline
    st += R(0, 8, 4, 4, "#2aa5b5") + R(0, 12, 4, 8, "#c68a5c")                                                         # left arm (still)
    st += '<g class="arm">' + R(12, 8, 4, 4, "#2aa5b5") + R(12, 12, 4, 8, "#c68a5c") + "</g>"                       # right arm (waves)
    st += R(4, 20, 4, 10, "#3c44aa") + R(8, 20, 4, 10, "#333a96") + R(4, 30, 4, 2, "#6b6b6b") + R(8, 30, 4, 2, "#5a5a5a")   # legs, shoes
    st += "</g>"
    b += st
    # speech bubble: "HI!" while Steve waves (every 5 seconds)
    bx, by, bw, bh = 748, 122, 66, 38
    say = '<g class="say">'
    say += f'<path fill="#1b1b1b" d="M{bx-3} {by-3}h{bw+6}v{bh+6}h-{bw+6}zM{bx+bw+3} {by+12}h9v9h-9z"/>'
    say += f'<path fill="#ffffff" d="M{bx} {by}h{bw}v{bh}h-{bw}zM{bx+bw} {by+15}h8v6h-8z"/>'
    say += pixels("HI!", bx + (bw - width("HI!", 3)) // 2, by + (bh - 21) // 2, 3, "#1b1b1b")
    b += say + "</g>"
    # title
    b += pixels("THANMAI A", 50, 58, 9, "#ffffff", "#3a3a3a", 5)
    b += pixels("AI & ML ENGINEER", 52, 148, 4, "#ffd23a", "#4a3a00", 3)
    b += pixels("FOUNDER OF FOXYNAI", 52, 190, 4, "#55ffff", "#0a3a3a", 3)
    style = """.sun{animation:bob 6s ease-in-out infinite}@keyframes bob{50%{transform:translateY(8px)}}
.cl1{animation:d1 60s linear infinite}.cl2{animation:d2 80s linear infinite}.cl3{animation:d3 100s linear infinite}
@keyframes d1{from{transform:translate(60px,30px)}to{transform:translate(1060px,30px)}}
@keyframes d2{from{transform:translate(520px,70px)}to{transform:translate(-120px,70px)}}
@keyframes d3{from{transform:translate(300px,18px)}to{transform:translate(1100px,18px)}}
.steve{animation:idle 3s ease-in-out infinite}@keyframes idle{50%{transform:translateY(-2px)}}
.arm{transform-box:view-box;transform-origin:882px 176px;animation:wave 5s ease-in-out infinite}
@keyframes wave{0%,6%{transform:rotate(0)}12%{transform:rotate(-135deg)}20%{transform:rotate(-108deg)}28%{transform:rotate(-135deg)}36%{transform:rotate(-108deg)}44%{transform:rotate(-135deg)}52%{transform:rotate(-108deg)}60%{transform:rotate(-135deg)}68%,100%{transform:rotate(0)}}
.say{opacity:0;transform-box:fill-box;transform-origin:100% 100%;animation:say 5s linear infinite}
@keyframes say{0%,8%{opacity:0;transform:scale(.6)}12%{opacity:1;transform:scale(1.1)}14%,64%{opacity:1;transform:scale(1)}68%,100%{opacity:0;transform:scale(.8)}}
@media (prefers-reduced-motion:reduce){.arm{animation:none}.say{animation:none;opacity:0}}
"""
    save("header4.svg", b, W, H, style)

# ---- section banner (wood sign) --------------------------------------
def banner(name, text, icon):
    W, H = 900, 64
    b = f'<rect width="{W}" height="{H}" fill="#9c7038"/>'
    for i in range(0, W, 30):
        b += f'<rect x="{i}" y="0" width="2" height="{H}" fill="#87602d" opacity=".6"/>'
    for y in (20, 42):
        b += f'<rect x="0" y="{y}" width="{W}" height="2" fill="#87602d" opacity=".5"/>'
    b += f'<rect width="{W}" height="4" fill="#c2965a"/><rect y="{H-4}" width="{W}" height="4" fill="#5c3d1a"/>'
    b += f'<rect width="4" height="{H}" fill="#5c3d1a"/><rect x="{W-4}" width="4" height="{H}" fill="#5c3d1a"/>'
    b += spr(icon, 22, 12, 5) + spr(icon, W - 22 - 40, 12, 5)
    tw = width(text, 4)
    b += pixels(text, (W - tw) // 2, 18, 4, "#ffffff", "#3a2a10", 3)
    save(name, b, W, H)

# ---- buttons ----------------------------------------------------------
def button(name, text):
    tw = width(text, 2)
    W, H = tw + 56, 40
    b = f'<rect width="{W}" height="{H}" fill="#000"/><rect x="2" y="2" width="{W-4}" height="{H-4}" fill="#6f6f6f"/>'
    b += f'<rect x="2" y="2" width="{W-4}" height="3" fill="#a8a8a8"/><rect x="2" y="2" width="3" height="{H-4}" fill="#a8a8a8"/>'
    b += f'<rect x="2" y="{H-7}" width="{W-4}" height="5" fill="#3d3d3d"/><rect x="{W-5}" y="2" width="3" height="{H-4}" fill="#4a4a4a"/>'
    b += pixels(text, (W - tw) // 2, 13, 2, "#ffffff", "#3a3a3a", 2)
    save(name, b, W, H)

# ---- chat window -----------------------------------------------------
def chat():
    """Scrolling server chat: one message per project, loops forever like a live game chat."""
    proj = [("Multimodal Graph RAG", "knowledge graph + vector search + LLM retrieval", "#55ffff"),
            ("Universal Optimizer", "quantize, prune, distill any model, laptop to edge", "#ffff55"),
            ("AR Plant Health Checker", "browser AR disease detection, 97.3% accuracy", "#55ff55"),
            ("Stock Bot", "AI paper trading on 18k+ US and India stocks, fully local", "#55ff55"),
            ("News Intelligence", "distributed crawler, NLP pipeline, AI dashboard", "#ffffff"),
            ("ReelForge", "autonomous agent that edits 9:16 shorts end to end, locally", "#ff5555"),
            ("NeuroReflex-X", "drone pursuit inspired by hawk, locust and dragonfly", "#ff55ff"),
            ("Vinci AI", "da Vinci reasoning assistant, local LLM + FAISS search", "#ff55ff"),
            ("Social Profile Intelligence", "OSINT across 40+ platforms, local LLM profiling", "#55ffff"),
            ("Micro Wind Analyzer", "turbine placement optimizer with 3D simulation", "#ffaa00"),
            ("Wine Quality ML Pipeline", "94% accuracy, ROC-AUC 0.955, CI-style quality gate", "#ff5555")]
    # each message is a list of (text, color) segments
    T = "#ffffff"
    msgs = [[("[Server] Thanmai A joined the game", "#ffff55")],
            [("<Thanmai> ", T), ("AI and ML engineer. Founder of FoxynAI.", T)],
            [("<Thanmai> ", T), ("here is everything I have built:", T)]]
    for i, (n, d, c) in enumerate(proj):
        msgs.append([("<Thanmai> ", T), (f"[{i+1}/11] ", "#aaaaaa"), (n + ": ", c), (d, T)])
    msgs += [[("<Thanmai> ", T), ("published: ", "#aaaaaa"), ("breast cancer prediction with XAI + ResNet101 (IEEE 2025)", "#55ffff")],
             [("<Thanmai> ", T), ("published: ", "#aaaaaa"), ("liver cirrhosis staging with tuned ML models (2025)", "#55ffff")],
             [("[Server] Thanmai A has made the advancement [Founder]", "#55ff55")]]
    N, V, STEP, HOLD, RH = len(msgs), 9, 2.0, 6.0, 30
    CYC = 0.6 + N * STEP + HOLD
    W, H = 900, 34 + V * RH
    pc = lambda t: t / CYC * 100
    b = f'<defs><clipPath id="vp"><rect x="0" y="16" width="{W}" height="{V*RH+8}"/></clipPath></defs>'
    b += f'<rect width="{W}" height="{H}" fill="#1b1b1b"/><rect width="{W}" height="{H}" fill="#000" opacity=".25"/>'
    b += f'<rect width="{W}" height="4" fill="#3a3a3a"/><rect y="{H-4}" width="{W}" height="4" fill="#3a3a3a"/>'
    style = ""
    b += '<g clip-path="url(#vp)"><g class="all">'
    shifts = []
    for i, segs in enumerate(msgs):
        t0 = 0.6 + i * STEP
        s0, s1 = pc(t0), pc(t0) + 0.9
        style += (f"@keyframes m{i}{{0%,{s0:.2f}%{{opacity:0;transform:translateX(-10px)}}{s1:.2f}%,94%{{opacity:1;transform:none}}98%,100%{{opacity:0;transform:none}}}}"
                  f".m{i}{{animation:m{i} {CYC:.1f}s linear infinite}}")
        y = 20 + i * RH
        tsp = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in segs)
        b += (f'<g class="m{i}" opacity="0"><rect x="14" y="{y}" width="{W-28}" height="26" fill="#000" opacity=".35"/>'
              f'<text x="24" y="{y+19}" font-size="14" xml:space="preserve" {MONO}>{tsp}</text></g>')
        if i >= V:
            shifts.append((pc(t0), -(i - V + 1) * RH))
    b += "</g></g>"
    kf = "0%{transform:translateY(0)}"
    prev = 0
    for pct, ty in shifts:
        kf += f"{pct:.2f}%{{transform:translateY({prev}px)}}{pct+0.9:.2f}%{{transform:translateY({ty}px)}}"
        prev = ty
    kf += f"98%{{transform:translateY({prev}px)}}99%,100%{{transform:translateY(0)}}"
    style += f"@keyframes sc{{{kf}}}.all{{animation:sc {CYC:.1f}s linear infinite}}"
    save("chat.svg", b, W, H, style)

# ---- inventory tooltip cards -----------------------------------------
P = [
 ("multimodal-graph-rag--datamesh", "Multimodal Graph RAG", "Knowledge graphs, vector search and LLM retrieval over multi-modal embeddings.", "FastAPI · React · Docker", "JavaScript", "compass", "#55ffff"),
 ("universal-optimizer", "Universal Optimizer", "Quantize, prune, distill and deploy any LLM, Transformer or CNN to laptop, cloud, mobile or edge.", "Quantize · Prune · Distill", "Python", "pickaxe", "#ffff55"),
 ("AR-Plant-Health-Checker", "AR Plant Health Checker", "Real-time plant disease detection from a browser camera with a 3D AR overlay.", "97.3% accuracy (DenseNet121)", "JavaScript", "sapling", "#55ff55"),
 ("stock-bot", "Stock Bot", "AI paper trading bot: GNN, XGBoost and FinBERT. Zero paid APIs, fully local.", "18k+ stocks (US + India)", "Python", "emerald", "#55ff55"),
 ("news-intelligence", "News Intelligence", "Self-hosted news platform with a distributed crawler, NLP pipeline and AI dashboard.", "Crawler · NLP · Dashboard", "Python", "paper", "#ffffff"),
 ("reelforge", "ReelForge", "Autonomous shorts-editing agent. Plans, fetches, captions, scores music and renders 9:16 locally.", "9:16 shorts, no external LLM", "Python", "redstone", "#ff5555"),
 ("NeuroReflex-X", "NeuroReflex-X", "Bio-inspired reflex-cognitive drone pursuit framework with kinematic prediction.", "Hawk · Locust · Dragonfly", "JavaScript", "feather", "#ff55ff"),
 ("vinci-ai", "Vinci AI", "Leonardo da Vinci reasoning assistant. Local LLM with FAISS vector search.", "Local LLM + FAISS", "Python", "book", "#ff55ff"),
 ("social-profile-intelligence", "Social Profile Intelligence", "OSINT tool that searches 40+ platforms, generates username variants and profiles with a local LLM.", "40+ platforms", "JavaScript", "eye", "#55ffff"),
 ("micro-wind-analyzer", "Micro Wind Analyzer", "Micro-scale wind analysis and turbine placement optimizer with physics simulation.", "Real-time 3D visualization", "JavaScript", "clock", "#ffaa00"),
 ("wine-quality-mlpipeline-DML", "Wine Quality ML Pipeline", "Jenkins-style ML pipeline on UCI Wine Quality. Auto-fails below 75% accuracy.", "94% acc · ROC-AUC 0.955", "Python", "potion", "#ff5555"),
]
LC = {"Python": "#3572A5", "JavaScript": "#f1e05a"}
def card(i, repo, title, desc, stat, lang, icon, col):
    W, H = 440, 172
    lines = textwrap.wrap(desc, 40)[:3]
    b = f'<rect width="{W}" height="{H}" fill="#100010"/>'
    b += f'<rect class="bd" x="4" y="4" width="{W-8}" height="{H-8}" fill="none" stroke="#3b0f80" stroke-width="4"/>'
    b += f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#100010" stroke-width="4"/>'
    b += slot(20, 22, 68) + spr(icon, 28, 30, 6)
    b += f'<text x="104" y="40" font-size="16" font-weight="bold" fill="{col}" {MONO}>{esc(title)}</text>'
    for j, l in enumerate(lines):
        b += f'<text x="104" y="{64+j*17}" font-size="12" fill="#aaaaaa" {MONO}>{esc(l)}</text>'
    b += f'<text x="104" y="{64+len(lines)*17+8}" font-size="12" fill="#5555ff" {MONO}>+ {esc(stat)}</text>'
    b += f'<rect x="20" y="{H-32}" width="10" height="10" fill="{LC[lang]}"/><text x="38" y="{H-23}" font-size="11" fill="#dddddd" {MONO}>{lang}</text>'
    b += f'<text x="{W-20}" y="{H-23}" font-size="10" fill="#777777" text-anchor="end" {MONO}>thanmaiashok/{esc(repo)}</text>'
    style = f".bd{{animation:g 3s ease-in-out {i*0.25}s infinite}}@keyframes g{{50%{{stroke:#7a3fd1}}}}"
    save(f"card-{repo}.svg", b, W, H, style)

# ---- enchanted-book paper cards -------------------------------------
PUBS = [
 ("Enhancing Breast Cancer Prediction in HER Health with XAI Technology and ResNet101", "SR Sreeram, N Subash, N Nithya, M Patil, A Thanmai", "2025 IEEE 17th International Conference on Computational Intelligence and ..."),
 ("Performance Analysis of Machine Learning Models for Liver Cirrhosis Staging with Hyperparameter Tuning", "GG Saralaya, N Subash, SV Raja, A Thanmai", "2025 5th International Conference on Emerging Research in Electronics ..."),
]
def pubs():
    for i, (t, a, v) in enumerate(PUBS):
        tl = textwrap.wrap(t, 62)
        H = 92 + len(tl) * 24 + 50
        W = 900
        b = f'<rect width="{W}" height="{H}" fill="#100010"/>'
        b += f'<rect class="bd" x="4" y="4" width="{W-8}" height="{H-8}" fill="none" stroke="#3b0f80" stroke-width="4"/>'
        b += slot(24, 24, 72) + spr("book", 33, 33, 6)
        b += f'<rect class="glint" x="24" y="24" width="14" height="72" fill="#c9a0ff" opacity="0"/>'
        for j, l in enumerate(tl):
            b += f'<text x="116" y="{46+j*24}" font-size="19" font-weight="bold" fill="#55ffff" {MONO}>{esc(l)}</text>'
        y = 46 + len(tl) * 24 + 4
        b += f'<text x="116" y="{y}" font-size="13" fill="#aaaaaa" {MONO}>{esc(a)}</text>'
        b += f'<text x="116" y="{y+22}" font-size="13" fill="#aaaaaa" font-style="italic" {MONO}>{esc(v)}</text>'
        b += f'<text x="116" y="{y+48}" font-size="13" fill="#ffaa00" {MONO}>Published: 2025</text>'
        b += f'<text x="{W-24}" y="{y+48}" font-size="13" fill="#ff55ff" text-anchor="end" {MONO}>Enchanted: Peer Reviewed</text>'
        style = ".bd{animation:g 3s ease-in-out infinite}@keyframes g{50%{stroke:#7a3fd1}}.glint{animation:gl 3s ease-in-out infinite}@keyframes gl{0%{transform:translateX(-20px);opacity:0}40%{opacity:.5}80%,100%{transform:translateX(70px);opacity:0}}"
        save(f"pub-{i+1}.svg", b, W, H, style)

# ---- tech stack: two marquee rows (opposite directions) of real logos ----
def stack():
    import json
    icons = json.load(open(os.path.join(os.path.dirname(__file__), "icons.json")))
    half = (len(icons) + 1) // 2
    rows = [icons[:half], icons[half:]]
    TW, TH, GAP = 100, 100, 12
    PITCH = TW + GAP
    W, H = 900, 16 + 2 * TH + GAP + 16
    def tile(ic, x, y):
        hx = ic["hex"]
        lum = 0.3 * int(hx[0:2], 16) + 0.59 * int(hx[2:4], 16) + 0.11 * int(hx[4:6], 16)
        col = "#e8e8e8" if lum < 45 else "#" + hx
        g = slot(x, y, TW).replace('fill="#8b8b8b"', 'fill="#2a2b2e"').replace('fill="#373737"', 'fill="#0e0e10"').replace('fill="#ffffff"', 'fill="#5a5b60"')
        g += f'<g transform="translate({x + TW/2 - 24:.1f} {y + 12}) scale(2)"><path fill="{col}" d="{ic["d"]}"/></g>'
        g += f'<text x="{x + TW/2}" y="{y + TH - 14}" font-size="12" text-anchor="middle" fill="#cfcfcf" {MONO}>{esc(ic["name"])}</text>'
        return g
    b = ('<defs><linearGradient id="fade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#000"/><stop offset=".07" stop-color="#fff"/>'
         '<stop offset=".93" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
         f'<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask></defs>')
    b += f'<rect width="{W}" height="{H}" fill="#151618"/><rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="#3a3b3f" stroke-width="2"/>'
    b += '<g mask="url(#m)">'
    style = ""
    for r, row in enumerate(rows):
        y = 16 + r * (TH + GAP)
        span = len(row) * PITCH
        g = "".join(tile(ic, i * PITCH, y) for i, ic in enumerate(row)) + "".join(tile(ic, span + i * PITCH, y) for i, ic in enumerate(row))
        # enough copies to cover the view while the row slides
        g += "".join(tile(ic, 2 * span + i * PITCH, y) for i, ic in enumerate(row))
        b += f'<g class="r{r}">{g}</g>'
        a, z = (0, -span) if r == 0 else (-span, 0)
        dur = 48 if r == 0 else 56
        style += f"@keyframes m{r}{{from{{transform:translateX({a}px)}}to{{transform:translateX({z}px)}}}}.r{r}{{animation:m{r} {dur}s linear infinite}}"
    b += "</g>"
    style += "@media (prefers-reduced-motion:reduce){.r0,.r1{animation:none}}"
    save("stack-marquee.svg", b, W, H, style)

# ---- advancement toasts ----------------------------------------------
def toasts():
    items = [("star", "Published Author", "2 IEEE papers in 2025"), ("sword", "Shipper", "11 projects built and released"), ("steve", "Founder", "Founder of FoxynAI")]
    W, H = 900, 72
    b = ""
    for i, (ic, t, d) in enumerate(items):
        x = 6 + i * 298
        b += f'<g class="t" style="animation-delay:{i*0.4}s"><rect x="{x}" y="4" width="288" height="64" fill="#212121"/>'
        b += f'<rect x="{x}" y="4" width="288" height="4" fill="#6a6a6a"/><rect x="{x}" y="64" width="288" height="4" fill="#0e0e0e"/>'
        b += f'<rect x="{x}" y="4" width="4" height="64" fill="#6a6a6a"/><rect x="{x+284}" y="4" width="4" height="64" fill="#0e0e0e"/>'
        b += slot(x + 12, 16, 40) + spr(ic, x + 16, 20, 4)
        b += f'<text x="{x+64}" y="30" font-size="13" font-weight="bold" fill="#ffff55" {MONO}>Advancement Made!</text>'
        b += f'<text x="{x+64}" y="46" font-size="12" fill="#ffffff" {MONO}>{esc(t)}</text>'
        b += f'<text x="{x+64}" y="60" font-size="10" fill="#aaaaaa" {MONO}>{esc(d)}</text></g>'
    style = ".t{animation:sl .6s backwards}@keyframes sl{from{opacity:0;transform:translateX(60px)}to{opacity:1;transform:none}}"
    save("toasts.svg", b, W, H, style)

# ---- footer -----------------------------------------------------------
def footer():
    rnd = random.Random(3)
    W, H = 900, 64
    b = f'<rect width="{W}" height="{H}" fill="#8a5a36"/>'
    for x in range(0, W, 16):
        for y in range(16, H, 16):
            if rnd.random() < .5:
                b += f'<rect x="{x}" y="{y}" width="16" height="16" fill="{rnd.choice(["#7a4d2c", "#9a6a42", "#6b4224"])}"/>'
    b += f'<rect width="{W}" height="16" fill="#5fa03a"/>'
    for x in range(0, W, 8):
        if rnd.random() < .5:
            b += f'<rect x="{x}" width="8" height="8" fill="{rnd.choice(["#4f8a2f", "#6fb84a"])}"/>'
    b += pixels("THANKS FOR VISITING", (W - width("THANKS FOR VISITING", 3)) // 2, 30, 3, "#ffffff", "#3a2a10", 2)
    save("footer.svg", b, W, H)

if __name__ == "__main__":
    header(); chat(); stack(); toasts(); footer(); pubs()
    for n, t, i in [("banner-projects.svg", "INVENTORY: PROJECTS", "pickaxe"), ("banner-papers.svg", "ENCHANTED BOOKS: PAPERS", "book"),
                    ("banner-tech.svg", "TECH STACK", "sword"), ("banner-activity.svg", "ACTIVITY: CONTRIBUTIONS", "emerald"),
                    ("banner-about.svg", "SERVER CHAT", "paper"), ("banner-adv.svg", "ADVANCEMENTS", "star")]:
        banner(n, t, i)
    for n, t in [("btn-foxynai.svg", "FOXYNAI"), ("btn-linkedin.svg", "LINKEDIN"), ("btn-email.svg", "EMAIL"), ("btn-instagram.svg", "INSTAGRAM")]:
        button(n, t)
    for i, p in enumerate(P):
        card(i, *p)
    import vines
    vines.apply_all(OUT, "v6-")
