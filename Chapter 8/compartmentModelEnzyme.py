import tellurium as te
import pylab

r = te.loada ('''
    compartment V1, V2, V3;
    var S1 in V1, S2 in V2, S3 in V3;
    S1 -> S2; A*k1*(S1-S2/Keq)/(1 + S1/Km1 + S2/Km2);
    S2 -> S3; A*k2*(S2-S3/Keq)/(1 + S2/Km1 + S3/Km2);

    V1 = 100; V2 = 10; V3 = 1;
    S1 = 10;
    A = 1; k1 = 100; k2 = 25;
    Km1 = 0.5; Km2 = 0.5;
    Keq = 1;
''')

result = r.simulate(0, 20, 100);
r.plot(xlim=(0,20),ylim=(0,15))
print ("Total Mass = ", r.S1*r.V1 + r.S2*r.V2 + r.S3*r.V3);
