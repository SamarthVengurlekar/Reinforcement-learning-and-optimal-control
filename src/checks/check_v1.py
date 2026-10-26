import numpy as np, itertools, math
print("== P2 DP ==")
g={'A':{'B':333,'C':282,'D':230},'B':{'E':553,'F':280,'G':370},'C':{'E':470,'F':404,'G':522},'D':{'E':268,'F':606,'G':767},'E':{'H':807},'F':{'H':450},'G':{'H':603}}
J={'H':0}
for n in ['E','F','G','B','C','D','A']:
    vals={m:c+J[m] for m,c in g[n].items()}; J[n]=min(vals.values()); print(n,vals,J[n])
for b in 'BCD':
    for e in 'EFG': print('A'+b+e+'H', g['A'][b]+g[b][e]+g[e]['H'])
print("== TSP ==")
def tsp(C):
    n='ABCD'; res={}
    for p in itertools.permutations('BCD'):
        t='A'+''.join(p)+'A'; res[t]=sum(C[t[i]+t[i+1]] for i in range(4))
    return res
def mk(ab):
    d={'AB':ab,'AC':1,'AD':15,'BC':20,'BD':4,'CD':3}; C={}
    for k,v in d.items(): C[k]=v; C[k[::-1]]=v
    return C
C=mk(5); print(tsp(C)); C2=mk(50); print(tsp(C2))
def nn(C,path):
    path=list(path)
    while len(path)<4:
        cur=path[-1]; rem=[c for c in 'ABCD' if c not in path]
        path.append(min(rem,key=lambda c:C[cur+c]))
    path.append('A'); return path, sum(C[path[i]+path[i+1]] for i in range(4))
print('NN',nn(C,'A'),nn(C2,'A'))
for f in 'BCD': print('rollout A->',f, nn(C2,'A'+f))
for f in 'BD': print('rollout AC->',f, nn(C2,'AC'+f))
for f in 'CD': print('rollout AB->',f, nn(C2,'AB'+f))
print("== P3 B ==")
JF,JG=450,603
JB=min(553+JF,280+JG);JC=min(470+JF,404+JG);JD=min(268+JF,606+JG);JE=min(807+JF,370+JG)
print(JB,JC,JD,JE, 'East',0.6*(333+JB)+0.4*(282+JC),'West',0.8*(230+JD)+0.2*(300+JE))
print("== parking ==")
def park(N,c,S,rho,s=None):
    s=s or (lambda k:N-k); V=np.zeros((N+1,2)); V[N]=S; pol=['']*N
    for k in range(N-1,-1,-1):
        d=c+rho*V[k+1][0]+(1-rho)*V[k+1][1]; V[k]=[min(s(k),d),d]; pol[k]='park' if s(k)<=d else 'drive'
    return V,pol
V,p=park(10,1,10,0.1); print(V[:,1].round(4),p)
V,p=park(3,0.4,3,0.5); print(V,p)
print("== frozen lake slippery ==")
desc=["SFFF","FHFH","FFFH","HFFG"]
nS=16
def step(s,a):
    r,c=divmod(s,4)
    if a==0: c=max(c-1,0)
    elif a==1: r=min(r+1,3)
    elif a==2: c=min(c+1,3)
    else: r=max(r-1,0)
    return r*4+c
def P(s,a,slip):
    if desc[s//4][s%4] in 'GH': return [(1.0,s,0)]
    acts=[(a-1)%4,a,(a+1)%4] if slip else [a]
    out=[]
    for b in acts:
        ns=step(s,b); out.append((1/len(acts),ns,1.0 if desc[ns//4][ns%4]=='G' else 0.0))
    return out
for slip in [False,True]:
    V=np.zeros(nS); it=0
    while True:
        it+=1; d=0
        for s in range(nS):
            v=V[s]; V[s]=max(sum(p*(r+.99*V[ns]) for p,ns,r in P(s,a,slip)) for a in range(4)); d=max(d,abs(v-V[s]))
        if d<1e-5: break
    print(slip,it,V.reshape(4,4).round(4))
    if slip:
        for a in range(4): print('s14 a',a,sum(p*(r+.99*V[ns]) for p,ns,r in P(14,a,True)))
        for a in range(4): print('s0 a',a,sum(p*(r+.99*V[ns]) for p,ns,r in P(0,a,True)))
print(0.99**5)
print("== P5 ==")
grid=np.array([[0,0,-10,0],[0,0,0,0],[0,-10,0,0],[0,0,-10,1]])
h=lambda i,j:-math.hypot(3-i,3-j)
mv={'up':(-1,0),'down':(1,0),'left':(0,-1),'right':(0,1)}
for (i,j) in [(2,0),(3,0),(3,1)]:
    out={}
    for a,(di,dj) in mv.items():
        ni,nj=i+di,j+dj
        if 0<=ni<4 and 0<=nj<4: out[a]=round(grid[ni,nj]-1+h(ni,nj),3)
    print((i,j),out)
def phi(s):
    v=np.array([s[0],s[1],abs(s[0]-4)+abs(s[1]-4)],float); return v/v.sum()
print(phi((1,1)), phi((0,0)) if False else '', [ (i,j,i+j+abs(i-4)+abs(j-4)) for i in range(5) for j in range(5)][:3])
r=np.array([10,10,2.]); print([[round(r@phi((i,j)),3) if (i,j)!=(0,0) else 'nan' for j in range(5)] for i in range(5)])
r=np.zeros(3); f=phi((1,1)); tgt=max(-1+r@phi(n) for n in [(0,1),(2,1),(1,0),(1,2)]); r=r-0.01*f*(r@f-tgt); print('sgd',r)
print("== cliff update ==")
q=-2; print('sarsa',q+0.5*((-1+0.99*-100)-q),'ql',q+0.5*((-1+0.99*-1)-q))
print("== mock Q3 ==")
# states 1 start,2 edge,3 upper,5 upper2,4 goal
T={(1,'A'):(2,-1),(1,'B'):(3,-1),(2,'A'):(4,-1),(2,'B'):(1,-100),(3,'A'):(5,-1),(3,'B'):(1,-1),(5,'A'):(4,-1),(5,'B'):(3,-1)}
eps=[[(1,'A'),(2,'B'),(1,'A'),(2,'A')],[(1,'B'),(3,'A'),(5,'A')]]
for algo in ['sarsa','q']:
    Q={(s,a):0.0 for s in [1,2,3,4,5] for a in 'AB'}
    for ep in eps:
        for t,(s,a) in enumerate(ep):
            ns,r=T[(s,a)]
            if ns==4: tgt=r
            elif algo=='sarsa': tgt=r+0.9*Q[ep[t+1]]
            else: tgt=r+0.9*max(Q[(ns,'A')],Q[(ns,'B')])
            old=Q[(s,a)]; Q[(s,a)]=old+0.5*(tgt-old)
            print(algo,(s,a,r,ns),'target',round(tgt,4),'Q',old,'->',round(Q[(s,a)],4))
    print(algo,{k:round(v,4) for k,v in Q.items() if v})
