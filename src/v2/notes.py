# Adds lecture notes to each topic tab (and the question paper to the 2024 exam tab):
# view inline, view side by side with the tab content (wide screens), or download.
# Run after build_v2.py; edits enn582-v2.html in place. PDFs are served from notes/<file>.
import sys, os
D = sys.argv[1]
f = os.path.join(D, 'enn582-v2.html')
h = open(f).read()

def sub1(old, new):
    global h
    assert h.count(old) == 1, (old[:70], h.count(old))
    h = h.replace(old, new)

NOTES = {
    1: ('Week_1_MPC_notes.pdf', 'Week 1 · Model Predictive Control', 24),
    2: ('Week_2_and_3_DP_notes.pdf', 'Weeks 2 &amp; 3 · Dynamic Programming (deterministic and stochastic)', 15),
    3: ('Week_2_and_3_DP_notes.pdf', 'Weeks 2 &amp; 3 · Dynamic Programming (deterministic and stochastic)', 15),
    4: ('Week_4_Inf_DP.pdf', 'Week 4 · Infinite Horizon DP', 11),
    5: ('Week_5_ApproxDP.pdf', 'Week 5 · Approximate DP', 9),
    6: ('Week_6_RL.pdf', 'Week 6 · Reinforcement Learning', 9),
}

def box(fname, label, pages, tag='Lecture notes'):
    return ('  <div class="box notes" data-pdf="notes/%s" data-file="%s" data-label="%s"><span class="tag">%s</span>'
            '<p><b>%s</b> · PDF, %d pages</p>'
            '<div class="nact"><button type="button" class="btn nside">⇆ Side by side</button>'
            '<button type="button" class="btn ghost nview">📖 View here</button>'
            '<button type="button" class="btn ghost ndl">⬇ Download PDF</button>'
            '<a class="nopen" href="notes/%s" target="_blank" rel="noopener">Open in new tab ↗</a></div>'
            '<p class="stat nstat"></p><div class="nviewer" hidden></div></div>\n') % (fname, fname, label, tag, label, pages, fname)

for p, (fname, label, pages) in NOTES.items():
    marker = '  <div class="box pracbox"><span class="tag">Your practical · P%d</span>' % p
    sub1(marker, box(fname, label, pages) + marker)

sub1('<p class="lede">Written as you would answer in the exam, with marks in mind. Read the question, try it yourself, then compare.</p>',
     '<p class="lede">Written as you would answer in the exam, with marks in mind. Read the question, try it yourself, then compare.</p>\n'
     + box('ENN582_EXAM_2024_questions.pdf', 'ENN582 Exam 2024 · question paper', 2, 'Question paper'))

# docked side panel
sub1('</div></main>', '''</div></main>
<aside id="npane" aria-label="Lecture notes side panel" hidden>
  <div class="nphead"><div class="nptitle"><span class="tag">Notes</span><b id="nplabel"></b></div>
    <div class="npbtns"><button type="button" class="btn ghost" id="npdl">⬇</button><button type="button" class="btn ghost" id="npclose" aria-label="Close side panel">✕ Close</button></div></div>
  <p class="stat" id="npstat"></p>
  <div class="nviewer" id="npview"></div>
</aside>''')

css = '''.notes{background:var(--surface);border:1px solid var(--line)} .notes>.tag{color:var(--accent)}
.nact{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.nopen{font:500 14px/1 var(--f-body);color:var(--accent);padding:10px 4px}
.nviewer{max-height:80vh;overflow:auto;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px;display:flex;flex-direction:column;gap:8px}
.nviewer[hidden]{display:none!important}
.npage{background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.25);position:relative;width:100%;flex:0 0 auto}
.npage canvas{display:block;width:100%;height:auto}
.npage .pn{position:absolute;right:6px;bottom:4px;font:11px var(--f-mono);color:#555;background:rgba(255,255,255,.8);padding:1px 4px;border-radius:3px}
#npane{position:fixed;top:0;right:0;bottom:0;width:46vw;z-index:20;background:var(--surface);border-left:1px solid var(--line);display:flex;flex-direction:column;gap:6px;padding:10px 12px;box-shadow:-4px 0 14px rgba(0,0,0,.12)}
#npane[hidden]{display:none!important}
#npane .nviewer{flex:1 1 auto;max-height:none;min-height:0}
.nphead{display:flex;justify-content:space-between;align-items:center;gap:8px}
.nptitle{display:flex;flex-direction:column;gap:3px;min-width:0}
.nptitle .tag{font:600 11px/1 var(--f-mono);letter-spacing:.09em;text-transform:uppercase;color:var(--accent)}
.nptitle b{font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.npbtns{display:flex;gap:6px;flex:0 0 auto}
.npbtns .btn{padding:8px 10px}
body.split header.top,body.split nav.tabs,body.split main{margin-right:46vw}
body.split .wrap{max-width:none}
.nside{display:none}
@media (min-width:900px){.nside{display:inline-block}}
@media (max-width:899px){#npane{display:none!important} body.split header.top,body.split nav.tabs,body.split main{margin-right:0}}
'''
sub1('/* cheatsheet paper */', css + '/* cheatsheet paper */')

js = r'''
  // lecture notes: inline viewer, docked side-by-side panel, download
  var PDFJS='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',pdfjsP=null,dlP=null;
  function loadPdfjs(){
    if(pdfjsP)return pdfjsP;
    pdfjsP=new Promise(function(res,rej){var s=document.createElement('script');s.src=PDFJS;
      s.onload=function(){var l=window['pdfjs-dist/build/pdf'];if(!l)return rej(new Error('pdfjs'));l.GlobalWorkerOptions.workerSrc=PDFJS.replace('pdf.min.js','pdf.worker.min.js');res(l)};
      s.onerror=function(){pdfjsP=null;rej(new Error('pdfjs'))};document.head.appendChild(s)});
    return pdfjsP;
  }
  function getDl(){if(!dlP)dlP=(window.claude&&window.claude.use)?window.claude.use('downloads').catch(function(){return null}):Promise.resolve(null);return dlP}
  // render every page of url into viewer (lazily, as pages scroll into view)
  function renderPdf(viewer,url,st){
    viewer.innerHTML='';st.textContent='Loading notes…';var token={};viewer._tok=token;
    return loadPdfjs().then(function(lib){return lib.getDocument(url).promise}).then(function(doc){
      if(viewer._tok!==token)return;
      st.textContent=doc.numPages+' pages. Scroll inside the frame.';
      var obs=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting||e.target.dataset.done)return;e.target.dataset.done='1';obs.unobserve(e.target);
        var n=+e.target.dataset.n;doc.getPage(n).then(function(pg){
          var w=Math.max(260,viewer.clientWidth-18),v1=pg.getViewport({scale:1}),sc=w/v1.width,dpr=Math.min(window.devicePixelRatio||1,2),vp=pg.getViewport({scale:sc*dpr});
          var c=document.createElement('canvas');c.width=vp.width;c.height=vp.height;e.target.style.minHeight='';e.target.insertBefore(c,e.target.firstChild);
          return pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise;})})},{root:viewer,rootMargin:'600px 0px'});
      for(var i=1;i<=doc.numPages;i++){var d=document.createElement('div');d.className='npage';d.dataset.n=i;d.style.minHeight=Math.round((viewer.clientWidth-18)*1.3)+'px';
        var pn=document.createElement('span');pn.className='pn';pn.textContent=i+' / '+doc.numPages;d.appendChild(pn);viewer.appendChild(d);obs.observe(d)}
    }).catch(function(){if(viewer._tok===token)st.textContent='The notes could not be displayed in this view. Use Download PDF or Open in new tab.';throw new Error('render')});
  }
  function download(url,file,st,btn){
    btn.disabled=true;st.textContent='Preparing download…';
    getDl().then(function(dl){
      if(!dl){window.open(url,'_blank','noopener');st.textContent='Opened the PDF in a new tab; save it from there.';return}
      return fetch(url).then(function(r){if(!r.ok)throw new Error('fetch');return r.blob()}).then(function(b){return dl.save({filename:file,data:b})}).then(function(){st.textContent='Saved '+file+'.'});
    }).catch(function(e){var c=e&&e.code;st.textContent=c==='declined'?'Download cancelled.':c==='rate_limited'?'A save prompt is already open.':'Could not save the file here. Try Open in new tab.'}).then(function(){btn.disabled=false});
  }
  // docked panel
  var pane=document.getElementById('npane'),pview=document.getElementById('npview'),pst=document.getElementById('npstat'),plabel=document.getElementById('nplabel'),pcur=null;
  function openPane(nb){
    document.body.classList.add('split');pane.hidden=false;
    if(pcur===nb.dataset.pdf)return;
    pcur=nb.dataset.pdf;plabel.innerHTML=nb.dataset.label;pane.dataset.file=nb.dataset.file;
    renderPdf(pview,pcur,pst).catch(function(){});
  }
  function closePane(){document.body.classList.remove('split');pane.hidden=true;try{localStorage.setItem('enn582v2split','0')}catch(e){}}
  document.getElementById('npclose').addEventListener('click',closePane);
  document.getElementById('npdl').addEventListener('click',function(){if(pcur)download(pcur,pane.dataset.file,pst,this)});
  // when the panel is open, it follows the tab you switch to (tabs without notes keep the last notes)
  function follow(){if(pane.hidden)return;var p=[].filter.call(document.querySelectorAll('[data-panel]'),function(x){return !x.hidden})[0];var nb=p&&p.querySelector('.notes');if(nb)openPane(nb)}
  [].forEach.call(document.querySelectorAll('nav.tabs button,[data-goto]'),function(b){b.addEventListener('click',function(){setTimeout(follow,0)})});
  window.addEventListener('hashchange',function(){setTimeout(follow,0)});
  // inline viewer per notes box
  [].forEach.call(document.querySelectorAll('.notes'),function(nb){
    var url=nb.dataset.pdf,file=nb.dataset.file,viewer=nb.querySelector('.nviewer'),st=nb.querySelector('.nstat'),vb=nb.querySelector('.nview');
    vb.addEventListener('click',function(){
      if(viewer.hidden){viewer.hidden=false;vb.textContent='✕ Hide';if(!viewer.childNodes.length)renderPdf(viewer,url,st).catch(function(){viewer.hidden=true;vb.textContent='📖 View here'});}
      else{viewer.hidden=true;vb.textContent='📖 View here';}
    });
    nb.querySelector('.nside').addEventListener('click',function(){openPane(nb);try{localStorage.setItem('enn582v2split','1')}catch(e){}});
    nb.querySelector('.ndl').addEventListener('click',function(){download(url,file,st,this)});
  });
  // reopen the panel after a reload if it was open
  try{if(localStorage.getItem('enn582v2split')==='1'&&window.innerWidth>=900){pane.hidden=false;follow();if(!pcur)closePane()}}catch(e){}
'''
sub1('  // plan checkboxes', js + '\n  // plan checkboxes')
open(f, 'w').write(h)
print('notes ok', len(h))
