import re, sys, os
D = sys.argv[1]
h = open(os.path.join(D, '../v1/enn582-v1.html')).read()
eli = open(os.path.join(D, 'eli5.html')).read()

def sub1(old, new):
    global h
    assert h.count(old) == 1, (old[:70], h.count(old))
    h = h.replace(old, new)

# grid heatmap for the infinite-horizon ELI5 (P4 values)
V = [[-4.0951, -3.439, -2.71, -1.9], [-3.439, -2.71, -1.9, -1], [-4.0951, -3.439, -1, 0], [-4.68559, -4.0951, 0, 1]]
P = [['↓', '↓', '↓', '↓'], ['→', '→', '→', '↓'], ['↑', '↑', '→', '↓'], ['↑', '↑', '→', 'G']]
bad = {(0, 2), (2, 2), (3, 2)}
cs, x0, y0 = 56, 20, 12
g = []
for i in range(4):
    for j in range(4):
        op = 0.12 + 0.75 * (V[i][j] + 4.7) / 5.7
        x, y = x0 + j * cs, y0 + i * cs
        stroke = 'stroke:var(--mark);stroke-width:3' if (i, j) in bad else 'stroke:var(--line);stroke-width:1'
        g.append(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" style="fill:var(--accent);fill-opacity:{op:.2f};{stroke}"/>')
        g.append(f'<text x="{x+cs/2}" y="{y+22}" text-anchor="middle" font-size="15">{P[i][j]}</text>')
        g.append(f'<text x="{x+cs/2}" y="{y+42}" text-anchor="middle" font-size="10.5">{V[i][j]:g}</text>')
eli = eli.replace('<g id="g4"></g>', '<g>' + ''.join(g) + '</g>')

blocks = dict(re.findall(r'<!--ELI:(\w+)-->(.*?)<!--/ELI-->', eli, re.S))
for pid, p in zip(['mpc', 'ddp', 'sdp', 'ihdp', 'adp', 'rl'], range(1, 7)):
    marker = 'data-anchor="pr%d">Open the P%d lesson →</button></p></div>' % (p, p)
    sub1(marker, marker + '\n' + blocks[pid])

# titles
sub1('<title>ENN582 Exam Prep v1</title>', '<title>ENN582 Exam Prep v2</title>')
sub1('<h1>Exam Prep v1: lectures + your practicals</h1>', '<h1>Exam Prep v2: lectures, ELI5 and your practicals</h1>')
sub1('<div class="eyebrow">ENN582 · Reinforcement Learning and Optimal Control</div>',
     '<div class="toprow"><div class="eyebrow">ENN582 · Reinforcement Learning and Optimal Control</div>'
     '<button type="button" class="themebtn" id="themebtn" aria-label="Switch colour theme">◐ Theme</button></div>')
sub1('<span class="tag">New in v1</span>', '<span class="tag">New in v2</span>')
sub1('The cheatsheet has a new section 9 with the practical results.</p>',
     'The cheatsheet has a new section 9 with the practical results. <b>v2</b> adds an <b>ELI5</b> block at the top of every topic tab (plain-language analogies, a diagram, links back to your practicals, and YouTube videos you can play in the page), a light/dark switch (top right), and every tab visible at once.</p>')

# tokens for ELI5 colour in all three theme blocks
sub1('--ok:#2E7548; --ok-soft:#E3F1E7;', '--ok:#2E7548; --ok-soft:#E3F1E7; --eli:#6B3FA0; --eli-soft:#F2ECF9;')
h = h.replace('--ok:#6BC48F; --ok-soft:#173326;', '--ok:#6BC48F; --ok-soft:#173326; --eli:#C8A8F2; --eli-soft:#271F35;')
assert h.count('--eli:#C8A8F2') == 2

css = '''/* v2: all tabs visible (wrap), theme switch, ELI5 blocks, video cards */
[hidden]{display:none!important}
.vid .vlen{color:var(--ink);font-weight:600}
nav.tabs .wrap{flex-wrap:wrap;overflow:visible;gap:4px 2px;padding-block:6px}
nav.tabs button{padding:9px 10px 8px;border-radius:5px 5px 0 0}
nav.tabs button[aria-selected="true"]{background:var(--accent-soft)}
@media (max-width:760px){nav.tabs{position:static}nav.tabs button{font-size:13px;padding:8px 8px 7px}}
.toprow{display:flex;justify-content:space-between;align-items:center;gap:12px}
.themebtn{font:500 13px/1 var(--f-body);color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:8px 12px;cursor:pointer}
.themebtn:hover{border-color:var(--accent)}
.eli5{border:2px solid var(--eli);border-radius:8px;background:var(--eli-soft);padding:16px;display:flex;flex-direction:column;gap:14px;min-width:0}
.eli-head{display:flex;align-items:center;gap:10px}
.eli-badge{font:700 12px/1 var(--f-mono);letter-spacing:.08em;background:var(--eli);color:var(--surface);border-radius:4px;padding:6px 8px}
h3.eli-title{margin:0;padding:0;border:0;font-size:20px;color:var(--eli)}
.eli5 svg.dia{background:var(--surface);border-radius:6px;padding:6px}
.eli5 .eli-plan{fill:var(--eli-soft);stroke:var(--eli)}
.eli-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px}
.eli-card{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:12px 14px;display:flex;flex-direction:column;gap:7px;min-width:0}
.eli-card h4{color:var(--ink);font-size:15.5px}
.eli-prac{font-size:14.5px;border-left:3px solid var(--ok);padding-left:9px;color:var(--ink)}
.eli-prac b{color:var(--ok)}
.vids{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.vid{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:12px 14px;display:flex;flex-direction:column;gap:6px;min-width:0}
.vid::before{content:"▶ VIDEO";font:600 10.5px/1 var(--f-mono);letter-spacing:.08em;color:#C4302B}
.vid .vsrc{font:500 12px/1.3 var(--f-mono);color:var(--muted)}
.vid .vact{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.vid .vact a,.vid .vact button{font:500 13px/1 var(--f-body);padding:8px 11px;border-radius:5px;cursor:pointer;text-decoration:none}
.vid .vact button{background:var(--accent);color:var(--surface);border:0}
.vid .vact a{color:var(--accent);border:1px solid var(--accent)}
.vframe{grid-column:1/-1;display:flex;flex-direction:column;gap:6px}
.vframe iframe{width:100%;aspect-ratio:16/9;border:0;border-radius:6px;background:#000}
'''
sub1('/* cheatsheet paper */', css + '/* cheatsheet paper */')

js = '''
  // theme switch (light/dark), remembered per browser
  var root=document.documentElement,tb=document.getElementById('themebtn');
  function eff(){var t=root.getAttribute('data-theme');if(t)return t;return window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
  function lab(){tb.textContent=eff()==='dark'?'☀ Light mode':'☾ Dark mode'}
  try{var st0=localStorage.getItem('enn582v2theme');if(st0)root.setAttribute('data-theme',st0)}catch(e){}
  lab();
  tb.addEventListener('click',function(){var n=eff()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('enn582v2theme',n)}catch(e){}lab()});
  if(window.matchMedia)matchMedia('(prefers-color-scheme: dark)').addEventListener('change',lab);

  // video cards: open on YouTube, or play inside the page
  [].forEach.call(document.querySelectorAll('.vid'),function(v){
    var id=v.dataset.yt,list=v.dataset.list;
    var url=id?'https://www.youtube.com/watch?v='+id:'https://www.youtube.com/playlist?list='+list;
    var emb=id?'https://www.youtube-nocookie.com/embed/'+id:'https://www.youtube-nocookie.com/embed/videoseries?list='+list;
    var act=document.createElement('div');act.className='vact';
    var b=document.createElement('button');b.type='button';b.textContent='▶ Play here';
    var a=document.createElement('a');a.href=url;a.target='_blank';a.rel='noopener';a.textContent='Open on YouTube ↗';
    act.appendChild(b);act.appendChild(a);v.appendChild(act);
    b.addEventListener('click',function(){
      var grid=v.parentNode,old=grid.querySelector('.vframe');if(old)old.remove();
      var f=document.createElement('div');f.className='vframe';
      var ifr=document.createElement('iframe');ifr.src=emb+(id?'?autoplay=1':'&autoplay=1');ifr.title=v.querySelector(':scope > b').textContent;
      ifr.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';ifr.allowFullscreen=true;
      var p=document.createElement('p');p.className='stat';p.innerHTML='If the player stays blank, this viewer blocks embedded video. Use <b>Open on YouTube ↗</b> instead.';
      f.appendChild(ifr);f.appendChild(p);grid.appendChild(f);f.scrollIntoView({behavior:'smooth',block:'nearest'});
    });
  });
'''
sub1('  // plan checkboxes', js + '\n  // plan checkboxes')
sub1("try{localStorage.setItem('enn582v1tab',id)}catch(e){}", "try{localStorage.setItem('enn582v1tab',id)}catch(e){}\n    if(location.hash.slice(1)!==id&&history.replaceState)history.replaceState(null,'','#'+id);")
sub1("  // plan checkboxes", "  window.addEventListener('hashchange',function(){var t=location.hash.slice(1);if(panels[t])show(t,true)});\n  // plan checkboxes")
h = h.replace("'enn582v1tab'", "'enn582v2tab'").replace("'enn582v1-'", "'enn582v2-'")
open(os.path.join(D, 'enn582-v2.html'), 'w').write(h)
print('ok', len(h))
