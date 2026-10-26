import re, sys
f = sys.argv[1]
V = {
 'mpc': [('8U0xiOkDcmw','4:50','MATLAB · Understanding MPC, part 1','Why use Model Predictive Control?'),
         ('9OYWiuefK14','7:13','The Control Eng GEEK','MPC part 1: the receding horizon')],
 'ddp': [('_zE5z-KZGRw','9:25','CSBreakdown','Principle of optimality'),
         ('eGNRlhSIeWM','11:26','Worked example','Multi-stage shortest path, backward approach (like Tom\'s journey)')],
 'sdp': [('4Fqt2Nk2lhY','3:36','Cyrill Stachniss · 5 Minutes with Cyrill','Markov Decision Process (MDP)'),
         ('XKZIsODur_g','7:44','SmartSlides','MDPs: expected return, policy and value functions')],
 'ihdp': [('raSia5MpwUQ','4:58','DRL course 4.6','Generalized policy iteration: evaluate ↔ improve'),
          ('gThGerajccM','0:33','Aaron Becker · demo','Value iteration solving a robot grid world (watch the values spread)')],
 'adp': [('Ru-9pJJyggo','4:27','Standarity','Monte Carlo tree search: lookahead + rollouts (how AlphaGo plans)'),
         ('g6EBIr0uRr0','13:14','Gerstner Lab (EPFL) · RL3.1','Too many states? Why we approximate the value function')],
 'rl': [('UWiIxWy5kD8','4:05','Gerstner Lab (EPFL) · RL2.2','Q-learning and variations of SARSA'),
        ('Ii7GJDB3r0Q','7:16','Gerstner Lab (EPFL) · RL2.3','TD learning (temporal difference)')],
}
s = open(f).read()
def rep(m):
    key = m.group(1); body = m.group(2)
    cards = ''.join('\n    <div class="vid" data-yt="%s"><span class="vsrc">%s · <b class="vlen">%s</b></span><b>%s</b></div>' % v for v in V[key])
    body = re.sub(r'<div class="vids">.*?\n  </div>', '<div class="vids">' + cards + '\n  </div>', body, flags=re.S)
    return '<!--ELI:%s-->%s<!--/ELI-->' % (key, body)
s, n = re.subn(r'<!--ELI:(\w+)-->(.*?)<!--/ELI-->', rep, s, flags=re.S)
open(f, 'w').write(s); print(n, s.count('class="vid"'))
