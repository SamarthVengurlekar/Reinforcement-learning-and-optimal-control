import re, sys, os
D = sys.argv[1]
r = lambda f: open(os.path.join(D, f)).read()
h = r('main_base.html')

def sub1(old, new):
    global h
    assert h.count(old) == 1, (old[:60], h.count(old))
    h = h.replace(old, new)

# title + header
sub1('<title>ENN582 Exam Prep</title>', '<title>ENN582 Exam Prep v1</title>')
h = re.sub(r'<h1>[^<]*</h1>', '<h1>Exam Prep v1: lectures + your practicals</h1>', h, count=1)
h = re.sub(r'(<header class="top"><div class="wrap">.*?<p>)(.*?)(</p>)',
           r'\1Every topic from the Week 1–6 notes, plus a lesson for each of your six practical submissions (P1–P6), a mock exam built from them, the 2024 paper solved in full, practice questions, and the cheatsheet you can carry in.\3',
           h, count=1, flags=re.S)

# nav
sub1('<button role="tab" data-tab="exam">',
     '<button role="tab" data-tab="prac"><span class="n">P</span>Practicals P1–P6</button>\n  <button role="tab" data-tab="mock"><span class="n">M</span>Mock exam</button>\n  <button role="tab" data-tab="exam">')

# plan
plan = '''<div class="box idea"><span class="tag">New in v1</span>
    <p>Each topic tab now opens with a link to the matching practical. The <b>Practicals</b> tab teaches P1–P6 (code ↔ equation, your results explained, hand-sized versions, exam questions), and the <b>Mock exam</b> tab is a second full paper built from the practicals. The cheatsheet has a new section 9 with the practical results.</p>
  </div>

  <h3>9-day plan</h3>
  <p class="stat">Tick items as you finish them. Ticks are saved in this browser only.</p>
  <div class="plan" id="planlist">
    <label><input type="checkbox" id="p1"><span class="d">Day 1</span><span><b>MPC + P1 crane.</b> Read tab 01, then the P1 lesson. From memory: the cost function, the roles of Q/R/Q<sub>F</sub>, the four receding-horizon steps, and H, f, A<sub>in</sub>, b<sub>in</sub>. Do practice Q1–Q5 and P1-a to P1-d.</span></label>
    <label><input type="checkbox" id="p2"><span class="d">Day 2</span><span><b>Deterministic DP + P2.</b> Tab 02, then P2. Redo Tom's DP table and the TSP rollout on paper. Practice Q6–Q7, P2-a, P2-b.</span></label>
    <label><input type="checkbox" id="p3"><span class="d">Day 3</span><span><b>Stochastic DP + P3.</b> Tab 03, then P3. The fork (East/West) and parking recursions are prime exam material. Practice Q8–Q10, P3-a, P3-b.</span></label>
    <label><input type="checkbox" id="p4"><span class="d">Day 4</span><span><b>Infinite-horizon DP + P4.</b> Tab 04, then P4. Do one slippery Bellman backup by hand; know VI vs PI cold. Practice Q11–Q13, P4-a, P4-b.</span></label>
    <label><input type="checkbox" id="p5"><span class="d">Day 5</span><span><b>Approximate DP + P5.</b> Tab 05, then P5. One-step lookahead trap, one SGD weight update. Practice Q14–Q16, P5-a, P5-b.</span></label>
    <label><input type="checkbox" id="p6"><span class="d">Day 6</span><span><b>RL + P6.</b> Tab 06, then P6. SARSA vs Q-learning on one transition (−51 vs −1.995). Practice Q17–Q21, P6-a, P6-b.</span></label>
    <label><input type="checkbox" id="p7"><span class="d">Day 7</span><span><b>2024 paper, timed.</b> Only the cheatsheet allowed. Mark it against the ★ tab.</span></label>
    <label><input type="checkbox" id="p8"><span class="d">Day 8</span><span><b>Mock exam, timed.</b> Same rules. Mark it against the M tab.</span></label>
    <label><input type="checkbox" id="p9"><span class="d">Day 9</span><span><b>Fix gaps.</b> Redo every question you missed. Print the cheatsheet and add your own notes.</span></label>
  </div>'''
h = re.sub(r'<h3>8-day plan</h3>.*?</div>', lambda m: plan, h, count=1, flags=re.S)

# topic boxes
boxes = {
 'mpc': ('P1', 'pr1', 'Gantry crane: you designed Q and R (Bryson\'s rule), saw LQR be conservative (7.3 s), then built the batch QP and got 5.4 s with MPC running on the swing limits.'),
 'ddp': ('P2', 'pr2', 'Tom\'s journey A→H by backward DP (1063, A-B-F-H; the greedy route costs 1305) and the 4-city TSP, nearest neighbour and rollout.'),
 'sdp': ('P3', 'pr3', 'Random leg costs (certainty equivalence gives 1063 again), a random road closure (go West, 1013) and the parking stopping problem (threshold rules).'),
 'ihdp': ('P4', 'pr4', 'Grid world VI with resets, and Frozen Lake deterministic vs slippery: VI took 180 iterations, PI 5, and the slippery-optimal policy hugs walls.'),
 'adp': ('P5', 'pr5', 'Distance heuristic + one-step lookahead loops in a dead end; ℓ = 3 fixes it. Linear features learn r = [10, 10, 2] exactly by SGD.'),
 'rl': ('P6', 'pr6', 'Cliff Walking: Q-learning takes the 13-step edge path, SARSA a 15/17-step safe detour, because SARSA learns the value of the exploring policy.'),
}
for pid, (p, anchor, txt) in boxes.items():
    pat = re.compile(r'(<section class="panel" id="%s" data-panel="%s" hidden>\s*<h2>.*?</h2>\s*<p class="lede">.*?</p>)' % (pid, pid), re.S)
    box = ('\n  <div class="box pracbox"><span class="tag">Your practical · %s</span><p>%s</p>'
           '<p><button type="button" class="btn ghost" data-goto="prac" data-anchor="%s">Open the %s lesson →</button></p></div>') % (p, txt, anchor, p)
    h, n = pat.subn(lambda m: m.group(1) + box, h, count=1)
    assert n == 1, pid

# insert practicals + mock before 2024 exam
sub1('<!-- ===================== EXAM ===================== -->',
     r('prac.html') + '\n' + r('mock.html') + '\n<!-- ===================== EXAM ===================== -->')

# css
css = '''.pills{display:flex;flex-wrap:wrap;gap:8px}
.pill{font:500 13.5px/1 var(--f-body);background:var(--surface);color:var(--accent);border:1px solid var(--line);border-radius:999px;padding:9px 13px;cursor:pointer}
.pill:hover{border-color:var(--accent)}
article.prac{display:flex;flex-direction:column;gap:14px;scroll-margin-top:64px}
article.prac>h3{font-size:24px}
.pracbox{background:var(--ok-soft)} .pracbox>.tag{color:var(--ok)}
'''
sub1('/* cheatsheet paper */', css + '/* cheatsheet paper */')

# cheatsheet
cs = r('cs.html')
i = cs.rstrip().rfind('</div>')
cs = cs[:i] + r('cs9.html') + '\n</div>\n'
cs = cs.replace('ENN582 Exam Cheatsheet: RL &amp; Optimal Control', 'ENN582 Exam Cheatsheet v1: RL &amp; Optimal Control')
open(os.path.join(D, 'cs_full.html'), 'w').write(cs)
sub1('<!--CHEATSHEET-->', cs)
sub1('Every formula, algorithm, key number and answer recipe from the six topics, on two A4 pages (about 1.5 pages used, leaving room for your own notes).',
     'Every formula, algorithm, key number and answer recipe from the six topics, plus the key results from your six practicals (section 9), on two A4 pages.')
sub1("filename:'ENN582_Exam_Cheatsheet.pdf'", "filename:'ENN582_Exam_Cheatsheet_v1.pdf'")

# storage keys
h = h.replace("'enn582tab'", "'enn582v1tab'").replace("'enn582-'", "'enn582v1-'")

# JS: pills + goto
js = '''
  // practicals: jump links and cross-tab buttons
  function jump(id){var el=document.getElementById(id);if(el)el.scrollIntoView({behavior:'smooth',block:'start'})}
  [].forEach.call(document.querySelectorAll('[data-scroll]'),function(b){b.addEventListener('click',function(){jump(b.dataset.scroll)})});
  [].forEach.call(document.querySelectorAll('[data-goto]'),function(b){b.addEventListener('click',function(){show(b.dataset.goto,true);if(b.dataset.anchor)setTimeout(function(){jump(b.dataset.anchor)},60)})});
'''
sub1('  // plan checkboxes', js + '\n  // plan checkboxes')

open(os.path.join(D, 'enn582-v1.html'), 'w').write(h)
print('ok', len(h))
