import tellurium as te
import matplotlib.pyplot as plt
import roadrunner

rr = te.loada ('''
   A -> B; k1*A;
   B -> A; k2*B;
   k1 = 0.2; k2 = 0.4;
''')

starting = 6000 # 10 zepto molar 10^(-21) = 6000 molecules

rr.model["init(A)"] = starting
rr.model["init(B)"] = 0

plt.subplot(221)
plt.title("A = 6000")
m1 = rr.gillespie(0, 12, ["time", "A", "B"])
te.plotArray(m1)
rr.model["init(A)"] = starting
rr.model["init(B)"] = 0

m2 = rr.simulate(0, 12, 100)
te.plotArray(m2)

starting = 600
rr.model["init(A)"] = starting
rr.model["init(B)"] = 0

plt.subplot(222)
plt.title("A = 600")
m1 = rr.gillespie(0, 12, ["time", "A", "B"])
te.plotArray(m1)
rr.model["init(A)"] = starting


rr.model["init(B)"] = 0
m2 = rr.simulate(0, 12, 100)
te.plotArray(m2)

starting = 60
rr.model["init(A)"] = starting
rr.model["init(B)"] = 0

plt.subplot(223)
plt.title("A = 60")
m1 = rr.gillespie(0, 12, ["time", "A", "B"])
te.plotArray(m1)
rr.model["init(A)"] = starting
rr.model["init(B)"] = 0

m2 = rr.simulate(0, 12, 100)
te.plotArray(m2)
plt.xlabel("Time")
starting = 20
rr.model["init(A)"] = starting
rr.model["init(B)"] = 0

plt.subplot (224)
plt.title("A = 20")
m1 = rr.gillespie(0, 12, ["time", "A", "B"])
te.plotArray(m1)
rr.model["init(A)"] = starting
rr.model["init(B)"] = 0

m2 = rr.simulate(0, 12, 100)
plt.xlabel("Time")
te.plotArray(m2)
