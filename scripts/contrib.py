"""Fetches the contribution calendar and renders assets/mc-contrib.svg as Minecraft blocks.
Usage: GITHUB_TOKEN=... python3 scripts/contrib.py <username>   (no token: renders an empty grid)"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from pixelfont import pixels, width

USER = sys.argv[1] if len(sys.argv) > 1 else "thanmaiashok"
Q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions
weeks{contributionDays{contributionLevel date contributionCount}}}}}}"""
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
# 0 stone, 1 grass, 2 gold, 3 diamond, 4 redstone
COL = ["#3b3b3b", "#5fa03a", "#e8b923", "#4aedd9", "#e53030"]
NAME = ["NONE", "GRASS", "GOLD", "DIAMOND", "REDSTONE"]

def fetch():
    tok = os.environ.get("GITHUB_TOKEN")
    if not tok:
        return 0, [[(0, 0)] * 7 for _ in range(53)]
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": Q, "variables": {"u": USER}}).encode(),
        headers={"Authorization": f"bearer {tok}", "Content-Type": "application/json"})
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[(LEVEL[d["contributionLevel"]], d["contributionCount"]) for d in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks

def shade(c, f):
    c = c.lstrip("#"); v = [int(c[i:i+2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(min(255, int(x * f)) for x in v)

def render(total, weeks):
    S, G, X0, Y0 = 13, 3, 30, 92
    W = X0 * 2 + len(weeks) * (S + G)
    H = Y0 + 7 * (S + G) + 56
    b = f'<rect width="{W}" height="{H}" fill="#161b22"/><rect width="{W}" height="4" fill="#3a3a3a"/><rect y="{H-4}" width="{W}" height="4" fill="#3a3a3a"/>'
    b += pixels(f"{total} CONTRIBUTIONS IN THE LAST YEAR", X0, 26, 3, "#ffffff", "#3a3a3a", 2)
    for wi, w in enumerate(weeks):
        for di, (lv, n) in enumerate(w):
            x, y, c = X0 + wi * (S + G), Y0 + di * (S + G), COL[lv]
            b += (f'<g class="b" style="animation-delay:{wi*0.02:.2f}s"><rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{c}"/>'
                  f'<rect x="{x}" y="{y}" width="{S}" height="3" fill="{shade(c,1.3)}"/><rect x="{x}" y="{y+S-3}" width="{S}" height="3" fill="{shade(c,.7)}"/>'
                  f'<title>{n} contributions</title></g>')
    lx = X0
    ly = H - 34
    b += pixels("LESS", lx, ly + 2, 2, "#8b949e")
    lx += width("LESS", 2) + 14
    for i, c in enumerate(COL):
        b += f'<rect x="{lx}" y="{ly}" width="{S}" height="{S}" fill="{c}"/><rect x="{lx}" y="{ly}" width="{S}" height="3" fill="{shade(c,1.3)}"/>'
        lx += S + 6
    b += pixels("MORE", lx + 8, ly + 2, 2, "#8b949e")
    style = ".b{animation:pop .5s backwards}@keyframes pop{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">'
            f'<style>{style}</style>{b}</svg>')

if __name__ == "__main__":
    total, weeks = fetch()
    out = os.path.join(os.path.dirname(__file__), "..", "assets", "v6-contrib.svg")
    open(out, "w").write(render(total, weeks))
    print("wrote", out, total)
