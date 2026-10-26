# Wraps the artifact page (src/v2 build output) into a standalone index.html for GitHub Pages.
import sys
src, out = sys.argv[1], sys.argv[2]
body = open(src).read()
shim = """<script>
/* Outside claude.ai there is no window.claude: provide a tiny stand-in so the
   cheatsheet button downloads the PDF with a normal browser download. */
if(!window.claude){window.claude={use:function(n){return Promise.resolve(n==='downloads'?{save:function(o){
  var u=URL.createObjectURL(o.data),a=document.createElement('a');a.href=u;a.download=o.filename;
  document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},4000);return Promise.resolve();}}:null)}};}
</script>
"""
html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<style>*,*::before,*::after{box-sizing:border-box}html,body{margin:0}</style>\n'
        + shim + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open(out, 'w').write(html)
print('wrote', out, len(html))
