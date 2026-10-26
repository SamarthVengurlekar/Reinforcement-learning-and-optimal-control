T={(1,'A'):(2,-1),(1,'B'):(3,-1),(2,'A'):(4,-1),(2,'B'):(1,-100),(3,'A'):(5,-1),(3,'B'):(1,-1),(5,'A'):(4,-1),(5,'B'):(3,-1)}
eps=[[(1,'A'),(2,'B'),(1,'B'),(3,'A'),(5,'A')],[(1,'A'),(2,'B'),(1,'A'),(2,'A')]]
for algo in ['sarsa','q']:
    Q={(s,a):0.0 for s in [1,2,3,5] for a in 'AB'}
    for e,ep in enumerate(eps):
        for t,(s,a) in enumerate(ep):
            ns,r=T[(s,a)]
            if ns==4: tgt=r; how='terminal'
            elif algo=='sarsa': tgt=r+0.9*Q[ep[t+1]]; how=f"Q{ep[t+1]}={Q[ep[t+1]]:.4f}"
            else: m=max(Q[(ns,'A')],Q[(ns,'B')]); tgt=r+0.9*m; how=f"maxQ({ns})={m:.4f}"
            old=Q[(s,a)]; Q[(s,a)]=old+0.5*(tgt-old)
            print(algo,'ep',e+1,(s,a,r,ns),how,'target',round(tgt,4),old,'->',round(Q[(s,a)],4))
    print(algo,{k:round(v,4) for k,v in Q.items()})
