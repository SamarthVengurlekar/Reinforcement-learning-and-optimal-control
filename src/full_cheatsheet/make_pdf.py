# Renders cs_full.html (+ as many extras blocks as fit) into a 2-page (double-sided) A4 PDF,
# 3 columns per page, choosing the largest font size at which everything fits.
# Usage: python make_pdf.py <out.pdf>
import sys, os, re, io, pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
core = open(os.path.join(HERE, 'cs_full.html')).read()
extras = re.findall(r'<!--X\d-->(.*?)<!--/X\d-->', open(os.path.join(HERE, 'extras.html')).read(), re.S)
OUT = sys.argv[1]
W, H = pymupdf.paper_size('a4')
M, GAP, PAGES = 15, 11, 2
NCOL = int(os.environ.get('NCOL', '3'))
CW = (W - 2 * M - (NCOL - 1) * GAP) / NCOL
arch = pymupdf.Archive('/System/Library/Fonts/Supplemental')

# one colour per topic: (heading colour, formula-box tint)
TOPIC = [('#0b4f73', '#e3eef4'), ('#2f6b2f', '#e6f1e4'), ('#5a3d8a', '#ede7f5'),
         ('#9c4610', '#f7ebe0'), ('#8a1f45', '#f5e4eb'), ('#0d6a6a', '#e0f1f0')]

def tag_topics(html):
    # give every h2/h3/formula box the class of the topic it belongs to
    out, t = [], 0
    for part in re.split(r'(<h2>|<h3>|<p class="f">)', html):
        if part == '<h2>':
            t += 1; out.append(f'<h2 class="t{t}">')
        elif part == '<h3>':
            out.append(f'<h3 class="t{t}">')
        elif part == '<p class="f">':
            out.append(f'<p class="f t{t}">')
        else:
            out.append(part)
    return ''.join(out)

core = tag_topics(core)

def css(fs):
    return f'''
@font-face{{font-family:U;src:url("Arial Unicode.ttf");}}
@font-face{{font-family:U;font-weight:bold;src:url("Arial Bold.ttf");}}
*{{font-family:U;}}
body{{font-size:{fs}pt;line-height:1.27;color:#000;}}
h1{{font-size:{fs+2.2}pt;margin:0 0 2pt 0;color:#0b4f73;}}
h2{{font-size:{fs+1.7}pt;margin:3.5pt 0 2pt 0;padding:1.5pt 4pt 0 4pt;color:#ffffff;}}
h3{{font-size:{fs+0.6}pt;margin:3pt 0 0.8pt 0;}}
p{{margin:0 0 2.5pt 0;}}
ul{{margin:0 0 2pt 0;padding-left:9pt;}}
li{{margin:0 0 0.8pt 0;}}
p.f{{padding:1.5pt 3pt 0 3pt;margin-bottom:3pt;font-weight:bold;}}
p.ex{{color:#3a2a10;background-color:#fdf5e6;padding:1.5pt 3pt 0 3pt;margin-bottom:3pt;}}
p.ex b{{color:#8a5a00;}}
''' + ''.join(f'h2.t{i+1}{{background-color:{c};}} h3.t{i+1}{{color:{c};}} p.t{i+1}{{background-color:{t};}}\n' for i, (c, t) in enumerate(TOPIC)) + f'''
b{{font-weight:bold;}}
sub,sup{{font-size:{fs*0.72:.2f}pt;}}
table{{border-collapse:collapse;width:100%;}}
td{{border:0.4pt solid #b8c4cc;padding:1pt 3pt;vertical-align:top;}}
'''

def layout(html, fs, write=None):
    """Return number of columns used; optionally write the PDF."""
    story = pymupdf.Story(html=html, user_css=css(fs), archive=arch)
    # Story only advances when each placed rect is drawn, so always draw (to memory when measuring)
    writer = pymupdf.DocumentWriter(write if write else io.BytesIO())
    n, more = 0, 1
    while more:
        col = n % NCOL
        if col == 0:
            dev = writer.begin_page(pymupdf.Rect(0, 0, W, H))
        r = pymupdf.Rect(M + col * (CW + GAP), M, M + col * (CW + GAP) + CW, H - M - 6)
        more, _ = story.place(r)
        story.draw(dev)
        if col == NCOL - 1 or not more:
            writer.end_page()
        n += 1
        if n > 3 * NCOL * PAGES:
            if col != NCOL - 1 and more:
                writer.end_page()
            break
    writer.close()
    return n

cap = NCOL * PAGES
MIN_FS = float(os.environ.get('MIN_FS', '8.4'))   # readability floor when adding extras

def max_font(html):
    for fs10 in range(120, 54, -1):
        if layout(html, fs10 / 10) <= cap:
            return fs10 / 10
    return None

core_fs = max_font(core.replace('<!--EXTRAS-->', ''))
print('core alone fits at', core_fs, 'pt')
fs, k, html = core_fs, 0, core.replace('<!--EXTRAS-->', '')
for kk in range(1, len(extras) + 1):              # add extras while the font stays readable
    h2 = core.replace('<!--EXTRAS-->', ''.join(extras[:kk]))
    f2 = max_font(h2)
    if f2 is None or f2 < MIN_FS:
        break
    fs, k, html = f2, kk, h2
if os.environ.get('FORCE_FS', '8.4'):
    fs = float(os.environ.get('FORCE_FS', '8.4'))  # leaves room for the symbols table
tmp = OUT + '.tmp'
layout(html, fs, tmp)
d = pymupdf.open(tmp)
names = ['MPC', 'Deterministic DP', 'Stochastic DP', 'Infinite-horizon DP', 'Approximate DP', 'RL']
heads = ['Model Predictive Control', 'Deterministic DP', 'Stochastic DP &', 'Infinite-horizon DP', 'Approximate DP', 'Reinforcement Learning']
cur = -1
for i, p in enumerate(d):
    for c in range(NCOL):                                      # hide a box-background artefact just above each column
        x0 = M + c * (CW + GAP)
        p.draw_rect(pymupdf.Rect(x0 - 2, M - 2, x0 + CW + 2, M + 0.6), color=None, fill=(1, 1, 1))
    for c in range(1, NCOL):                                   # thin rules between columns
        x = M + c * (CW + GAP) - GAP / 2
        p.draw_line((x, M), (x, H - M - 6), color=(.78, .8, .82), width=0.5)
    lines = [' '.join(l.replace('\xa0', ' ').split()) for l in p.get_text().splitlines() if l.strip()]
    starts = [int(m.group(1)) - 1 for l in lines for m in [re.match(r'^([1-6]) · ', l)] if m]
    span = sorted(set(([cur] if cur >= 0 and not (lines and re.match(r'^[1-6] · ', lines[0])) else []) + starts))
    if starts: cur = starts[-1]
    on = ', '.join(f'{j+1} {names[j]}' for j in span)
    p.insert_text((M, H - 6), f'ENN582 cheatsheet · side {i+1}/{len(d)} · {on}', fontsize=6.2, color=(.35, .35, .35))
# fill the space left at the end of the last column with the symbols table (shrunk to fit)
last = d[-1]
xl = M + (NCOL - 1) * (CW + GAP)
bottoms = [b[3] for b in last.get_text('blocks') if b[0] >= xl - 1 and b[3] < H - M - 6]
y_end = max(bottoms) if bottoms else M
box = pymupdf.Rect(xl, y_end + 5, xl + CW, H - M - 6)
ncss = css(fs) + 'h2.t0{background-color:#333f48;} p.sym{margin:0;padding:0.9pt 2pt;border-bottom:0.4pt solid #c9d1d6;}'
if box.height > 40:
    spare, scale = last.insert_htmlbox(box, open(os.path.join(HERE, 'notation.html')).read(), css=ncss, archive=arch, scale_low=0.6)
    print('symbols box', round(box.height), 'spare', spare, 'scale', scale)
d.subset_fonts()
d.save(OUT, garbage=4, deflate=True)
os.remove(tmp)
print(f'font {fs}pt, extras {k}/{len(extras)}, pages {len(d)}')
for i in range(len(d)):
    d[i].get_pixmap(dpi=110).save(OUT.replace('.pdf', f'_p{i+1}.png'))
