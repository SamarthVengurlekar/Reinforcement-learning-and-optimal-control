# Adds a "Lecture notes" viewer/download box to each topic tab (and the question paper to the 2024 exam tab).
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
    return ('  <div class="box notes" data-pdf="notes/%s" data-file="%s"><span class="tag">%s</span>'
            '<p><b>%s</b> · PDF, %d pages</p>'
            '<div class="nact"><button type="button" class="btn nview">📖 View notes here</button>'
            '<button type="button" class="btn ghost ndl">⬇ Download PDF</button>'
            '<a class="nopen" href="notes/%s" target="_blank" rel="noopener">Open in new tab ↗</a></div>'
            '<p class="stat nstat"></p><div class="nviewer" hidden></div></div>\n') % (fname, fname, tag, label, pages, fname)

for p, (fname, label, pages) in NOTES.items():
    marker = '  <div class="box pracbox"><span class="tag">Your practical · P%d</span>' % p
    sub1(marker, box(fname, label, pages) + marker)

sub1('<p class="lede">Written as you would answer in the exam, with marks in mind. Read the question, try it yourself, then compare.</p>',
     '<p class="lede">Written as you would answer in the exam, with marks in mind. Read the question, try it yourself, then compare.</p>\n'
     + box('ENN582_EXAM_2024_questions.pdf', 'ENN582 Exam 2024 · question paper', 2, 'Question paper'))

css = '''.notes{background:var(--surface);border:1px solid var(--line)} .notes>.tag{color:var(--accent)}
.nact{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.nopen{font:500 14px/1 var(--f-body);color:var(--accent);padding:10px 4px}
.nviewer{max-height:80vh;overflow:auto;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px;display:flex;flex-direction:column;gap:8px}
.nviewer[hidden]{display:none!important}
.npage{background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.25);position:relative;width:100%}
.npage canvas{display:block;width:100%;height:auto}
.npage .pn{position:absolute;right:6px;bottom:4px;font:11px var(--f-mono);color:#555;background:rgba(255,255,255,.8);padding:1px 4px;border-radius:3px}
'''
sub1('/* cheatsheet paper */', css + '/* cheatsheet paper */')

js = r'''
  // lecture notes: render in the page with PDF.js, or download
  var PDFJS='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',pdfjsP=null,dlP=null;
  function loadPdfjs(){
    if(pdfjsP)return pdfjsP;
    pdfjsP=new Promise(function(res,rej){var s=document.createElement('script');s.src=PDFJS;
      s.onload=function(){var l=window['pdfjs-dist/build/pdf'];if(!l)return rej(new Error('pdfjs'));l.GlobalWorkerOptions.workerSrc=PDFJS.replace('pdf.min.js','pdf.worker.min.js');res(l)};
      s.onerror=function(){pdfjsP=null;rej(new Error('pdfjs'))};document.head.appendChild(s)});
    return pdfjsP;
  }
  function getDl(){if(!dlP)dlP=(window.claude&&window.claude.use)?window.claude.use('downloads').catch(function(){return null}):Promise.resolve(null);return dlP}
  [].forEach.call(document.querySelectorAll('.notes'),function(nb){
    var url=nb.dataset.pdf,file=nb.dataset.file,viewer=nb.querySelector('.nviewer'),st=nb.querySelector('.nstat'),vb=nb.querySelector('.nview'),db=nb.querySelector('.ndl'),loaded=false;
    function render(){
      st.textContent='Loading notes…';
      loadPdfjs().then(function(lib){return lib.getDocument(url).promise}).then(function(doc){
        loaded=true;st.textContent=doc.numPages+' pages. Scroll inside the frame; pages render as they come into view.';
        var obs=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting||e.target.dataset.done)return;e.target.dataset.done='1';obs.unobserve(e.target);
          var n=+e.target.dataset.n;doc.getPage(n).then(function(pg){
            var w=Math.max(280,viewer.clientWidth-18),v1=pg.getViewport({scale:1}),sc=w/v1.width,dpr=Math.min(window.devicePixelRatio||1,2),vp=pg.getViewport({scale:sc*dpr});
            var c=document.createElement('canvas');c.width=vp.width;c.height=vp.height;e.target.style.minHeight='';e.target.insertBefore(c,e.target.firstChild);
            return pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise;})})},{root:viewer,rootMargin:'600px 0px'});
        for(var i=1;i<=doc.numPages;i++){var d=document.createElement('div');d.className='npage';d.dataset.n=i;d.style.minHeight=Math.round((viewer.clientWidth-18)*1.3)+'px';
          var pn=document.createElement('span');pn.className='pn';pn.textContent=i+' / '+doc.numPages;d.appendChild(pn);viewer.appendChild(d);obs.observe(d)}
      }).catch(function(){viewer.hidden=true;vb.textContent='📖 View notes here';st.textContent='The notes could not be displayed in this view. Use Download PDF or Open in new tab.'});
    }
    vb.addEventListener('click',function(){
      if(viewer.hidden){viewer.hidden=false;vb.textContent='✕ Hide notes';if(!loaded&&!viewer.childNodes.length)render();}
      else{viewer.hidden=true;vb.textContent='📖 View notes here';}
    });
    db.addEventListener('click',function(){
      db.disabled=true;st.textContent='Preparing download…';
      getDl().then(function(dl){
        if(!dl){window.open(url,'_blank','noopener');st.textContent='Opened the PDF in a new tab; save it from there.';return}
        return fetch(url).then(function(r){if(!r.ok)throw new Error('fetch');return r.blob()}).then(function(b){return dl.save({filename:file,data:b})}).then(function(){st.textContent='Saved '+file+'.'});
      }).catch(function(e){var c=e&&e.code;st.textContent=c==='declined'?'Download cancelled.':c==='rate_limited'?'A save prompt is already open.':'Could not save the file here. Try Open in new tab.'}).then(function(){db.disabled=false});
    });
  });
'''
sub1('  // plan checkboxes', js + '\n  // plan checkboxes')
open(f, 'w').write(h)
print('notes ok', len(h))
