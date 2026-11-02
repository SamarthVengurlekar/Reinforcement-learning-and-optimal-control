# Verifies the numbers in mock papers B and C (src/v1/mock.html)
import numpy as np, sympy as sp, itertools
print('=== B Q1 batch MPC ===')
a,b=0.9,0.5; Q,QF,R=1,2,0.1; x0=2
Lam=np.array([[a],[a*a]]); Phi=np.array([[b,0],[a*b,b]]); Qb=np.diag([Q,QF]); Rb=R*np.eye(2)
M=Phi.T@Qb@Phi+Rb; F=Phi.T@Qb@Lam
print('Lam',Lam.ravel(),'Phi',Phi.tolist()); print('PhiTQPhi+R',M.tolist(),'PhiTQLam',F.ravel())
H=2*M; f=2*F*x0; print('H',H.tolist(),'f',f.ravel())
U=-np.linalg.solve(M,F*x0); print('U*',U.ravel())
X=Lam*x0+Phi@U; print('X',X.ravel())
Jq=lambda U:(U@Rb@U+(Lam.ravel()*x0+Phi@U)@Qb@(Lam.ravel()*x0+Phi@U))
best=min(((Jq(np.array([u0,u1])),u0,u1) for u0 in np.linspace(-1,1,401) for u1 in np.linspace(-1,1,401)))
print('constrained grid best',best)
# KKT: u0=-1 active, optimise u1
u1=sp.symbols('u1'); Jc=sp.expand(Jq(np.array([-1,u1],dtype=object))); s=sp.solve(sp.diff(Jc,u1),u1)[0]; print('u1|u0=-1',s,float(s),'J',float(Jc.subs(u1,s)))
print('grad at (-1,-1):',[float(v) for v in sp.Matrix([Jq(np.array([sp.Symbol('p'),sp.Symbol('q')],dtype=object))]).jacobian([sp.Symbol('p'),sp.Symbol('q')]).subs({sp.Symbol('p'):-1,sp.Symbol('q'):-1})])
lam=-(sp.diff(Jq(np.array([sp.Symbol('u0'),u1],dtype=object)),sp.Symbol('u0'))).subs({sp.Symbol('u0'):-1,u1:s}); print('dJ/du0 at sol',float(-lam))
print('=== B Q2 stochastic LQ ===')
x,u=sp.symbols('x u',real=True); r,sg=sp.symbols('r sigma',positive=True)
J2=x**2
J1=sp.simplify(x**2+sp.Min(0,0)+0) # placeholder
def step(Jn):
    # E[Jn(x+u+w)] for Jn=c x^2+d: c((x+u)^2+s^2)+d
    c=sp.Poly(sp.expand(Jn),x).coeff_monomial(x**2); d=sp.expand(Jn).subs(x,0)
    e=x**2+r*u**2+c*((x+u)**2+sg**2)+d
    us=sp.solve(sp.diff(e,u),u)[0]; return sp.simplify(e.subs(u,us)),sp.simplify(us)
J1,u1s=step(J2); J0,u0s=step(J1)
print('J1',sp.factor(J1),'mu1',u1s); print('J0',sp.simplify(J0),'mu0',u0s)
print('r=1: J1',sp.expand(J1.subs(r,1)),'J0',sp.expand(J0.subs(r,1)),'mu0',u0s.subs(r,1),'mu1',u1s.subs(r,1))
print('sigma^2 for J0(1)=2.6:',sp.solve(sp.Eq(J0.subs({r:1,x:1}),sp.Rational(26,10)),sg))
print('=== B Q3 Q-learning ===')
T={(1,'A'):(2,-1),(1,'B'):(3,2),(2,'A'):(4,5),(2,'B'):(3,-2),(3,'A'):(2,1),(3,'B'):(4,3)}
eps=[[(1,'A'),(2,'B'),(3,'B')],[(1,'B'),(3,'A'),(2,'A')]]
d,al=0.1,0.5
for algo in ['q','sarsa']:
    Qt={k:0.0 for k in T}
    for e,ep in enumerate(eps):
        for t,(s_,a_) in enumerate(ep):
            ns,rw=T[(s_,a_)]
            if ns==4: tgt=rw
            elif algo=='sarsa': tgt=rw+al*Qt[ep[t+1]]
            else: tgt=rw+al*max(Qt[(ns,'A')],Qt[(ns,'B')])
            old=Qt[(s_,a_)]; Qt[(s_,a_)]=old+d*(tgt-old)
            print(algo,e+1,(s_,a_,rw,ns),'tgt',round(tgt,5),old,'->',round(Qt[(s_,a_)],5))
    print(algo,{k:round(v,5) for k,v in Qt.items()})
# true Q*
Qs={k:0.0 for k in T}
for _ in range(200):
    for k,(ns,rw) in T.items(): Qs[k]=rw+(0 if ns==4 else al*max(Qs[(ns,'A')],Qs[(ns,'B')]))
print('Q*',Qs)
print('=== C Q2 dropout ===')
G=sp.symbols('Gamma',positive=True)
def stepd(Jn):
    c=sp.Poly(sp.expand(Jn),x).coeff_monomial(x**2); d_=sp.expand(Jn).subs(x,0)
    e=x**2+u**2+c*(G*(x+u)**2+(1-G)*x**2+sg**2)+d_
    us=sp.solve(sp.diff(e,u),u)[0]; return sp.simplify(e.subs(u,us)),sp.simplify(us)
J1d,m1=stepd(x**2); print('J1',sp.simplify(J1d),'mu1',m1)
for g in [1,sp.Rational(1,2),0]: print(' Gamma',g,'J1',sp.expand(J1d.subs(G,g)),'mu1',m1.subs(G,g))
J0d,m0=stepd(J1d); print('Gamma=1/2: J0',sp.expand(J0d.subs(G,sp.Rational(1,2))),'mu0',sp.simplify(m0.subs(G,sp.Rational(1,2))))
print('=== C Q3 VI/PI ===')
al=0.9
P={(1,'a'):(2,[0.8,0.2]),(1,'b'):(0.5,[0.3,0.7]),(2,'a'):(1,[0.6,0.4]),(2,'b'):(3,[0.9,0.1])}
V=np.zeros(2)
for it in range(1,3):
    q={k:g+al*np.dot(p,V) for k,(g,p) in P.items()}
    V=np.array([min(q[(1,'a')],q[(1,'b')]),min(q[(2,'a')],q[(2,'b')])]); print('VI',it,{k:round(v,4) for k,v in q.items()},V)
def evalp(mu):
    Pm=np.array([P[(i+1,mu[i])][1] for i in range(2)]); g=np.array([P[(i+1,mu[i])][0] for i in range(2)])
    return np.linalg.solve(np.eye(2)-al*Pm,g)
mu=('a','a')
for it in range(4):
    Jm=evalp(mu); q={k:g+al*np.dot(p,Jm) for k,(g,p) in P.items()}
    new=tuple(min('ab',key=lambda a_:q[(i+1,a_)]) for i in range(2)); print('PI',mu,Jm,{k:round(v,4) for k,v in q.items()},'->',new)
    if new==mu: break
    mu=new
Vi=np.zeros(2)
for _ in range(2000): Vi=np.array([min(P[(i+1,a_)][0]+al*np.dot(P[(i+1,a_)][1],Vi) for a_ in 'ab') for i in range(2)])
print('J* by VI',Vi)
# TD(0)
J=np.array([6.0,8.0]); g=0.5; J1n=J[0]+0.1*(g+al*J[1]-J[0]); print('TD(0) J(1)',J1n,'TD error',g+al*J[1]-J[0])
print('=== extra ===')
print('J(U*)',Jq(U.ravel()),"J clipped",Jq(np.array([-1,U.ravel()[1]])),"J(-1,-1)",Jq(np.array([-1.,-1.])),'H^-1',np.linalg.inv(H))
print('C Q2 x0=3: Gamma=1',1.5*9,'Gamma=.5',11/6*9)
