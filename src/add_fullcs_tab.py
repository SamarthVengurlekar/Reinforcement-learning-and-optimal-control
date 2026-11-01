# Adds the "Full cheatsheet" tab (preview + notes-panel viewer + download) to the built index.html.
# Run after make_index.py:  python src/add_fullcs_tab.py index.html
import sys
f = sys.argv[1]
h = open(f).read()

def sub1(old, new):
    global h
    assert h.count(old) == 1, (old[:60], h.count(old))
    h = h.replace(old, new)

sub1('<button role="tab" data-tab="cheatsheet"><span class="n">↓</span>Cheatsheet</button>',
     '<button role="tab" data-tab="cheatsheet"><span class="n">↓</span>Cheatsheet</button>\n'
     '  <button role="tab" data-tab="fullcs"><span class="n">⇩</span>Full cheatsheet</button>')

sub1('</div></main>', '''<!-- ===================== FULL CHEATSHEET ===================== -->
<section class="panel" id="fullcs" data-panel="fullcs" hidden>
  <h2>Full cheatsheet (double-sided A4)</h2>
  <p class="lede">Every subsection from the six topic tabs (1.1 to 6.7) with its formulas and worked examples, plus a symbols list, on one double-sided A4 sheet. Topics are colour-coded; formulas are in tinted boxes and worked examples in cream boxes. Print double-sided, flipping on the long edge.</p>
  <div class="box notes" data-pdf="ENN582_Full_Cheatsheet.pdf" data-file="ENN582_Full_Cheatsheet.pdf" data-label="ENN582 full cheatsheet (2 sides)"><span class="tag">PDF</span><p><b>ENN582 full cheatsheet</b> · 2 pages (one sheet, double-sided)</p><div class="nact"><button type="button" class="btn nside">📖 View here</button><button type="button" class="btn ghost ndl">⬇ Download PDF</button><a class="nopen" href="ENN582_Full_Cheatsheet.pdf" target="_blank" rel="noopener">Open in new tab ↗</a></div><p class="stat nstat"></p></div>
  <h3>Side 1 · Topics 1–4</h3>
  <img class="fcs-prev" src="full_cheatsheet_side1.png" alt="Full cheatsheet side 1: MPC, deterministic DP, stochastic DP, start of infinite-horizon DP" loading="lazy">
  <h3>Side 2 · Topics 4–6 and symbols</h3>
  <img class="fcs-prev" src="full_cheatsheet_side2.png" alt="Full cheatsheet side 2: infinite-horizon DP, approximate DP, reinforcement learning, symbols" loading="lazy">
  <p class="stat">The previews are images. Use View here to zoom or mark up the PDF, or Download PDF to print it.</p>
</section>

</div></main>''')

sub1('/* cheatsheet paper */', '.fcs-prev{display:block;width:100%;max-width:820px;height:auto;margin:0 auto;border:1px solid var(--line);border-radius:4px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.12)}\n/* cheatsheet paper */')
open(f, 'w').write(h)
print('ok')
