import sys, pymupdf
S=sys.argv[1]
html=open(S+'/cs_full.html').read()
css='''
@font-face{font-family:U;src:url("Arial Unicode.ttf");}
@font-face{font-family:U;font-weight:bold;src:url("Arial Bold.ttf");}
*{font-family:U;}
body{font-size:8.6pt;line-height:1.3;color:#111;}
h1{font-size:11pt;margin:0 0 3pt 0;color:#0b4f73;}
h2{font-size:9.6pt;margin:4pt 0 1.5pt 0;padding:1pt 2pt;background-color:#e3edf3;color:#0b4f73;}
p{margin:0 0 2.2pt 0;text-align:left;}
b{font-weight:bold;}
sub,sup{font-size:6.3pt;}
'''
arch=pymupdf.Archive("/System/Library/Fonts/Supplemental")
story=pymupdf.Story(html=html,user_css=css,archive=arch)
W,H=pymupdf.paper_size("a4")
m=20; gap=12; cw=(W-2*m-gap)/2
rects=[]
def rectfn(rect_num, filled):
    col=rect_num%2
    r=pymupdf.Rect(m+col*(cw+gap), m, m+col*(cw+gap)+cw, H-m)
    return pymupdf.Rect(0,0,W,H), r, None
writer=pymupdf.DocumentWriter(S+'/cheatsheet.pdf')
n=0
more=1
while more:
    if n%2==0: dev=writer.begin_page(pymupdf.Rect(0,0,W,H))
    col=n%2
    r=pymupdf.Rect(m+col*(cw+gap), m, m+col*(cw+gap)+cw, H-m-10)
    more,_=story.place(r)
    story.draw(dev)
    n+=1
    if n%2==0 or not more: writer.end_page()
writer.close()
d=pymupdf.open(S+'/cheatsheet.pdf')
print('pages',len(d))
for i,p in enumerate(d):
    p.insert_text((W/2-60,H-10),f"ENN582 cheatsheet · page {i+1}/{len(d)}",fontsize=6,color=(.4,.4,.4))
    p.get_pixmap(dpi=110).save(f"{S}/cs{i+1}.png")
d.saveIncr()
