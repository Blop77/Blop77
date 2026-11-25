#!/usr/bin/env python3
"""Generates the animated SVGs used by README.md.

GitHub renders SVG images with their CSS animations but strips scripts, so
every effect here is pure CSS keyframes. Edit the data below and run:

    python3 tools/build_assets.py
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# Design tokens (dark, cinematic)
BG = "#07090d"
PANEL = "#0d1117"
LINE = "#1f2633"
TEXT = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#2997ff"
GREEN = "#30d158"
RED = "#ff453a"
PURPLE = "#bf5af2"
ORANGE = "#ff9f0a"
CYAN = "#64d2ff"
PINK = "#ff375f"

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Ubuntu, 'DejaVu Sans', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', 'DejaVu Sans Mono', Menlo, monospace"

REDUCED = """
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"""


def write(name, svg):
    (OUT / name).write_text(svg.strip() + "\n", encoding="utf-8")
    print("wrote", name)


# ---------------------------------------------------------------- hero banner
def banner():
    import random
    rnd = random.Random(77)
    W, H = 1200, 380

    # Star / dust field
    stars = []
    for i in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([0.6, 0.8, 1.0, 1.3])
        d = rnd.uniform(0, 4)
        stars.append(f'<circle class="tw" cx="{x:.0f}" cy="{y:.0f}" r="{r}" style="animation-delay:{d:.2f}s"/>')

    # Neural network on the right
    layers = [3, 5, 5, 2]
    xs = [770, 890, 1010, 1120]
    nodes = []
    for li, n in enumerate(layers):
        gap = 230 / (n - 1) if n > 1 else 0
        top = 190 - 115 if n > 1 else 190
        nodes.append([(xs[li], top + i * gap) for i in range(n)])
    edges, pulses = [], []
    k = 0
    for li in range(len(layers) - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                path = f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}"
                edges.append(f'<path d="{path}" class="edge"/>')
                if rnd.random() < 0.42:
                    col = rnd.choice([BLUE, CYAN, PURPLE, GREEN])
                    delay = rnd.uniform(0, 3.2) + li * 0.5
                    pulses.append(
                        f'<path d="{path}" class="pulse" pathLength="100" '
                        f'style="stroke:{col};animation-delay:{delay:.2f}s"/>')
                k += 1
    circles = []
    for li, layer in enumerate(nodes):
        for i, (x, y) in enumerate(layer):
            d = li * 0.45 + i * 0.18
            circles.append(
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="13" class="halo" style="animation-delay:{d:.2f}s"/>'
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" class="node" style="animation-delay:{d:.2f}s"/>')

    chips = [
        ("AI agents", BLUE), ("Computer vision", PURPLE),
        ("Hackathons", GREEN), ("C at heart", ORANGE),
    ]
    chip_svg, cx = [], 64
    for i, (label, col) in enumerate(chips):
        w = 30 + len(label) * 10
        chip_svg.append(
            f'<g class="reveal" style="animation-delay:{1.5 + i * 0.12:.2f}s">'
            f'<rect x="{cx:.0f}" y="282" width="{w:.0f}" height="38" rx="19" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".55"/>'
            f'<text x="{cx + w / 2:.0f}" y="307" text-anchor="middle" class="chip" fill="{col}">{label}</text></g>')
        cx += w + 12

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Blop77: building AI that helps real people">
<title>Blop77: building AI that helps real people</title>
<defs>
  <radialGradient id="glowA" cx="78%" cy="45%" r="45%">
    <stop offset="0" stop-color="{BLUE}" stop-opacity=".28"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="12%" cy="100%" r="55%">
    <stop offset="0" stop-color="{PURPLE}" stop-opacity=".22"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="title" x1="0" x2="1" spreadMethod="reflect">
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1 0;0 0" dur="9s" repeatCount="indefinite"/>
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".35" stop-color="{BLUE}"/>
    <stop offset=".7" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".035"/>
  </pattern>
</defs>
<style>
  .title {{ font: 800 112px {SANS}; letter-spacing: -3px; }}
  .kicker {{ font: 600 19px {MONO}; fill: {GREEN}; letter-spacing: .5px; }}
  .sub {{ font: 500 27px {SANS}; fill: {TEXT}; }}
  .muted {{ fill: {MUTED}; }}
  .chip {{ font: 600 17px {SANS}; }}
  .tw {{ fill: #fff; opacity: .15; animation: tw 4s ease-in-out infinite; }}
  @keyframes tw {{ 50% {{ opacity: .8; }} }}
  .edge {{ stroke: #ffffff; stroke-opacity: .07; stroke-width: 1.2; }}
  .pulse {{ fill: none; stroke-width: 2.4; stroke-linecap: round; stroke-dasharray: 12 100;
           stroke-dashoffset: 112; opacity: 0; animation: pulse 3.6s cubic-bezier(.6,0,.4,1) infinite; }}
  @keyframes pulse {{ 0% {{ stroke-dashoffset: 112; opacity: 0; }} 10% {{ opacity: 1; }}
                     80% {{ opacity: 1; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  .node {{ fill: {PANEL}; stroke: {BLUE}; stroke-width: 2.5; animation: node 3s ease-in-out infinite; }}
  @keyframes node {{ 50% {{ stroke: {CYAN}; fill: #10233d; }} }}
  .halo {{ fill: {BLUE}; opacity: 0; transform-box: fill-box; transform-origin: center; animation: halo 3s ease-out infinite; }}
  @keyframes halo {{ 0% {{ opacity: .45; transform: scale(.5); }} 70%,100% {{ opacity: 0; transform: scale(2); }} }}
  .reveal {{ animation: fadeUp .9s cubic-bezier(.2,.8,.2,1) backwards; }}
  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(18px); }} }}
  .wipe {{ animation: wipe 1.3s cubic-bezier(.7,0,.2,1) .25s backwards; }}
  @keyframes wipe {{ from {{ clip-path: inset(0 100% 0 0); }} to {{ clip-path: inset(0 0 0 0); }} }}
  .caret {{ fill: {GREEN}; animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .scan {{ fill: url(#shine); opacity: .05; animation: scan 7s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY({H}px); }} }}
  .spin {{ transform-origin: 945px 190px; animation: spin 40s linear infinite; }}
  .spin2 {{ transform-origin: 945px 190px; animation: spin 26s linear infinite reverse; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  {REDUCED}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glowA)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#glowB)"/>
<g>{''.join(stars)}</g>

<g class="spin"><circle cx="945" cy="190" r="168" fill="none" stroke="{BLUE}" stroke-opacity=".14" stroke-dasharray="2 10"/></g>
<g class="spin2"><circle cx="945" cy="190" r="140" fill="none" stroke="{PURPLE}" stroke-opacity=".16" stroke-dasharray="40 18 4 18"/>
  <circle cx="1085" cy="190" r="4" fill="{PURPLE}"/></g>

<g>{''.join(edges)}</g>
<g>{''.join(pulses)}</g>
<g>{''.join(circles)}</g>

<g class="reveal" style="animation-delay:.05s"><text x="64" y="96" class="kicker">~/blop77 $ ./build --for-real-people<tspan class="caret">▌</tspan></text></g>
<g class="wipe"><text x="60" y="200" class="title" fill="url(#title)">Blop77</text></g>
<g class="reveal" style="animation-delay:1.1s">
  <text x="64" y="252" class="sub">I build <tspan fill="{CYAN}" font-weight="700">AI-powered apps</tspan> that help real people<tspan class="muted"> · MIT-WPU</tspan></text>
</g>
{''.join(chip_svg)}
<rect class="scan" x="0" y="0" width="{W}" height="40"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>
</svg>"""
    write("banner.svg", svg)


# ------------------------------------------------------------ section headers
def header(name, label, index, color):
    W, H = 1200, 96
    width = 40 + len(label) * 19
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">
<title>{escape(label)}</title>
<defs>
  <linearGradient id="g" x1="0" x2="1">
    <stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
  .idx {{ font: 700 15px {MONO}; fill: {color}; letter-spacing: 3px; }}
  .lbl {{ font: 800 34px {SANS}; fill: {TEXT}; letter-spacing: -.5px; }}
  .bar {{ transform-box: fill-box; transform-origin: left;
         animation: grow 1.4s cubic-bezier(.7,0,.2,1) .2s backwards; }}
  @keyframes grow {{ from {{ transform: scaleX(0); }} }}
  .dot {{ fill: {color}; animation: run 3.2s cubic-bezier(.6,0,.4,1) 1.6s infinite; opacity: 0; }}
  @keyframes run {{ 0% {{ transform: translateX(0); opacity: 0; }} 10% {{ opacity: 1; }}
                   90% {{ opacity: 1; }} 100% {{ transform: translateX({W - width - 90}px); opacity: 0; }} }}
  .in {{ animation: in .8s cubic-bezier(.2,.8,.2,1) backwards; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-14px); }} }}
  {REDUCED}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{LINE}"/>
<rect x="0" y="18" width="5" height="60" rx="2.5" fill="{color}"/>
<g class="in"><text x="30" y="34" class="idx">{index:02d} /</text>
<text x="30" y="74" class="lbl">{escape(label)}</text></g>
<rect class="bar" x="{width + 16}" y="63" width="{W - width - 46}" height="2" fill="url(#g)"/>
<circle class="dot" cx="{width + 18}" cy="64" r="4"/>
</svg>"""
    write(name, svg)


# --------------------------------------------------------------- featured card
def featured():
    W, H = 1200, 330
    arms = []
    for i in range(4):
        arms.append(
            f'<path d="M0,-30 C30,-34 62,-60 60,-98 C58,-118 44,-130 24,-136" '
            f'transform="rotate({i * 90})" fill="none" stroke="{CYAN}" stroke-opacity=".75" stroke-width="5" stroke-linecap="round"/>')
    chips = [("40-storm ensemble", BLUE), ("Gemini satellite vision", PURPLE),
             ("Odia · Telugu · Bengali alerts", GREEN)]
    chip_svg, y = [], 0
    cx = 390
    for i, (label, col) in enumerate(chips):
        w = 28 + len(label) * 9.4
        chip_svg.append(
            f'<g class="reveal" style="animation-delay:{.9 + i * .15:.2f}s">'
            f'<rect x="{cx:.0f}" y="240" width="{w:.0f}" height="38" rx="19" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>'
            f'<text x="{cx + w / 2:.0f}" y="265" text-anchor="middle" class="chip" fill="{col}">{label}</text></g>')
        cx += w + 12
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Featured project: CycloneSentinel">
<title>Featured project: CycloneSentinel</title>
<defs>
  <radialGradient id="eye"><stop offset="0" stop-color="{CYAN}" stop-opacity=".9"/><stop offset=".25" stop-color="{BLUE}" stop-opacity=".35"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
  <linearGradient id="arm" x1="0" y1="0" x2="0" y2="-1" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity=".45"/></linearGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>
  <clipPath id="radar"><circle cx="175" cy="165" r="135"/></clipPath>
</defs>
<style>
  .tag {{ font: 700 15px {MONO}; fill: {ORANGE}; letter-spacing: 2.5px; }}
  .h {{ font: 800 54px {SANS}; fill: {TEXT}; letter-spacing: -1.2px; }}
  .p {{ font: 400 22px {SANS}; fill: #c9d1d9; }}
  .chip {{ font: 600 16px {SANS}; }}
  .storm {{ transform-origin: 175px 165px; animation: spin 7s linear infinite; }}
  .storm2 {{ transform-origin: 175px 165px; animation: spin 12s linear infinite; opacity: .5; }}
  .sweep {{ transform-origin: 175px 165px; animation: spin 4s linear infinite; }}
  @keyframes spin {{ to {{ transform: rotate(-360deg); }} }}
  .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 2.4s ease-out infinite; }}
  @keyframes ping {{ 0% {{ transform: scale(.4); opacity: .9; }} 100% {{ transform: scale(3); opacity: 0; }} }}
  .reveal {{ animation: up .8s cubic-bezier(.2,.8,.2,1) backwards; }}
  @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} }}
  .border {{ stroke-dasharray: 600 2400; animation: trace 6s linear infinite; }}
  @keyframes trace {{ to {{ stroke-dashoffset: -3000; }} }}
  {REDUCED}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{PANEL}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>
<rect class="border" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="url(#edge)" stroke-width="2" pathLength="3000"/>

<circle cx="175" cy="165" r="135" fill="#05080c" stroke="{GREEN}" stroke-opacity=".25"/>
<g stroke="{GREEN}" stroke-opacity=".12" fill="none">
  <circle cx="175" cy="165" r="90"/><circle cx="175" cy="165" r="45"/>
  <path d="M40 165H310M175 30V300"/></g>
<g clip-path="url(#radar)">
  <g class="sweep"><path d="M175 165 L310 165 A135 135 0 0 0 270 70 Z" fill="url(#sweep)"/></g>
  <g class="storm2"><g transform="translate(175 165) scale(1.25)">{''.join(arms)}</g></g>
  <g class="storm"><g transform="translate(175 165)">{''.join(arms)}</g></g>
  <circle cx="175" cy="165" r="38" fill="url(#eye)"/>
</g>
<g fill="{RED}"><circle cx="248" cy="118" r="4"/><circle class="ping" cx="248" cy="118" r="4"/>
  <circle cx="120" cy="222" r="4"/><circle class="ping" cx="120" cy="222" r="4" style="animation-delay:.8s"/>
  <circle cx="232" cy="236" r="4"/><circle class="ping" cx="232" cy="236" r="4" style="animation-delay:1.6s"/></g>

<g class="reveal" style="animation-delay:.1s"><text x="390" y="70" class="tag">FEATURED · BUILD WITH AI: CODE FOR COMMUNITIES</text></g>
<g class="reveal" style="animation-delay:.3s"><text x="388" y="128" class="h">CycloneSentinel</text></g>
<g class="reveal" style="animation-delay:.55s">
  <text x="390" y="172" class="p">Predicts which hospitals, substations and roads</text>
  <text x="390" y="204" class="p">a cyclone will break, <tspan fill="{CYAN}" font-weight="700">24 hours before landfall</tspan>.</text>
</g>
{''.join(chip_svg)}
</svg>"""
    write("featured-cyclone.svg", svg)


# ------------------------------------------------------------- project cards
ICONS = {
    # simple 48x48 line icons, drawn centred on (0,0)
    "shield": '<path d="M0,-22 L18,-14 V0 C18,12 9,19 0,23 C-9,19 -18,12 -18,0 V-14 Z"/><path d="M-8,0 L-2,6 L9,-6"/>',
    "bug": '<ellipse cx="0" cy="4" rx="11" ry="15"/><circle cx="0" cy="-14" r="6"/><path d="M-11,0H-21M11,0H21M-10,-8L-18,-15M10,-8L18,-15M-10,12L-18,19M10,12L18,19M0,-8V19"/>',
    "card": '<rect x="-22" y="-15" width="44" height="30" rx="5"/><path d="M-22,-5H22M-14,8H-4"/>',
    "wheel": '<circle cx="-11" cy="8" r="11"/><circle cx="13" cy="8" r="11"/><path d="M-11,8 L-2,-10 H9 L13,8 M-2,-10 L3,8 H-11 M5,-15 H11"/>',
    "rotor": '<circle r="20"/><circle r="11"/><path d="M0,-20V-11M0,11V20M-20,0H-11M11,0H20M-14,-14L-8,-8M8,8L14,14M14,-14L8,-8M-8,8L-14,14"/>',
    "infinity": '<path d="M0,0 C-6,-10 -20,-10 -20,0 C-20,10 -6,10 0,0 C6,-10 20,-10 20,0 C20,10 6,10 0,0 Z"/>',
    "sparkle": '<path d="M0,-22 C2,-6 6,-2 22,0 C6,2 2,6 0,22 C-2,6 -6,2 -22,0 C-6,-2 -2,-6 0,-22 Z"/><path d="M15,-18 V-10 M11,-14 H19"/>',
}

PROJECTS = [
    ("scamkavach", "ScamKavach", "shield", GREEN, "CODE FOR A BILLION",
     ["Checks a suspicious UPI, SMS or WhatsApp", "message and explains why it looks like a scam."]),
    ("segsense", "SegSense", "bug", RED, "NVIDIA × NEBIUS",
     ["Agentic debugger for C memory bugs:", "ASan catches it, Nemotron patches it."]),
    ("allowance", "Allowance", "card", BLUE, "PAYPAL AI HACKATHON",
     ["An AI buying agent for every teammate that", "never breaks the budget or approval rules."]),
    ("ridetaste", "RideTaste", "wheel", ORANGE, "QLOO AGENTIC HACKATHON",
     ["Plans bike rides around the films, music", "and food you love, with Qloo's Taste AI."]),
    ("enigma", "Enigma", "rotor", "#e3b341", "SIMULATOR",
     ["A historically accurate WWII Enigma machine", "that looks, clicks and lights up like the real one."]),
    ("limitless", "Limitless", "infinity", PURPLE, "COMPUTER VISION",
     ["Cast Gojo Satoru's techniques with your", "bare hands, tracked live with MediaPipe."]),
    ("mystic-hands", "Mystic Hands", "sparkle", PINK, "COMPUTER VISION",
     ["Shields, portals, energy whips and a time", "loop on your webcam, all from hand gestures."]),
]


def card(slug, title, icon, color, tag, lines, delay):
    W, H = 600, 210
    body = "".join(
        f'<text x="32" y="{142 + i * 28}" class="p">{escape(l)}</text>' for i, l in enumerate(lines))
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
  <radialGradient id="glow" cx="88%" cy="10%" r="70%"><stop offset="0" stop-color="{color}" stop-opacity=".22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset=".5" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>
</defs>
<style>
  .tag {{ font: 700 14px {MONO}; fill: {color}; letter-spacing: 2px; }}
  .h {{ font: 800 38px {SANS}; fill: {TEXT}; letter-spacing: -.8px; }}
  .p {{ font: 400 19px {SANS}; fill: #b1bac4; }}
  .icon {{ fill: none; stroke: {color}; stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round;
          stroke-dasharray: 220; animation: draw 1.6s ease-out {delay + .2:.2f}s backwards; }}
  @keyframes draw {{ from {{ stroke-dashoffset: 220; }} }}
  .float {{ animation: float 4s ease-in-out {delay:.2f}s infinite; }}
  @keyframes float {{ 50% {{ transform: translateY(-6px); }} }}
  .ring {{ fill: {color}; fill-opacity: .1; stroke: {color}; stroke-opacity: .35; }}
  .trace {{ stroke-dasharray: 260 1340; animation: trace 5s linear {delay:.2f}s infinite; }}
  @keyframes trace {{ to {{ stroke-dashoffset: -1600; }} }}
  .in {{ animation: in .8s cubic-bezier(.2,.8,.2,1) {delay:.2f}s backwards; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateY(10px); }} }}
  .arrow {{ animation: nudge 1.8s ease-in-out infinite; }}
  @keyframes nudge {{ 50% {{ transform: translateX(5px); }} }}
  {REDUCED}
</style>
<rect width="{W}" height="{H}" rx="16" fill="{PANEL}"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#glow)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{LINE}"/>
<rect class="trace" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="url(#edge)" stroke-width="2" pathLength="1600"/>
<g class="float"><circle class="ring" cx="530" cy="64" r="38"/><g transform="translate(530 64) scale(.95)" class="icon">{ICONS[icon]}</g></g>
<g class="in">
  <text x="32" y="48" class="tag">{escape(tag)}</text>
  <text x="30" y="96" class="h">{escape(title)}<tspan class="arrow" dx="10" fill="{color}" font-size="24">→</tspan></text>
  {body}
</g>
</svg>"""
    write(f"card-{slug}.svg", svg)


# --------------------------------------------------------------------- footer
def footer():
    W, H = 1200, 150

    def wave(amp, length, y):
        d = f"M0,{y}"
        x = 0
        while x < W * 2 + length:
            d += f" q{length / 4},{-amp} {length / 2},0 t{length / 2},0"
            x += length
        return d + f" V{H} H0 Z"

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thanks for stopping by">
<title>Thanks for stopping by</title>
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient></defs>
<style>
  .w1 {{ animation: slide 9s linear infinite; }}
  .w2 {{ animation: slide 14s linear infinite reverse; }}
  .w3 {{ animation: slide 20s linear infinite; }}
  @keyframes slide {{ to {{ transform: translateX(-400px); }} }}
  .t {{ font: 700 26px {SANS}; fill: {TEXT}; letter-spacing: .3px; }}
  .m {{ font: 500 14px {MONO}; fill: {MUTED}; letter-spacing: 2px; }}
  {REDUCED}
</style>
<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<g clip-path="url(#c)">
  <path class="w3" d="{wave(18, 400, 92)}" fill="url(#g)" opacity=".12"/>
  <path class="w2" d="{wave(14, 400, 104)}" fill="url(#g)" opacity=".2"/>
  <path class="w1" d="{wave(10, 400, 118)}" fill="url(#g)" opacity=".45"/>
</g>
<text x="600" y="46" text-anchor="middle" class="t">Thanks for stopping by. Let's build something that matters.</text>
<text x="600" y="72" text-anchor="middle" class="m">— BLOP77 —</text>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>
</svg>"""
    write("footer.svg", svg)


if __name__ == "__main__":
    banner()
    featured()
    header("h-projects.svg", "Things I've shipped", 2, BLUE)
    header("h-featured.svg", "Featured build", 1, ORANGE)
    header("h-tools.svg", "Toolbox", 3, PURPLE)
    header("h-stats.svg", "Activity", 4, GREEN)
    for i, p in enumerate(PROJECTS):
        card(*p, delay=0.1 + (i % 2) * 0.15)
    footer()
