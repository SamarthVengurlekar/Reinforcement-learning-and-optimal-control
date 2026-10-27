# Adds lecture notes to each topic tab (and the question paper to the 2024 exam tab).
# "View here" opens a notes panel beside the tab content (full screen on narrow screens) with
# zoom and marking tools (pen, highlighter, eraser; marks saved in the browser), plus download.
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
            '<div class="nact"><button type="button" class="btn nside">📖 View here</button>'
            '<button type="button" class="btn ghost ndl">⬇ Download PDF</button>'
            '<a class="nopen" href="notes/%s" target="_blank" rel="noopener">Open in new tab ↗</a></div>'
            '<p class="stat nstat"></p></div>\n') % (fname, fname, label, tag, label, pages, fname)

for p, (fname, label, pages) in NOTES.items():
    marker = '  <div class="box pracbox"><span class="tag">Your practical · P%d</span>' % p
    sub1(marker, box(fname, label, pages) + marker)

sub1('<p class="lede">Written as you would answer in the exam, with marks in mind. Read the question, try it yourself, then compare.</p>',
     '<p class="lede">Written as you would answer in the exam, with marks in mind. Read the question, try it yourself, then compare.</p>\n'
     + box('ENN582_EXAM_2024_questions.pdf', 'ENN582 Exam 2024 · question paper', 2, 'Question paper'))

sub1('</div></main>', '''</div></main>
<aside id="npane" aria-label="Lecture notes panel" hidden>
  <div class="nphead"><div class="nptitle"><span class="tag">Notes</span><b id="nplabel"></b></div>
    <div class="npbtns"><button type="button" class="btn ghost" id="npfull" title="Full screen notes">⛶ Full screen</button><button type="button" class="btn ghost" id="npdl" title="Download PDF">⬇ PDF</button><button type="button" class="btn ghost" id="npclose" aria-label="Close notes">✕ Close</button></div></div>
  <div class="nptools" role="toolbar" aria-label="Zoom and marking tools">
    <div class="tg"><button type="button" data-z="-" title="Zoom out" aria-label="Zoom out">−</button><span id="npzoom" class="zl">100%</span><button type="button" data-z="+" title="Zoom in" aria-label="Zoom in">+</button><button type="button" data-z="fit" title="Fit page width">↔ Width</button><button type="button" data-z="page" title="Fit the entire page in view">↕ Page</button></div>
    <div class="tg"><button type="button" data-tool="hand" title="Scroll / select nothing" aria-pressed="true">✋</button><button type="button" data-tool="pen" title="Pen" aria-pressed="false">✏️</button><button type="button" data-tool="hl" title="Highlighter" aria-pressed="false">🖍</button><button type="button" data-tool="erase" title="Eraser (removes a whole stroke)" aria-pressed="false">⌫</button></div>
    <div class="tg" id="npcolors"><button type="button" class="sw" data-c="#d62828" title="Red" aria-pressed="true" style="--c:#d62828"></button><button type="button" class="sw" data-c="#1d4ed8" title="Blue" aria-pressed="false" style="--c:#1d4ed8"></button><button type="button" class="sw" data-c="#15803d" title="Green" aria-pressed="false" style="--c:#15803d"></button><button type="button" class="sw" data-c="#facc15" title="Yellow" aria-pressed="false" style="--c:#facc15"></button><button type="button" class="sw" data-c="#111111" title="Black" aria-pressed="false" style="--c:#111111"></button></div>
    <div class="tg"><button type="button" id="npundo" title="Undo last mark">↶ Undo</button><button type="button" id="npclear" title="Clear all marks in this PDF">🗑 Clear</button></div>
  </div>
  <p class="stat" id="npstat"></p>
  <div class="nviewer" id="npview"></div>
</aside>''')

css = '''.notes{background:var(--surface);border:1px solid var(--line)} .notes>.tag{color:var(--accent)}
.nact{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.nopen{font:500 14px/1 var(--f-body);color:var(--accent);padding:10px 4px}
.nviewer{overflow:auto;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:8px;display:flex;flex-direction:column;gap:10px}
.npage{background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.25);position:relative;flex:0 0 auto;align-self:flex-start;margin:0 auto}
.npage canvas{position:absolute;inset:0;width:100%;height:100%;display:block}
.npage canvas.ann{z-index:2;pointer-events:none}
.nviewer.drawing canvas.ann{pointer-events:auto;touch-action:none;cursor:crosshair}
.npage .pn{position:absolute;right:6px;bottom:4px;z-index:3;font:11px var(--f-mono);color:#555;background:rgba(255,255,255,.8);padding:1px 4px;border-radius:3px;pointer-events:none}
#npane{position:fixed;top:0;right:0;bottom:0;width:46vw;z-index:20;background:var(--surface);border-left:1px solid var(--line);display:flex;flex-direction:column;gap:6px;padding:10px 12px;box-shadow:-4px 0 14px rgba(0,0,0,.12)}
#npane[hidden]{display:none!important}
#npane.full,#npane:fullscreen{width:100vw;left:0;border-left:0}
#npane .nviewer{flex:1 1 auto;min-height:0}
.nphead{display:flex;justify-content:space-between;align-items:center;gap:8px}
.nptitle{display:flex;flex-direction:column;gap:3px;min-width:0}
.nptitle .tag{font:600 11px/1 var(--f-mono);letter-spacing:.09em;text-transform:uppercase;color:var(--accent)}
.nptitle b{font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.npbtns{display:flex;gap:6px;flex:0 0 auto}
.npbtns .btn{padding:8px 10px}
.nptools{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center}
.nptools .tg{display:flex;gap:3px;align-items:center}
.nptools button{font:500 13px/1 var(--f-body);min-width:32px;height:32px;padding:0 8px;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:5px;cursor:pointer}
.nptools button:hover{border-color:var(--accent)}
.nptools button[aria-pressed="true"]{background:var(--accent-soft);border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.nptools .zl{font:500 12px/1 var(--f-mono);min-width:44px;text-align:center;color:var(--muted)}
.nptools .sw{min-width:24px;width:24px;height:24px;padding:0;border-radius:50%;background:var(--c)}
.nptools .sw[aria-pressed="true"]{background:var(--c);border-color:var(--c);box-shadow:0 0 0 2px var(--surface),0 0 0 4px var(--ink)}
body.split header.top,body.split nav.tabs,body.split main{margin-right:46vw}
body.split .wrap{max-width:none}
@media (max-width:899px){#npane{width:100vw;border-left:0} body.split header.top,body.split nav.tabs,body.split main{margin-right:0}}
'''
sub1('/* cheatsheet paper */', css + '/* cheatsheet paper */')

js = r'''
  // lecture notes: panel viewer with zoom and marking tools, plus download
  var PDFJS='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',pdfjsP=null,dlP=null;
  function loadPdfjs(){
    if(pdfjsP)return pdfjsP;
    pdfjsP=new Promise(function(res,rej){var s=document.createElement('script');s.src=PDFJS;
      s.onload=function(){var l=window['pdfjs-dist/build/pdf'];if(!l)return rej(new Error('pdfjs'));l.GlobalWorkerOptions.workerSrc=PDFJS.replace('pdf.min.js','pdf.worker.min.js');res(l)};
      s.onerror=function(){pdfjsP=null;rej(new Error('pdfjs'))};document.head.appendChild(s)});
    return pdfjsP;
  }
  function getDl(){if(!dlP)dlP=(window.claude&&window.claude.use)?window.claude.use('downloads').catch(function(){return null}):Promise.resolve(null);return dlP}
  function download(url,file,st,btn){
    btn.disabled=true;st.textContent='Preparing download…';
    getDl().then(function(dl){
      if(!dl){window.open(url,'_blank','noopener');st.textContent='Opened the PDF in a new tab; save it from there.';return}
      return fetch(url).then(function(r){if(!r.ok)throw new Error('fetch');return r.blob()}).then(function(b){return dl.save({filename:file,data:b})}).then(function(){st.textContent='Saved '+file+'.'});
    }).catch(function(e){var c=e&&e.code;st.textContent=c==='declined'?'Download cancelled.':c==='rate_limited'?'A save prompt is already open.':'Could not save the file here. Try Open in new tab.'}).then(function(){btn.disabled=false});
  }

  var pane=document.getElementById('npane'),pview=document.getElementById('npview'),pst=document.getElementById('npstat'),plabel=document.getElementById('nplabel'),pzoom=document.getElementById('npzoom');
  var N={doc:null,url:null,file:null,zoom:1,base:600,tool:'hand',color:'#d62828',ann:{},undo:[],obs:null,tok:null};
  var ZOOMS=[0.25,0.5,0.75,1,1.25,1.5,2,2.5,3];
  function annKey(){return 'enn582v2ann:'+N.url}
  function loadAnn(){try{return JSON.parse(localStorage.getItem(annKey())||'{}')||{}}catch(e){return {}}}
  function saveAnn(){try{localStorage.setItem(annKey(),JSON.stringify(N.ann))}catch(e){pst.textContent='Marks could not be saved in this browser (storage unavailable).'}}
  function pages(){return [].slice.call(pview.querySelectorAll('.npage'))}
  function sizePage(w){var px=Math.round(N.base*N.zoom);w.style.width=px+'px';w.style.height=Math.round(px*(+w.dataset.r))+'px'}
  function drawAnn(w,cur){
    var c=w.querySelector('canvas.ann');if(!c)return;var ctx=c.getContext('2d'),W=c.width,H=c.height;ctx.clearRect(0,0,W,H);
    var list=(N.ann[w.dataset.n]||[]).slice();if(cur)list.push(cur);
    list.forEach(function(s){if(!s.p.length)return;ctx.save();ctx.lineCap='round';ctx.lineJoin='round';ctx.strokeStyle=s.c;
      if(s.t==='hl'){ctx.globalAlpha=.32;ctx.lineWidth=0.02*W;ctx.lineCap='butt'}else{ctx.lineWidth=Math.max(1.5,0.0028*W)}
      ctx.beginPath();ctx.moveTo(s.p[0][0]*W,s.p[0][1]*H);
      if(s.p.length===1)ctx.lineTo(s.p[0][0]*W+0.1,s.p[0][1]*H);
      for(var i=1;i<s.p.length;i++)ctx.lineTo(s.p[i][0]*W,s.p[i][1]*H);ctx.stroke();ctx.restore()});
  }
  function renderPage(w){
    var z=String(N.zoom);if(w.dataset.done===z)return;w.dataset.done=z;var tok=N.tok;
    N.doc.getPage(+w.dataset.n).then(function(pg){
      if(tok!==N.tok)return;
      var v1=pg.getViewport({scale:1});w.dataset.r=v1.height/v1.width;sizePage(w);
      var dpr=Math.min(window.devicePixelRatio||1,2),vp=pg.getViewport({scale:(N.base*N.zoom/v1.width)*dpr});
      var c=document.createElement('canvas');c.className='pdf';c.width=vp.width;c.height=vp.height;
      return pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise.then(function(){
        if(tok!==N.tok||w.dataset.done!==z)return;
        var old=w.querySelector('canvas.pdf');if(old)old.remove();w.insertBefore(c,w.firstChild);
        var a=w.querySelector('canvas.ann');if(!a){a=document.createElement('canvas');a.className='ann';w.insertBefore(a,c.nextSibling);bindDraw(a,w)}
        a.width=vp.width;a.height=vp.height;drawAnn(w);
      });
    });
  }
  function openDoc(url,file,label){
    N.url=url;N.file=file;N.tok={};N.mode='width';N.ann=loadAnn();N.undo=[];N.zoom=1;N.doc=null;
    plabel.innerHTML=label;pview.innerHTML='';pst.textContent='Loading notes…';updZoom();
    if(N.obs)N.obs.disconnect();
    var tok=N.tok;
    loadPdfjs().then(function(lib){return lib.getDocument(url).promise}).then(function(doc){
      if(tok!==N.tok)return;N.doc=doc;N.base=Math.max(260,pview.clientWidth-18);
      return doc.getPage(1).then(function(p1){
        var v=p1.getViewport({scale:1}),r=v.height/v.width;
        N.obs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)renderPage(e.target)})},{root:pview,rootMargin:'800px 0px'});
        for(var i=1;i<=doc.numPages;i++){var d=document.createElement('div');d.className='npage';d.dataset.n=i;d.dataset.r=r;sizePage(d);
          var pn=document.createElement('span');pn.className='pn';pn.textContent=i+' / '+doc.numPages;d.appendChild(pn);pview.appendChild(d);N.obs.observe(d)}
        pst.textContent=doc.numPages+' pages · Ctrl/⌘ + scroll or pinch to zoom · marks are saved in this browser.';
      });
    }).catch(function(){if(tok===N.tok)pst.textContent='The notes could not be displayed in this view. Use ⬇ PDF or the "Open in new tab" link.'});
  }
  function updZoom(){pzoom.textContent=Math.round(N.zoom*100)+'%'}
  function setZoom(z,force){
    z=Math.min(3,Math.max(0.25,z));if(!N.doc||(z===N.zoom&&!force))return;
    var fy=pview.scrollTop/(pview.scrollHeight||1),fx=pview.scrollLeft/(pview.scrollWidth||1);
    N.zoom=z;updZoom();
    pages().forEach(function(w){sizePage(w);w.dataset.done='';N.obs.unobserve(w);N.obs.observe(w)});
    pview.scrollTop=fy*pview.scrollHeight;pview.scrollLeft=fx*pview.scrollWidth;
  }
  // fit the whole current page inside the frame, keeping that page in view
  function fitPage(){
    var p1=pview.querySelector('.npage');if(!p1)return;
    var top=pview.getBoundingClientRect().top,cur=p1,bt=1e9;
    pages().forEach(function(w){var d=Math.abs(w.getBoundingClientRect().top-top);if(d<bt){bt=d;cur=w}});
    var z=(pview.clientHeight-22)/(N.base*(+cur.dataset.r));setZoom(Math.round(z*100)/100,true);
    pview.scrollTop=cur.offsetTop-pview.offsetTop-8;
  }
  [].forEach.call(pane.querySelectorAll('[data-z]'),function(b){b.addEventListener('click',function(){
    var k=b.dataset.z;if(k==='fit'){N.mode='width';return setZoom(1)}
    if(k==='page'){N.mode='page';return fitPage()}
    N.mode=null;
    var nz=k==='+'?ZOOMS.filter(function(z){return z>N.zoom+0.001})[0]:ZOOMS.filter(function(z){return z<N.zoom-0.001}).pop();if(nz)setZoom(nz);
  })});
  pview.addEventListener('wheel',function(e){if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();N.mode=null;setZoom(Math.round((N.zoom*Math.exp(-e.deltaY*0.0025))*100)/100)},{passive:false});
  // tools
  function setTool(t){N.tool=t;[].forEach.call(pane.querySelectorAll('[data-tool]'),function(b){b.setAttribute('aria-pressed',b.dataset.tool===t)});pview.classList.toggle('drawing',t!=='hand')}
  [].forEach.call(pane.querySelectorAll('[data-tool]'),function(b){b.addEventListener('click',function(){setTool(b.dataset.tool)})});
  [].forEach.call(pane.querySelectorAll('.sw'),function(b){b.addEventListener('click',function(){N.color=b.dataset.c;[].forEach.call(pane.querySelectorAll('.sw'),function(x){x.setAttribute('aria-pressed',x===b)});if(N.tool==='hand'||N.tool==='erase')setTool('pen')})});
  function pt(c,e){var r=c.getBoundingClientRect();return [(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height]}
  function eraseAt(w,c,p){
    var list=N.ann[w.dataset.n]||[],r=c.getBoundingClientRect(),tol=14/r.width,ar=r.height/r.width,hit=false;
    for(var i=list.length-1;i>=0;i--){if(list[i].p.some(function(q){var dx=q[0]-p[0],dy=(q[1]-p[1])*ar;return dx*dx+dy*dy<tol*tol})){N.undo.push({n:w.dataset.n,s:list[i],erased:true});list.splice(i,1);hit=true}}
    if(hit){drawAnn(w);saveAnn()}
  }
  function bindDraw(c,w){
    var cur=null;
    c.addEventListener('pointerdown',function(e){if(N.tool==='hand')return;e.preventDefault();c.setPointerCapture(e.pointerId);
      if(N.tool==='erase'){cur={erase:true};eraseAt(w,c,pt(c,e));return}
      cur={t:N.tool,c:N.tool==='hl'&&N.color==='#111111'?'#facc15':N.color,p:[pt(c,e)]};drawAnn(w,cur)});
    c.addEventListener('pointermove',function(e){if(!cur)return;var p=pt(c,e);if(cur.erase)return eraseAt(w,c,p);
      var l=cur.p[cur.p.length-1];if(Math.abs(p[0]-l[0])+Math.abs(p[1]-l[1])>0.0015){cur.p.push(p);drawAnn(w,cur)}});
    function end(){if(!cur)return;if(!cur.erase){var n=w.dataset.n;(N.ann[n]=N.ann[n]||[]).push(cur);N.undo.push({n:n,s:cur});saveAnn();drawAnn(w)}cur=null}
    c.addEventListener('pointerup',end);c.addEventListener('pointercancel',end);
  }
  document.getElementById('npundo').addEventListener('click',function(){
    var u=N.undo.pop();if(!u)return;var list=N.ann[u.n]=N.ann[u.n]||[];
    if(u.erased)list.push(u.s);else{var i=list.indexOf(u.s);if(i>=0)list.splice(i,1)}
    saveAnn();var w=pview.querySelector('.npage[data-n="'+u.n+'"]');if(w)drawAnn(w);
  });
  document.getElementById('npclear').addEventListener('click',function(){
    if(!N.url||!window.confirm('Remove all your marks from this PDF?'))return;
    N.ann={};N.undo=[];saveAnn();pages().forEach(function(w){drawAnn(w)});
  });
  // open / close / follow the selected tab
  function openPane(nb){
    document.body.classList.add('split');pane.hidden=false;
    if(N.url!==nb.dataset.pdf)openDoc(nb.dataset.pdf,nb.dataset.file,nb.dataset.label);
  }
  // full screen and re-layout when the panel changes size
  var fb=document.getElementById('npfull');
  function relayout(){if(!N.doc)return;N.base=Math.max(260,pview.clientWidth-18);if(N.mode==='page')fitPage();else setZoom(N.zoom,true)}
  function setFull(on){pane.classList.toggle('full',on);fb.textContent=on?'⛶ Exit full screen':'⛶ Full screen';setTimeout(relayout,60)}
  fb.addEventListener('click',function(){
    var on=!pane.classList.contains('full');setFull(on);
    try{if(on&&pane.requestFullscreen)pane.requestFullscreen().catch(function(){});else if(!on&&document.fullscreenElement)document.exitFullscreen().catch(function(){})}catch(e){}
  });
  document.addEventListener('fullscreenchange',function(){if(!document.fullscreenElement&&pane.classList.contains('full'))setFull(false);else setTimeout(relayout,60)});
  var rz=null;window.addEventListener('resize',function(){clearTimeout(rz);rz=setTimeout(relayout,200)});
  function closePane(){if(pane.classList.contains('full')){setFull(false);try{if(document.fullscreenElement)document.exitFullscreen()}catch(e){}}document.body.classList.remove('split');pane.hidden=true;try{localStorage.setItem('enn582v2split','0')}catch(e){}}
  document.getElementById('npclose').addEventListener('click',closePane);
  document.getElementById('npdl').addEventListener('click',function(){if(N.url)download(N.url,N.file,pst,this)});
  function follow(){if(pane.hidden)return;var p=[].filter.call(document.querySelectorAll('[data-panel]'),function(x){return !x.hidden})[0];var nb=p&&p.querySelector('.notes');if(nb)openPane(nb)}
  [].forEach.call(document.querySelectorAll('nav.tabs button,[data-goto]'),function(b){b.addEventListener('click',function(){setTimeout(follow,0)})});
  window.addEventListener('hashchange',function(){setTimeout(follow,0)});
  [].forEach.call(document.querySelectorAll('.notes'),function(nb){
    nb.querySelector('.nside').addEventListener('click',function(){openPane(nb);try{localStorage.setItem('enn582v2split','1')}catch(e){}});
    nb.querySelector('.ndl').addEventListener('click',function(){download(nb.dataset.pdf,nb.dataset.file,nb.querySelector('.nstat'),this)});
  });
  try{if(localStorage.getItem('enn582v2split')==='1'&&window.innerWidth>=900){pane.hidden=false;follow();if(!N.url)closePane()}}catch(e){}
'''
sub1('  // plan checkboxes', js + '\n  // plan checkboxes')
open(f, 'w').write(h)
print('notes ok', len(h))
