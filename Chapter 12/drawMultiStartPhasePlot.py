# Plot a phase portrait for a simple species species pathway
import tellurium as te
import  matplotlib.pyplot as plt

rr = te.loada ('''
    $Xo -> S1;  k1*Xo;
    S1 -> S2;   k2*S1;
    S2 -> $X1;  k3*S2;
    k1 = 0.6; Xo = 1;
    k2 = 0.4; k3 = 0.8;
''')

plt.figure(figsize=(9,4))
S1Start = 0
S2Start = 0
for i in range(1, 11):
    rr.S1 = S1Start
    rr.S2 = S2Start
    m = rr.simulate(0, 10, 120, ["S1", "S2"])
    p = te.plotArray(m, show=False)
    plt.setp (p, color='r')
    S1Start = S1Start + 0.2
S1Start = 2
S2Start = 0
for i in range(1, 11):
    rr.S1 = S1Start
    rr.S2 = S2Start
    m = rr.simulate(0, 10, 120, ["S1", "S2"])
    p = te.plotArray(m, show=False)
    plt.setp (p, color='r')
    S2Start = S2Start + 0.2
S2Start = 0
S1Start = 0
for i in range(1, 11):
    rr.S1 = S1Start
    rr.S2 = S2Start
    m = rr.simulate(0, 10, 120, ["S1", "S2"])
    p = te.plotArray(m, show=False)
    plt.setp (p, color='r')
    S2Start = S2Start + 0.2
S1Start = 0
S2Start = 2
for i in range(1, 11):
    rr.S1 = S1Start
    rr.S2 = S2Start
    m = rr.simulate(0, 10, 120, ["S1", "S2"])
    p = te.plotArray(m, show=False)
    plt.setp (p, color='r')
    S1Start = S1Start + 0.2
plt.xlim ([0, 2])
plt.ylim ([0, 2])
plt.xlabel ('S1', fontsize=16)
plt.ylabel ('S2', fontsize=16)
plt.savefig ("plot.pdf")
plt.show()
