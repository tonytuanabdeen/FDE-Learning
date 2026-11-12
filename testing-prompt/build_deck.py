#!/usr/bin/env python3
"""
Build: Agentforce Testing & Deployment — executive-ready interactive PPTX.
Generates branded background assets (Pillow) then the 19-slide deck (python-pptx).
Content is sourced from the vetted FDE presenter guides in E2E-Testing-Deployment-Guide/.
All examples use placeholders (Service_Agent, client-dev, YOUR-ORG) — no real data.
"""
import os, math, tempfile
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.oxml.ns import qn

OUT = "/Users/tabdeen/Documents/Claude/FDE-Learning/E2E-Testing-Deployment-output"
os.makedirs(OUT, exist_ok=True)
ASSETS = tempfile.mkdtemp(prefix="deck_assets_")

# ---------------------------------------------------------------- palette
NAVY   = RGBColor(0x13,0x12,0x4A)
INDIGO = RGBColor(0x2E,0x2E,0x86)
CARD   = RGBColor(0xFF,0xFF,0xFF)
BG     = RGBColor(0xEE,0xF3,0xFC)
PURPLE = RGBColor(0x4A,0x17,0xC4)
PURPLE2= RGBColor(0x6A,0x2B,0xD8)
BLUE   = RGBColor(0x1B,0x96,0xFF)
BLUEMID= RGBColor(0x2E,0x6B,0xE6)
SKY    = RGBColor(0x4A,0x9B,0xFF)
TEXT   = RGBColor(0x2A,0x2A,0x4A)
MUTED  = RGBColor(0x5E,0x61,0x92)
LINE   = RGBColor(0xDC,0xE3,0xF2)
GREEN  = RGBColor(0x1F,0x8F,0x5F)
WHITE  = RGBColor(0xFF,0xFF,0xFF)
L_WHITE= RGBColor(0xD9,0xE2,0xFF)
SHADOW = RGBColor(0xD6,0xDE,0xF0)
CODEBG = RGBColor(0x0E,0x1A,0x3A)
CODETX = RGBColor(0xD6,0xE2,0xFF)
CODECMT= RGBColor(0x8F,0xB0,0xE0)
CODEKW = RGBColor(0x79,0xE8,0xC0)
CODESTR= RGBColor(0xFF,0xD9,0x8A)

HEAD_FONT = "Arial"
BODY_FONT = "Arial"
MONO_FONT = "Courier New"

# ---------------------------------------------------------------- assets (Pillow)
def _font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def gradient(path, c1, c2, w=2000, h=1125):
    """Diagonal gradient: c1 at top-left, c2 at bottom-right, plus a soft glow."""
    img = Image.new("RGB", (w, h))
    px = img.load()
    maxd = w + h
    for y in range(h):
        for x in range(0, w, 2):
            t = (x + y) / maxd
            r = int(c1[0] + (c2[0]-c1[0])*t)
            g = int(c1[1] + (c2[1]-c1[1])*t)
            b = int(c1[2] + (c2[2]-c1[2])*t)
            px[x, y] = (r, g, b)
            if x+1 < w: px[x+1, y] = (r, g, b)
    # soft radial highlight upper-right
    glow = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy, rad = int(w*0.78), int(h*0.28), int(h*0.9)
    for i in range(rad, 0, -8):
        a = int(70 * (1 - i/rad))
        gd.ellipse([cx-i, cy-i, cx+i, cy+i], fill=a)
    white = Image.new("RGB", (w, h), (255,255,255))
    img = Image.composite(white, img, glow)
    img.save(path, "PNG")

def cloud_logo(path, body=(0x8F,0xC4,0xF2), txt=(255,255,255)):
    w, h = 680, 430
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    col = body + (255,)
    # puffy cloud from overlapping ellipses + flat base
    d.ellipse([70,150,290,370], fill=col)
    d.ellipse([170,70,430,330], fill=col)
    d.ellipse([330,120,540,330], fill=col)
    d.ellipse([430,180,610,360], fill=col)
    d.rounded_rectangle([110,250,590,360], radius=40, fill=col)
    f = _font(96, bold=False)
    tw = d.textlength("salesforce", font=f)
    d.text(((w-tw)/2, 215), "salesforce", font=f, fill=txt+(255,))
    img.save(path, "PNG")

G_TITLE = os.path.join(ASSETS, "grad_title.png")
G_SECT  = os.path.join(ASSETS, "grad_sect.png")
LOGO    = os.path.join(ASSETS, "logo.png")
gradient(G_TITLE, (0x27,0x2E,0xC6), (0x58,0x22,0xB4))
gradient(G_SECT,  (0x23,0x2A,0xBE), (0x4C,0x1E,0xA8))
cloud_logo(LOGO)

# ---------------------------------------------------------------- pptx scaffold
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = 13.333, 7.5

def slide():
    return prs.slides.add_slide(BLANK)

def solid_bg(s, rgb):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb

def fullbleed(s, path):
    s.shapes.add_picture(path, 0, 0, width=prs.slide_width, height=prs.slide_height)

def logo(s, w=1.15):
    pic = s.shapes.add_picture(LOGO, Inches(SW-w-0.45), Inches(0.33), width=Inches(w))
    return pic

def pagenum(s, n, light=False):
    tb = s.shapes.add_textbox(Inches(SW-0.9), Inches(SH-0.5), Inches(0.6), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    r = p.add_run(); r.text = str(n)
    r.font.size = Pt(11); r.font.color.rgb = WHITE if light else MUTED; r.font.name = BODY_FONT

def no_shadow(shape):
    try: shape.shadow.inherit = False
    except Exception: pass

def rrect(s, x, y, w, h, fill, line=None, radius=0.06, shadow=False, line_w=1.0):
    if shadow:
        sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x+0.05), Inches(y+0.07),
                                Inches(w), Inches(h))
        sh.adjustments[0] = radius; no_shadow(sh)
        sh.fill.solid(); sh.fill.fore_color.rgb = SHADOW; sh.line.fill.background()
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.adjustments[0] = radius; no_shadow(sp)
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    return sp

def pill(s, x, y, w, h, fill):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.adjustments[0] = 0.5; no_shadow(sp)
    sp.fill.solid(); sp.fill.fore_color.rgb = fill; sp.line.fill.background()
    return sp

def oval(s, x, y, d, fill):
    sp = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    no_shadow(sp); sp.fill.solid(); sp.fill.fore_color.rgb = fill; sp.line.fill.background()
    return sp

def center_text(shape, text, size, color, bold=True, font=HEAD_FONT):
    tf = shape.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font

def tbox(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    return tf

def para(tf, runs, size=14, color=TEXT, bold=False, font=BODY_FONT, align=PP_ALIGN.LEFT,
         before=0, after=4, bullet=False, leading=None, first=False):
    """runs: str OR list of (text,{overrides}). Returns the paragraph."""
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(before); p.space_after = Pt(after)
    if leading: p.line_spacing = leading
    if isinstance(runs, str):
        runs = [(runs, {})]
    if bullet:
        r = p.add_run(); r.text = "•  "
        r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = font
    for text, ov in runs:
        r = p.add_run(); r.text = text
        r.font.size = Pt(ov.get("size", size))
        r.font.bold = ov.get("bold", bold)
        r.font.italic = ov.get("italic", False)
        r.font.color.rgb = ov.get("color", color)
        r.font.name = ov.get("font", font)
    return p

def header(s, title, subtitle=None, n=None):
    """Light content-slide header. Returns y where content can start."""
    solid_bg(s, BG)
    logo(s)
    tf = tbox(s, 0.6, 0.34, 10.8, 0.9)
    para(tf, title, size=33, color=NAVY, bold=True, font=HEAD_FONT, first=True, after=0)
    if subtitle:
        tf2 = tbox(s, 0.62, 1.16, 11.2, 0.5)
        para(tf2, subtitle, size=17, color=INDIGO, bold=False, first=True, after=0)
    if n is not None: pagenum(s, n)
    return 1.85 if subtitle else 1.45

def badge(s, x, y, text, fill, color=WHITE, w=1.3, h=0.42, size=11):
    p = pill(s, x, y, w, h, fill)
    center_text(p, text, size, color, bold=True, font=BODY_FONT)
    return p

def icon(s, x, y, d, fill, glyph):
    o = oval(s, x, y, d, fill)
    center_text(o, glyph, int(d*26), WHITE, bold=True, font=HEAD_FONT)
    return o

def code_block(s, x, y, w, h, lines, title=None, radius=0.03):
    rrect(s, x, y, w, h, CODEBG, radius=radius, shadow=True)
    if title:
        tf = tbox(s, x+0.25, y+0.12, w-0.5, 0.3)
        para(tf, title, size=10.5, color=CODECMT, bold=True, font=MONO_FONT, first=True, after=0)
        ystart = y + 0.5
    else:
        ystart = y + 0.18
    tf = tbox(s, x+0.28, ystart, w-0.5, h-(ystart-y)-0.1)
    for i, ln in enumerate(lines):
        if isinstance(ln, str):
            segs = [(ln, {})]
        else:
            segs = ln
        p = tf.paragraphs[0] if i == 0 and not tf.paragraphs[0].runs else tf.add_paragraph()
        p.space_before = Pt(0); p.space_after = Pt(2); p.line_spacing = 1.0
        for text, ov in segs:
            r = p.add_run(); r.text = text
            r.font.name = MONO_FONT; r.font.size = Pt(ov.get("size", 10.5))
            r.font.color.rgb = ov.get("color", CODETX); r.font.bold = ov.get("bold", False)

def notes(s, text):
    s.notes_slide.notes_text_frame.text = text.strip()

# ================================================================ SLIDE 1 — Title
s = slide()
fullbleed(s, G_TITLE)
logo(s, w=1.25)
tf = tbox(s, 0.85, 2.55, 10.5, 2.2)
para(tf, "Agentforce", size=58, color=WHITE, bold=True, font=HEAD_FONT, first=True, after=0)
para(tf, "Testing & Deployment", size=58, color=WHITE, bold=True, font=HEAD_FONT, after=0)
tf2 = tbox(s, 0.9, 4.75, 10.5, 1.2)
para(tf2, "From build to production — proving an agent is ready, and shipping it safely.",
     size=20, color=L_WHITE, first=True, after=10)
para(tf2, [("Tuan Abdeen", {"bold":True,"color":WHITE}),
           ("  ·  Salesforce Certified Technical Architect (CTA)  ·  Forward Deployed Engineer, Middle East",
            {"color":L_WHITE})], size=14, after=0)
pagenum(s, 1, light=True)
notes(s, """
OPENING (set credibility + topic, ~60s).
Say: "Hello everyone, I'm Tuan Abdeen, a Salesforce Certified Technical Architect — one of roughly 400 globally — and a Forward Deployed Engineer in the Middle East. Today we explore one of the most important aspects of delivering production-ready Agentforce solutions: Testing & Deployment."
Frame the promise of the session in one line: "We test the DECISION, not just the sentence — and we treat the agent as metadata we ship with its dependencies."
Audience: FDEs, FDE leadership, technical/solution architects, Agentforce builders. Pitch to both leadership (confidence, governance) and engineers (patterns, CLI, trade-offs).
Transition: "Before tools, let's agree on WHY this matters."
""")

# ================================================================ SLIDE 2 — Objectives
s = slide()
header(s, "Setting the objectives", "Why Agentforce testing & deployment deserves its own discipline", n=2)
items = [
    ("Building is only half the lifecycle", "A working demo is not a production system. Engineering value is realised at release, not at build."),
    ("Behave consistently & reliably", "Agents are probabilistic — the same question can take a different path. We must prove behaviour holds."),
    ("Earn confidence before production", "Evidence, not optimism. Replace “it worked when I tried it” with measured pass-rates and quality scores."),
    ("From experimentation to engineering", "Move the team from ad-hoc clicking to repeatable, reviewable, governed delivery."),
    ("Repeatable & scalable practices", "Tests as code, release as a pipeline — so the 50th agent ships as safely as the first."),
    ("Protect customer trust", "A wrong or unsafe answer in production is a trust incident, not just a bug."),
]
cols, cw, ch, gx, gy = 2, 5.9, 1.42, 0.33, 0.22
x0, y0 = 0.6, 1.95
for i, (t, d) in enumerate(items):
    r, c = divmod(i, cols)
    x = x0 + c*(cw+gx); y = y0 + r*(ch+gy)
    rrect(s, x, y, cw, ch, CARD, line=LINE, radius=0.08, shadow=True)
    icon(s, x+0.22, y+0.24, 0.58, PURPLE if i % 2 == 0 else BLUEMID, str(i+1))
    tf = tbox(s, x+1.0, y+0.17, cw-1.15, ch-0.3, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, size=14.5, color=NAVY, bold=True, first=True, after=2)
    para(tf, d, size=10.8, color=MUTED, leading=1.02, after=0)
notes(s, """
Key message: testing & deployment is where assumptions meet reality — and where most production incidents are born.
Talk down the six objectives; spend the most time on "behave consistently" and "earn confidence before production." Make the probabilistic point concrete: ask the room the same question five times, get five correct but differently-worded answers.
Audience hook: "Which phase causes the most production incidents?" Answer: test & deploy.
Leadership framing: this is risk management and trust protection; engineering framing: it's the difference between a prototype and a product.
Transition: "Here's how we'll spend our time."
""")

# ================================================================ SLIDE 3 — Agenda
s = slide()
header(s, "Agenda", "Two disciplines, grounded in one shared context", n=3)
# context strip
rrect(s, 0.6, 1.95, 12.13, 0.95, CARD, line=LINE, shadow=True)
tf = tbox(s, 0.85, 2.05, 11.6, 0.75, anchor=MSO_ANCHOR.MIDDLE)
para(tf, "First, the context", size=12.5, color=PURPLE, bold=True, first=True, after=2)
para(tf, [("Overview  ·  Agent Development Lifecycle (ADLC)  ·  the WISMO use case  ·  why testing matters",
           {"color":TEXT,"size":12.5})], after=0)
# two big section cards
for i, (num, title, pts, col) in enumerate([
    ("1", "Testing Agentforce agents",
     ["Why agentic testing is different", "A multi-layer testing strategy", "The testing toolbox & tools", "Designing effective test coverage"], PURPLE),
    ("2", "Deploying Agentforce agents",
     ["An agent is linked metadata", "Git, SFDX & package.xml", "Validate → deploy → publish → activate", "Pipelines & release governance"], BLUEMID),
]):
    x = 0.6 + i*(6.0+0.13); y = 3.15; w = 6.0; h = 3.55
    rrect(s, x, y, w, h, CARD, line=LINE, radius=0.06, shadow=True)
    icon(s, x+0.4, y+0.4, 0.95, col, num)
    tf = tbox(s, x+1.55, y+0.42, w-1.8, 1.0, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, title, size=19, color=NAVY, bold=True, first=True, after=0)
    tf2 = tbox(s, x+0.45, y+1.6, w-0.8, h-1.8)
    for j, p in enumerate(pts):
        para(tf2, p, size=13.5, color=TEXT, bullet=True, first=(j==0), after=7)
notes(s, """
Lay out the arc: two parts — testing then deployment — but first a shared foundation so everyone reasons from the same mental model.
Set expectations on format: live demos interleaved with the slides, and a knowledge check to reinforce the key principles. Tell them the two take-home lines up front so they listen for the payoff.
Note the context block is deliberately before the two parts: overview, ADLC, the WISMO scenario, and why testing matters. Transition: "Let's start with the big picture."
""")

# ================================================================ SLIDE 4 — Overview (section)
def section_slide(num, title, subtitle, n):
    s = slide()
    fullbleed(s, G_SECT)
    logo(s, w=1.1)
    tf = tbox(s, 0.9, 2.7, 11.2, 2.2, anchor=MSO_ANCHOR.TOP)
    para(tf, num, size=22, color=SKY, bold=True, first=True, after=4)
    para(tf, title, size=48, color=WHITE, bold=True, font=HEAD_FONT, after=8)
    para(tf, subtitle, size=19, color=L_WHITE, after=0)
    pagenum(s, n, light=True)
    return s

s = section_slide("Section 1", "Overview", "Foundations — lifecycle, scenario, and why testing matters.", 4)
notes(s, """
Section divider. Keep it to ~15 seconds. Purpose: signal a context-setting block before the deep testing content.
Say: "Before any tool, three things set the frame — where testing and deployment sit in the lifecycle, the reference scenario we'll reuse all session, and why agentic testing needs a different mindset."
""")

# ================================================================ SLIDE 5 — ADLC
s = slide()
header(s, "The Agent Development Lifecycle", "Testing and deployment are gates in a continuous loop — not a final step", n=5)
stages = [("Discover","Use case, data, risks"),("Build","Topics, actions, prompts"),
          ("Evaluate","Test & score behaviour"),("Integrate","Channels & systems"),
          ("Deploy","Promote with its deps"),("Operate","Monitor & feed back")]
n = len(stages); gap = 0.18
w = (12.13 - gap*(n-1))/n; y = 2.05; x0 = 0.6
for i,(t,d) in enumerate(stages):
    x = x0 + i*(w+gap)
    col = [SKY,BLUEMID,PURPLE,PURPLE2,BLUEMID,NAVY][i]
    rrect(s, x, y, w, 1.15, col, radius=0.1)
    tf = tbox(s, x+0.08, y+0.14, w-0.16, 0.9, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER, first=True, after=2)
    para(tf, d, size=9, color=L_WHITE, align=PP_ALIGN.CENTER, after=0)
    if i < n-1:
        ar = s.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x+w-0.02), Inches(y+0.42), Inches(0.22), Inches(0.3))
        no_shadow(ar); ar.fill.solid(); ar.fill.fore_color.rgb = MUTED; ar.line.fill.background()
tf = tbox(s, 0.6, 3.35, 12.13, 0.4)
para(tf, [("Continuous loop:",{"bold":True,"color":PURPLE}),
          ("  every bug found becomes a test — Operate feeds signals back into Discover.",{"color":TEXT})],
     size=13, first=True, after=0)
# Release train
rrect(s, 0.6, 4.0, 12.13, 2.45, CARD, line=LINE, shadow=True)
tf = tbox(s, 0.9, 4.15, 11.6, 0.5)
para(tf, "The release train — promotion & testing gates", size=16, color=NAVY, bold=True, first=True, after=0)
train = [("DEV","Build & unit test"),("QA","Batch, conversation & red-team gate"),
         ("STAGING","UAT & channel validation"),("PRODUCTION","Activate, verify, monitor")]
tw = 2.75; ty = 4.85; tx0 = 0.95; tgap = ((12.13-0.7) - tw*4)/3
for i,(t,d) in enumerate(train):
    x = tx0 + i*(tw+tgap)
    col = [BLUEMID,PURPLE,PURPLE2,NAVY][i]
    rrect(s, x, ty, tw, 1.15, col, radius=0.08)
    tf = tbox(s, x+0.1, ty+0.14, tw-0.2, 0.9, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, size=15, color=WHITE, bold=True, align=PP_ALIGN.CENTER, first=True, after=3)
    para(tf, d, size=10, color=L_WHITE, align=PP_ALIGN.CENTER, after=0)
    if i < 3:
        ar = s.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x+tw-0.01), Inches(ty+0.4), Inches(0.26), Inches(0.34))
        no_shadow(ar); ar.fill.solid(); ar.fill.fore_color.rgb = SKY; ar.line.fill.background()
tf = tbox(s, 0.95, 6.1, 11.3, 0.3)
para(tf, "A failing test gate blocks promotion — exactly like a failing Apex test blocks a deploy.",
     size=11.5, color=MUTED, first=True, after=0)
notes(s, """
Key message: testing and deployment are GATES inside a continuous loop, not a phase bolted on at the end.
Walk the lifecycle: Discover -> Build -> Evaluate -> Integrate -> Deploy -> Operate, and stress the loop back — Operate (production monitoring + session traces) feeds new failures back into Discover/Evaluate as fresh test cases.
Then the release train: DEV -> QA -> STAGING -> PRODUCTION. Map gates to stages: unit + functional at DEV; batch, multi-turn and red-team at QA; UAT and channel validation at STAGING; activate, verify, and monitor at PROD.
The governance line to land for leadership: "A failing test gate blocks promotion, just like a failing Apex test blocks a deploy." That is deployment governance and production confidence in one sentence.
Transition: "Everything from here uses one concrete scenario."
""")

# ================================================================ SLIDE 6 — Use case
s = slide()
header(s, "The reference scenario: WISMO", "Customer Service Agent — “Where Is My Order?”", n=6)
# architecture flow
arch = [("React UI","Custom conversational interface"),
        ("Experience Cloud","Hosts the site / channel"),
        ("Headless Agentforce","Service Agent via Agent API"),
        ("Salesforce data","Orders, cases, knowledge")]
w=2.85; y=1.95; x0=0.6; gap=((12.13)-w*4)/3
for i,(t,d) in enumerate(arch):
    x=x0+i*(w+gap)
    rrect(s, x, y, w, 1.2, CARD, line=LINE, radius=0.08, shadow=True)
    icon(s, x+0.22, y+0.33, 0.55, [SKY,BLUEMID,PURPLE,NAVY][i], "")
    tf=tbox(s, x+0.95, y+0.17, w-1.05, 0.9, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, size=13.5, color=NAVY, bold=True, first=True, after=2)
    para(tf, d, size=10, color=MUTED, leading=1.0, after=0)
    if i<3:
        ar=s.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x+w+gap*0.15), Inches(y+0.45), Inches(0.2),Inches(0.28))
        no_shadow(ar); ar.fill.solid(); ar.fill.fore_color.rgb=MUTED; ar.line.fill.background()
# handles
rrect(s, 0.6, 3.45, 6.0, 2.9, CARD, line=LINE, shadow=True)
tf=tbox(s, 0.85, 3.6, 5.6, 2.6)
para(tf, "What the agent handles", size=15, color=NAVY, bold=True, first=True, after=6)
for h in ["Where is my order? status & tracking","Order cancellation","Refund-related questions","Frequently asked questions"]:
    para(tf, h, size=13, color=TEXT, bullet=True, after=6)
# scope
rrect(s, 6.73, 3.45, 6.0, 2.9, RGBColor(0xF4,0xF0,0xFF), line=RGBColor(0xD9,0xCB,0xF5), shadow=True)
tf=tbox(s, 6.98, 3.6, 5.6, 2.6)
para(tf, "Scope for today", size=15, color=PURPLE, bold=True, first=True, after=6)
para(tf, [("NOT about",{"bold":True,"color":PURPLE}),(" designing the agent, choosing the use case, its architecture, or building it from scratch.",{"color":TEXT})], size=12.5, after=8)
para(tf, [("Our focus:",{"bold":True,"color":NAVY}),(" how to test, validate, release and confidently operate an Agentforce solution in production.",{"color":TEXT})], size=12.5, after=0)
notes(s, """
Introduce WISMO as the thread we pull through every demo. Keep the architecture deliberately simple: a custom React conversational UI on an Experience Cloud site, talking to a headless Salesforce Service Agent via the Agent API, grounded in Orders/Cases/knowledge.
Why headless + React matters for this talk: it forces real channel testing (Playwright) because the customer never touches the Agent Builder preview — they touch your React UI in an iframe.
Set scope explicitly and out loud: today is NOT agent design or build. It is test, validate, release, operate. This keeps 30-35 minutes focused.
Transition: "So why can't we just reuse the testing we already know?"
""")

# ================================================================ SLIDE 7 — Section: Testing
s = section_slide("Section 2", "Agentforce testing", "What are we trying to prove, and what evidence is enough?", 7)
notes(s, """
Section divider into the testing discipline. The promise to repeat: "We test the decision, not just the sentence."
Transition straight into goals: what good testing must achieve.
""")

# ================================================================ SLIDE 8 — Why testing matters
s = slide()
header(s, "Why testing matters: goals & expectations", "What good Agentforce testing must achieve", n=8)
goals = [("Reliability & consistency","Same intent, dependable behaviour across runs"),
         ("Accuracy & grounding","Answers grounded in data/knowledge — not hallucinated"),
         ("Guardrails & safety","In scope, protects data, refuses what it should"),
         ("Business outcomes","The right action is taken and the task completes"),
         ("Regression prevention","New changes don’t silently break what worked"),
         ("Production readiness & trust","Confidence to go live — and protect customer trust")]
cols=3; cw=3.9; ch=1.95; gx=0.22; gy=0.25; x0=0.6; y0=2.0
for i,(t,d) in enumerate(goals):
    r,c=divmod(i,cols); x=x0+c*(cw+gx); y=y0+r*(ch+gy)
    rrect(s,x,y,cw,ch,CARD,line=LINE,radius=0.08,shadow=True)
    icon(s, x+0.3, y+0.3, 0.6, [PURPLE,BLUEMID,PURPLE2,BLUEMID,PURPLE,NAVY][i], str(i+1))
    tf=tbox(s,x+0.3,y+1.0,cw-0.55,ch-1.1)
    para(tf,t,size=14.5,color=NAVY,bold=True,first=True,after=3)
    para(tf,d,size=11.5,color=MUTED,leading=1.02,after=0)
notes(s, """
Establish the scorecard for "good" before showing any tool — otherwise tools look like features, not evidence.
For each goal give a one-line failure story: reliability (a flaky refund path), grounding (a made-up refund window), safety (leaking another customer's order), outcomes (it apologised nicely but never cancelled the order).
Land the trust point for leadership: in production a wrong or unsafe answer is a trust incident, not merely a defect. These six goals become the acceptance criteria the later layers satisfy.
Transition: "So why isn't our existing test playbook enough to hit these?"
""")

# ================================================================ SLIDE 9 — Traditional vs agentic
s = slide()
header(s, "Why traditional testing isn’t enough", "Deterministic software vs. probabilistic agents", n=9)
rows = [("Dimension","Traditional SDLC","Agentic ADLC"),
        ("Behaviour","Same input → same output","Same input can take a different path"),
        ("Inputs","Typed fields, validated forms","Free-form language: tone, typos, many languages"),
        ("What you assert","Exact values","Routing, action called, meaning of the answer, safety"),
        ("Pass criteria","100% of tests green","Pass-rate thresholds + scored quality metrics"),
        ("Triggers a retest","A code change","Code, data, instructions, knowledge — or a silent model update"),
        ("Security focus","Auth, query injection","Prompt injection, data leakage, excessive agency"),
        ("After release","Mostly done","Monitor for drift; feed failures back into tests")]
tb_rows=len(rows); tb_cols=3
gt = s.shapes.add_table(tb_rows, tb_cols, Inches(0.6), Inches(1.9), Inches(12.13), Inches(4.75)).table
gt.columns[0].width=Inches(2.5); gt.columns[1].width=Inches(4.0); gt.columns[2].width=Inches(5.63)
# strip default style banding by setting explicit fills
for ri in range(tb_rows):
    for ci in range(tb_cols):
        cell=gt.cell(ri,ci)
        cell.margin_left=Inches(0.12); cell.margin_right=Inches(0.08)
        cell.margin_top=Inches(0.04); cell.margin_bottom=Inches(0.04)
        cell.vertical_anchor=MSO_ANCHOR.MIDDLE
        if ri==0:
            cell.fill.solid(); cell.fill.fore_color.rgb=NAVY
        elif ci==0:
            cell.fill.solid(); cell.fill.fore_color.rgb=RGBColor(0xE4,0xEA,0xF8)
        else:
            cell.fill.solid(); cell.fill.fore_color.rgb=CARD if ri%2 else RGBColor(0xF6,0xF9,0xFE)
        p=cell.text_frame.paragraphs[0]; p.text=rows[ri][ci]
        run=p.runs[0]; run.font.name=BODY_FONT; run.font.size=Pt(11.5)
        if ri==0:
            run.font.bold=True; run.font.color.rgb=WHITE; run.font.size=Pt(12.5)
        elif ci==0:
            run.font.bold=True; run.font.color.rgb=NAVY
        elif ci==2:
            run.font.color.rgb=INDIGO
        else:
            run.font.color.rgb=TEXT
notes(s, """
Key message: an agent is probabilistic, not deterministic — "it worked when I tried it" proves almost nothing.
Talk down the rows, spending most time on two: "What you assert" and "What triggers a retest" — they drive everything that follows.
Say it out loud: "In classic Apex, assertEquals('shipped', status) is the whole game. Ask an agent 'where's my order?' five times and you get five correct but different sentences. Assert on the exact string and a right answer fails. So we assert on topic routing, the action called, the key facts in the reply, and safety — and we run each case more than once."
The sleeper row is "triggers a retest": a model update with no commit can regress behaviour. That is why testing later runs on a schedule, not only on PRs.
Transition: "If one test can't cover all that, we need layers."
""")

# ================================================================ SLIDE 10 — Multi-layer strategy
s = slide()
header(s, "A multi-layer testing strategy", "Each layer catches what the one below misses — cheap/deterministic → rich/realistic", n=10)
layers=[("1","Unit & functional","Apex, Flow, prompt & action-level assertions. Right request → right routing + right action.",PURPLE),
        ("2","Batch / bulk","Hundreds of utterances scored at scale with suites & datasets; regression coverage.",BLUEMID),
        ("3","Multi-turn conversation","Context retention, follow-ups, intent changes, multi-step task completion.",PURPLE2),
        ("4","Red team","Prompt injection, jailbreaks, data leakage, unauthorised actions, guardrail validation.",NAVY),
        ("5","UI & channel","Real channel: Experience Cloud + React UI, session behaviour, end-to-end journeys.",BLUEMID),
        ("6","Automated & continuous","Repeatable runs, CI/CD integration, scheduled regression, quality gates.",PURPLE)]
cols=3; cw=3.9; ch=1.95; gx=0.22; gy=0.25; x0=0.6; y0=2.0
for i,(num,t,d,col) in enumerate(layers):
    r,c=divmod(i,cols); x=x0+c*(cw+gx); y=y0+r*(ch+gy)
    rrect(s,x,y,cw,ch,CARD,line=LINE,radius=0.08,shadow=True)
    icon(s, x+0.28, y+0.28, 0.62, col, num)
    tf=tbox(s,x+1.05,y+0.26,cw-1.2,0.6,anchor=MSO_ANCHOR.MIDDLE)
    para(tf,t,size=14.5,color=NAVY,bold=True,first=True,after=0)
    tf2=tbox(s,x+0.3,y+1.02,cw-0.55,ch-1.1)
    para(tf2,d,size=11,color=MUTED,leading=1.04,first=True,after=0)
notes(s, """
Present as a ladder: cheap and deterministic at the bottom, expensive and realistic at the top; each layer exists because the one below it can't see a certain class of failure.
Map layers to WISMO: unit proves GetOrderStatus returns the right status; batch proves 200 phrasings of "where's my order" route correctly; multi-turn proves the agent remembers the order number across turns; red team proves it won't show a different customer's order; UI proves the answer actually renders in the React iframe; continuous proves none of this silently rots after a model update.
Engineering nuance: keep deterministic logic OUT of the LLM where you can, then test that logic with normal unit tests — the model should reason, not calculate.
Transition: "Each layer has a tool. Here's the toolbox."
""")

# ================================================================ SLIDE 11 — Subsection: Testing tools
s = section_slide("Section 2.1", "Testing tools", "The Agentforce testing ecosystem — and where each tool fits.", 11)
notes(s, """
Short subsection divider. Signal the shift from strategy to concrete tooling. Tell them you'll frame tools as an end-to-end workflow, not a feature list, then deep-dive the ones with live demos.
""")

# ================================================================ SLIDE 12 — Toolbox
s = slide()
header(s, "The Agentforce testing toolbox", "Eight methods combine into four evidence layers", n=12)
tbx=[("Discover & build",[("01","Manual exploration","discovered risks & scenarios · DEV/QA/STAGING"),
                           ("02","Agent previews","fast authoring feedback · DEV/QA")],PURPLE),
     ("Component-test & regress",[("03","Apex / Flow tests","deterministic assertions · DEV/QA"),
                                   ("04","Testing Center / suites","repeatable behaviour & regression · QA")],BLUEMID),
     ("Evaluate conversation & channel",[("05","Conversational Testing (ACT)","multi-turn outcome & state · QA"),
                                          ("06","Playwright","browser, channel & integration evidence · QA/STAGING")],PURPLE2),
     ("Accept & operate",[("07","UAT","business acceptance · STAGING/PROD"),
                           ("08","Production verification","released-system health · PROD")],NAVY)]
y=1.9; ch=1.12; gy=0.15; x=0.6; w=12.13
for i,(title,methods,col) in enumerate(tbx):
    yy=y+i*(ch+gy)
    accent = (i==3)
    rrect(s,x,yy,w,ch,CARD,line=(BLUE if accent else LINE),radius=0.07,shadow=True,line_w=2.0 if accent else 1.0)
    oval(s, x+0.28, yy+0.27, 0.58, col)
    center_text(s.shapes[-1], str(i+1), 20, WHITE)
    tf=tbox(s,x+1.15,yy+0.12,w-1.4,ch-0.2,anchor=MSO_ANCHOR.MIDDLE)
    para(tf,title,size=14.5,color=(BLUE if accent else NAVY),bold=True,first=True,after=3)
    for j,(nn,mt,md) in enumerate(methods):
        para(tf,[(nn+" ",{"bold":True,"color":col,"size":11.5}),
                 (mt,{"bold":True,"color":NAVY,"size":11.5}),
                 (" — "+md,{"color":MUTED,"size":11})], after=1)
notes(s, """
Frame the toolbox as an end-to-end workflow, not a menu. Eight methods, grouped into four evidence layers that line up with the release train.
Discover & build: manual exploration surfaces risks and real-world scenarios; agent previews give the fastest authoring feedback loop. Component-test & regress: Apex/Flow tests give deterministic assertions on the tools, Testing Center turns findings into repeatable, regression-grade suites. Evaluate conversation & channel: ACT validates multi-turn outcome and state; Playwright proves the customer-facing channel. Accept & operate (the highlighted layer): UAT is business sign-off, production verification is released-system health.
Strengths/limits in one breath each: previews are fast but have no memory; Testing Center is repeatable but sandbox-only and consumes credits; Playwright is realistic but slower and flakier.
Transition: "Let's start at the top of the funnel — manual exploration, live."
""")

# ================================================================ SLIDE 13 — Manual exploration
s = slide()
header(s, "Manual exploration", "Your fastest feedback loop — and your weakest memory", n=13)
badge(s, 10.9, 1.32, "LIVE DEMO", BLUE, w=1.8, h=0.4, size=12)
rrect(s,0.6,1.95,6.0,2.5,CARD,line=LINE,shadow=True)
tf=tbox(s,0.85,2.1,5.6,2.25)
para(tf,"What you explore",size=14.5,color=NAVY,bold=True,first=True,after=5)
for t in ["Agent Builder Preview & sf agent preview","Prompts, instructions, topics & actions",
          "Expected vs. actual behaviour","Backing Apex & Flow tests"]:
    para(tf,t,size=12.5,color=TEXT,bullet=True,after=5)
rrect(s,6.73,1.95,6.0,2.5,CARD,line=LINE,shadow=True)
tf=tbox(s,6.98,2.1,5.6,2.25)
para(tf,"Simulation vs. live",size=14.5,color=NAVY,bold=True,first=True,after=5)
para(tf,[("Simulation ",{"bold":True,"color":PURPLE}),("— isolated from org data; use while instructions still change.",{})],size=12.5,after=5)
para(tf,[("Live ",{"bold":True,"color":BLUEMID}),("— runs real actions on sandbox data; use before you commit a version.",{})],size=12.5,after=5)
para(tf,[("Always read the trace: ",{"bold":True,"color":NAVY}),("subagent → action inputs → outputs → final response.",{})],size=12.5,after=0)
code_block(s,0.6,4.6,12.13,1.35,
    [[("# fast feedback loop from the IDE", {"color":CODECMT})],
     [("sf agent preview ",{"color":CODEKW}),("--api-name ",{"color":CODETX}),("Service_Agent",{"color":CODESTR})],
     [("sf agent preview ",{"color":CODEKW}),("--api-name ",{"color":CODETX}),("Service_Agent ",{"color":CODESTR}),("--use-live-actions",{"color":CODETX})]])
tf=tbox(s,0.6,5.95,12.13,0.4)
para(tf,[("Rule: ",{"bold":True,"color":PURPLE}),("anything you find in Preview becomes a batch test case. A bug found by hand and not captured will come back.",{"color":TEXT})],size=12,first=True,after=0)
notes(s, """
Key message: Preview is the fastest feedback loop and the weakest memory — it finds problems, it doesn't prove their absence.
Explain the two modes with intent: simulation isolates from org data (use it while instructions churn); live runs real actions against sandbox data (use it right before you commit a version). The reasoning trace is the point — read subagent selected, action inputs, action outputs, final response every single time.
DEMO 1 (~90s): ask an order-status question in simulation; open the trace and point to subagent + action inputs; switch to live and repeat; break the instructions to force a misroute, show it in the trace, fix it — then say "that misroute is now a test case."
Recovery: if live mode is slow or errors, fall back to the recorded clip; never debug org auth on stage.
Transition: "Hand-testing doesn't scale. We need hundreds of cases, scored."
""")

# ================================================================ SLIDE 14 — Batch / bulk
s = slide()
header(s, "Batch / bulk testing", "Agentforce Testing Center — one suite, hundreds of utterances, a scored grid", n=14)
badge(s, 10.9, 1.32, "LIVE DEMO", BLUE, w=1.8, h=0.4, size=12)
rrect(s,0.6,1.9,6.0,2.95,CARD,line=LINE,shadow=True)
tf=tbox(s,0.85,2.03,5.6,2.7)
para(tf,"How it works",size=14.5,color=NAVY,bold=True,first=True,after=5)
for t in ["Lives as a tab in Agentforce Studio","Cases 3 ways: AI-generated, Q&A from knowledge, or your own CSV/YAML",
          "Each case asserts expected subagent, actions & outcome",
          "Scorers: accuracy, completeness, coherence, conciseness, latency, instruction adherence",
          "Run history compares quality across agent versions"]:
    para(tf,t,size=11.8,color=TEXT,bullet=True,after=4)
rrect(s,6.73,1.9,6.0,0.95,RGBColor(0xFF,0xF4,0xE8),line=RGBColor(0xF3,0xD6,0xAE),shadow=True)
tf=tbox(s,6.98,2.0,5.6,0.78,anchor=MSO_ANCHOR.MIDDLE)
para(tf,[("! Guardrail  ",{"bold":True,"color":RGBColor(0xB5,0x6A,0x00)}),
         ("Testing Center consumes requests/credits and can modify CRM data. Run in sandboxes only.",{"color":TEXT})],size=11.5,first=True,after=0)
code_block(s,6.73,3.0,6.0,1.85,
    [[("# tests as code — the FDE workflow",{"color":CODECMT})],
     [("sf agent generate test-spec",{"color":CODEKW})],
     [("sf agent test create ",{"color":CODEKW}),("--spec ",{"color":CODETX}),("tests/wismo.yaml",{"color":CODESTR})],
     [("sf agent test run ",{"color":CODEKW}),("--api-name ",{"color":CODETX}),("Service_Agent_Tests \\",{"color":CODESTR})],
     [("  --wait ",{"color":CODETX}),("15 ",{"color":CODESTR}),("--result-format ",{"color":CODETX}),("junit",{"color":CODESTR})]],
    title="bash")
tf=tbox(s,0.6,4.95,12.13,0.95)
para(tf,[("The YAML spec becomes ",{"color":TEXT}),("AiEvaluationDefinition",{"bold":True,"color":PURPLE,"font":MONO_FONT}),
         (" metadata — so tests are versioned and deployed alongside the agent. ",{"color":TEXT}),
         ("--result-format",{"font":MONO_FONT,"color":INDIGO}),(" supports human, json, junit, tap (junit is what CI dashboards read).",{"color":TEXT})],
     size=12,first=True,after=0)
notes(s, """
Key message: move from one-off hand testing to one suite of hundreds of utterances, scored, repeatable, and comparable across versions.
Explain the three ways to create cases and the governance warning: runs consume requests/credits and can modify CRM data, so sandboxes only. Make the "tests as code" point loudly — the YAML becomes AiEvaluationDefinition metadata, versioned and deployed with the agent; junit output is what CI reads.
DEMO 2 (~2 min): generate ~20 cases for one subagent; hand-edit two and add a negative case; run; open a FAILING result to show the trace + scorer explanation; compare against the previous run.
Say it: "AI-generated cases are a starting point — review them like code. They come out polite and well-formed; real customers don't."
Transition: "Batch covers single turns. Real chats have many."
""")

# ================================================================ SLIDE 15 — ACT
s = slide()
header(s, "Agentforce Conversational Testing (ACT)", "Does the agent remember, and does it recover?", n=15)
left=[("Multi-turn by design","Simulates a whole dialogue with a synthetic persona across many turns."),
      ("Asserts state, not just the last line","Context carry-over and memory — not only last-answer correctness."),
      ("Scriptable scenarios","Greet → give details → ask a follow-up → change your mind."),
      ("Conversational quality","Evaluate coherence and turns-to-resolution across the exchange.")]
for i,(t,d) in enumerate(left):
    y=1.95+i*1.12
    rrect(s,0.6,y,6.0,0.98,CARD,line=LINE,shadow=True)
    icon(s,0.82,y+0.22,0.55,[PURPLE,BLUEMID,PURPLE2,NAVY][i],str(i+1))
    tf=tbox(s,1.55,y+0.1,4.9,0.8,anchor=MSO_ANCHOR.MIDDLE)
    para(tf,t,size=13,color=NAVY,bold=True,first=True,after=1)
    para(tf,d,size=10.5,color=MUTED,leading=1.0,after=0)
rrect(s,6.73,1.95,6.0,4.4,RGBColor(0xF4,0xF0,0xFF),line=RGBColor(0xD9,0xCB,0xF5),shadow=True)
tf=tbox(s,7.0,2.15,5.5,4.0)
para(tf,"When to use ACT vs. alternatives",size=14,color=PURPLE,bold=True,first=True,after=6)
para(tf,[("Testing Center",{"bold":True,"color":NAVY}),(" takes a Conversation History column — earlier turns go in, the next reply is checked (last turn must be the agent).",{"color":TEXT})],size=12,after=6)
para(tf,[("ACT",{"bold":True,"color":NAVY}),(" simulates the whole multi-turn dialogue with a persona — frustrated customer, non-native speaker, distracted user.",{"color":TEXT})],size=12,after=6)
para(tf,[("Agent API harness",{"bold":True,"color":NAVY}),(" when you need long/branching scripts, custom LLM-as-judge scoring, or load checks — drive the agent from Python. (Needs an External Client App, client-credentials flow.)",{"color":TEXT})],size=12,after=6)
para(tf,[("Demo cue: ",{"bold":True,"color":PURPLE}),("run “remember my name” with memory on (both turns pass), then off (turn 2 fails) — exactly what conversation testing is for.",{"color":TEXT})],size=11.5,after=0)
notes(s, """
Slide only (no live demo). Key message: real chats have more than one message — do they remember, and do they recover?
Distinguish the three tools clearly: Testing Center with a Conversation History column (earlier turns in, next reply checked; the last turn in the history must be the agent); ACT, which simulates a full multi-turn dialogue with a synthetic persona; and the Agent API harness for long/branching scripts, custom LLM-as-judge scoring, or load — which needs an External Client App using the client-credentials flow.
Design scenarios like a real person, not a QA script: frustrated customer, non-native speaker, someone who changes their mind mid-chat. Measure turns-to-resolution, not just pass/fail.
Optional verbal demo cue: "remember my name" with memory on vs off — the off case failing the second turn is the whole point.
Transition: "Even a perfect brain fails if the customer can't see the answer. Enter Playwright."
""")

# ================================================================ SLIDE 16 — Playwright
s = slide()
header(s, "Playwright & real-channel testing", "Testing Center checks the brain — Playwright checks what the customer sees", n=16)
badge(s, 10.9, 1.32, "LIVE DEMO", BLUE, w=1.8, h=0.4, size=12)
rrect(s,0.6,1.9,5.6,3.0,CARD,line=LINE,shadow=True)
tf=tbox(s,0.85,2.03,5.2,2.8)
para(tf,"Why test the channel",size=14,color=NAVY,bold=True,first=True,after=5)
for t in ["Enhanced Chat on Experience Cloud / the React site","Real user journeys & multi-turn interactions",
          "Rendered responses, rich content, handoff, file upload","Session & conversation continuity",
          "Plugs into automated regression pipelines"]:
    para(tf,t,size=11.8,color=TEXT,bullet=True,after=4)
para(tf,[("Assert loosely on agent text, strictly on UI state.",{"bold":True,"color":PURPLE})],size=11.5,after=0)
code_block(s,6.33,1.9,6.4,4.0,
    [[("test(",{"color":CODEKW}),("'order status in Enhanced Chat'",{"color":CODESTR}),(", async ({ page }) => {",{"color":CODETX})],
     [("  await page.goto(process.env.SITE_URL)",{"color":CODETX})],
     [("  await page.getByRole(",{"color":CODETX}),("'button'",{"color":CODESTR}),(", { name: /chat/i }).click()",{"color":CODETX})],
     [("  const chat = page.frameLocator(",{"color":CODETX}),("'iframe'",{"color":CODESTR}),(")",{"color":CODETX})],
     [("  await chat.getByRole(",{"color":CODETX}),("'textbox'",{"color":CODESTR}),(").fill(",{"color":CODETX})],
     [("     ",{"color":CODETX}),("'Where is order ORD-1001?'",{"color":CODESTR}),(")",{"color":CODETX})],
     [("  // loose on wording",{"color":CODECMT})],
     [("  await expect(chat.getByText(/shipped/i))",{"color":CODETX})],
     [("     .toBeVisible({ timeout: 30000 })",{"color":CODETX})],
     [("  // strict on UI",{"color":CODECMT})],
     [("  await expect(page).toHaveScreenshot()",{"color":CODETX})],
     [("})",{"color":CODETX})]],
    title="order-status.spec.ts")
tf=tbox(s,0.6,5.0,5.6,0.9)
para(tf,[("Tip: ",{"bold":True,"color":PURPLE}),("Enhanced Chat renders in an iframe — capture the exact selector with ",{"color":TEXT}),("npx playwright codegen",{"font":MONO_FONT,"color":INDIGO}),(".",{"color":TEXT})],size=11.5,first=True,after=0)
notes(s, """
Key message: Testing Center checks the brain; Playwright checks what the customer actually sees in the channel — iframe rendering, rich content, human handoff, file upload.
The assertion philosophy is the lesson: assert loosely on the agent's wording (regex/keywords, because it's non-deterministic) but strictly on UI state (screenshots, visibility, DOM). Enhanced Chat renders inside an iframe, so capture the exact selector with `npx playwright codegen` rather than guessing.
DEMO 3 (~90s): run HEADED so the room sees the browser drive WISMO through the React UI; show a pass; force a failure; open the Playwright trace viewer to show the timeline and DOM snapshots.
Recovery: UI demos are the flakiest — if it hangs, cut to the recording (this is the demo to drop first if you're behind, but keep the slide).
Transition: "Tools are necessary but not sufficient — coverage is a design problem."
""")

# ================================================================ SLIDE 17 — Subsection: Designing tests
s = section_slide("Section 3", "Designing effective tests", "From running tools to designing meaningful coverage.", 17)
notes(s, """
Subsection divider. Pivot the room from "which tool" to "what to test." The trap we're countering: teams measure coverage by number of prompts instead of diversity of scenarios, personas, data and outcomes.
""")

# ================================================================ SLIDE 18 — Designing effective scenarios
s = slide()
header(s, "Building effective agent test scenarios", "Design each test across four dimensions", n=18)
dims=[("Scenario","Define the goal","Happy, ambiguous & unsupported requests; where the journey starts and ends.",SKY),
      ("Persona","Represent the user","Who they are; context, language, role & permissions; what they must be denied.",BLUEMID),
      ("Data","Vary the state","No / one / many matches; incomplete, stale & boundary values; required integration state.",PURPLE),
      ("Outcome","Make it observable","Acceptable actions & responses, including clarification, refusal, escalation & safe failure.",NAVY)]
# pipeline pills
pw=2.85; py=3.3; px0=0.6; pgap=((12.13)-pw*4)/3
for i,(t,cap_t,cap_d,col) in enumerate(dims):
    x=px0+i*(pw+pgap)
    pill(s,x,py,pw,0.72,col)
    center_text(s.shapes[-1],t,17,WHITE)
    # caption above for 0,2 ; below for 1,3 (alternate)
    above = (i%2==0)
    cy = py-1.35 if above else py+0.95
    tf=tbox(s,x-0.1,cy,pw+0.2,1.3,anchor=(MSO_ANCHOR.BOTTOM if above else MSO_ANCHOR.TOP))
    para(tf,cap_t,size=12.5,color=NAVY,bold=True,align=PP_ALIGN.CENTER,first=True,after=2)
    para(tf,cap_d,size=10.3,color=MUTED,align=PP_ALIGN.CENTER,leading=1.02,after=0)
# bottom principle
rrect(s,0.6,5.75,12.13,0.95,RGBColor(0xF4,0xF0,0xFF),line=RGBColor(0xD9,0xCB,0xF5),shadow=True)
tf=tbox(s,0.9,5.85,11.5,0.78,anchor=MSO_ANCHOR.MIDDLE)
para(tf,[("Starting recipe per subagent: ",{"bold":True,"color":PURPLE}),
         ("5 happy-path phrasings · 3 edge cases · 2 negatives — vary tone, length, typos & language; run each suite more than once.  ",{"color":TEXT}),
         ("Test the boundary: ",{"bold":True,"color":NAVY}),("the allowed request, the denied request, and the manipulated request.",{"color":TEXT})],
     size=11.5,first=True,after=0)
notes(s, """
Key message: good coverage is not more prompts — it is systematic variation across scenario, persona, data and outcome.
Walk the four dimensions with WISMO: Scenario — not just "where's my order" but the ambiguous "it's late" and the unsupported "change my delivery address"; Persona — a logged-in customer vs an anonymous one, a non-native speaker, someone who must be denied another customer's order; Data — an order with no match, one match, multiple matches, a stale status, a boundary like a just-shipped order; Outcome — the observable: did it call the right action, refuse safely, clarify, or escalate?
Give them the starting recipe so they leave with a number: 5 happy / 3 edge / 2 negative per subagent, varying tone/length/typos/language, each suite run more than once. And the boundary trio: the allowed request, the denied request, the manipulated request.
Transition: "Let's lock in the principles with a quick knowledge check."
""")

# ================================================================ SLIDE 19 — Knowledge check
s = slide()
header(s, "Knowledge check", "Five questions — reveal the answer, then the one-line why", n=19)
quiz=[("1","Why not assert an exact string on an agent’s reply?",
       "Replies are non-deterministic — same input, different wording.","Assert on topic, action & the meaning/key-facts instead."),
      ("2","Why wrap an Apex action test in System.runAs(agentUser)?",
       "To test with the agent user’s real permissions.","The classic silent failure: it works for admin, not the agent user."),
      ("3","Where should Testing Center runs happen?",
       "Sandboxes only.","Runs consume requests/credits and can modify CRM data."),
      ("4","A new model ships with no code change — what catches a regression?",
       "Scheduled (nightly) agent test runs + production monitoring.","Agents drift without a commit, so testing runs on a schedule."),
      ("5","Which tool checks what the customer actually sees in the channel?",
       "Playwright (UI / channel testing).","Testing Center checks the brain; Playwright checks the rendered channel.")]
cols=2; cw=5.95; ch=1.3; gx=0.23; gy=0.18; x0=0.6; y0=1.95
for i,(num,q,a,why) in enumerate(quiz):
    r,c=divmod(i,cols); x=x0+c*(cw+gx); y=y0+r*(ch+gy)
    rrect(s,x,y,cw,ch,CARD,line=LINE,radius=0.07,shadow=True)
    icon(s,x+0.22,y+0.2,0.5,PURPLE,num)
    tf=tbox(s,x+0.9,y+0.1,cw-1.05,ch-0.2,anchor=MSO_ANCHOR.MIDDLE)
    para(tf,q,size=11.8,color=NAVY,bold=True,first=True,after=2)
    para(tf,[("✓ ",{"bold":True,"color":GREEN,"size":12}),(a,{"bold":True,"color":GREEN,"size":11})],after=1)
    para(tf,why,size=9.5,color=MUTED,leading=1.0,after=0)
# 6th cell: closing takeaway
x=x0+1*(cw+gx); y=y0+2*(ch+gy)
rrect(s,x,y,cw,ch,NAVY,radius=0.07,shadow=True)
tf=tbox(s,x+0.3,y+0.12,cw-0.55,ch-0.2,anchor=MSO_ANCHOR.MIDDLE)
para(tf,"Take it back to your first engagement",size=12.5,color=WHITE,bold=True,first=True,after=3)
para(tf,[("Test the decision, not the sentence. ",{"bold":True,"color":SKY}),("Treat the agent as metadata — ship it with its dependencies and let the pipeline say no.",{"color":L_WHITE})],size=10.5,after=0)
notes(s, """
Run this as a poll, not a lecture — on a virtual call it is what keeps the room awake. Reveal each answer after the room responds in chat, then give the one-line why.
Q1 rationale: assert on topic routing, the action called, and the meaning/key-facts of the reply. Q2: the #1 silent failure is the agent user lacking field access — runAs surfaces it. Q3: sandboxes only, because runs consume credits and can mutate CRM data. Q4: scheduled nightly runs + production monitoring, because agents drift with no commit. Q5: Playwright — Testing Center checks the brain, Playwright checks the rendered channel; assert loosely on text, strictly on UI.
Close on the two take-home lines in the navy card. Then open the floor: likely questions are "how many tests is enough" (5/3/2 per subagent, grow from real failures), "how do we handle flaky results" (run N times, pass at a threshold, track the trend), and "blocking gate from day one" (no — non-blocking ~2 weeks, then blocking once the team trusts the numbers).
""")

prs.save(os.path.join(OUT, "Agentforce-Testing-and-Deployment.pptx"))
print("Saved PPTX ->", os.path.join(OUT, "Agentforce-Testing-and-Deployment.pptx"))
print("Slides:", len(prs.slides._sldIdLst))
