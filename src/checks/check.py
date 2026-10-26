import numpy as np
# machine G/B example
P={0:np.array([[.7,.3],[0,1]]),1:np.array([[.9,.1],[.6,.4]])}
g={0:np.array([0,5.]),1:np.array([2,7.])}
a=.9
V=np.zeros(2)
for k in range(3):
    c=[g[u]+a*P[u]@V for u in (0,1)]; V=np.minimum(*c); print('VI',k+1,V,np.argmin(c,0))
for _ in range(300):
    c=[g[u]+a*P[u]@V for u in (0,1)]; V=np.minimum(*c)
print('VI conv',V,np.argmin(c,0))
mu=np.array([0,0])
for it in range(5):
    Pm=np.array([P[mu[i]][i] for i in range(2)]); gm=np.array([g[mu[i]][i] for i in range(2)])
    J=np.linalg.solve(np.eye(2)-a*Pm,gm)
    c=np.array([g[u]+a*P[u]@J for u in (0,1)]); new=np.argmin(c,0)
    print('PI',it,mu,J,c.T,new)
    if (new==mu).all(): break
    mu=new
# finite horizon N=2
J=np.zeros(2)
for k in (1,0):
    c=[g[u]+P[u]@J for u in (0,1)]; J=np.minimum(*c); print('FH J',k,J,np.argmin(c,0))
# rover inf PI check
P={0:np.array([[.75,.25,0],[0,0,1],[0,0,1]]),1:np.array([[.8,.2,0],[.9,0,.1],[0,.1,.9]])}
g={0:np.array([-3,0,0.]),1:np.array([-1,2,2.])}
for a in (.9,.96):
  V=np.zeros(3)
  for _ in range(3000):
    c=[g[u]+a*P[u]@V for u in (0,1)]; V=np.minimum(*c)
  print('rover',a,V,np.argmin(c,0))
# Sarsa exam
Q={}
d,al=.1,.5
R={(1,'A'):0,(1,'B'):0,(2,'A'):100,(2,'B'):-1,(3,'A'):0,(3,'B'):100,(4,'A'):-1,(4,'B'):100}
for ep in [[(1,'A'),(2,'A'),(4,'B'),(4,'B')],[(1,'B'),(3,'A'),(2,'A'),(4,'B')]]:
  for i in range(len(ep)-1):
    s,u=ep[i]; s2,u2=ep[i+1]
    old=Q.get((s,u),0); Q[(s,u)]=old+d*(R[(s,u)]+al*Q.get((s2,u2),0)-old)
    print(ep[i],'->',ep[i+1],round(Q[(s,u)],4))
print(Q)
# LS
Phi=np.array([[1,0],[1,1],[1,2.]]); b=np.array([1,3,7.]); print(np.linalg.solve(Phi.T@Phi,Phi.T@b))
