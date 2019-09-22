import tellurium as te

r = te.loada ('''
    ProA -> A + ProA; g*ProA;
    ProB -> B + ProB; g*ProB;
    A + ProB -> ProBA; a0*A*ProB;
    B + ProA -> ProAB; a0*B*ProA;
    ProBA -> ProB + A; a1*ProBA;
    ProAB -> ProA + B; a1*ProAB;
    A -> $w; d*A;
    B -> $w; d*B;
    ProAB -> ProA; d*ProAB;
    ProBA -> ProB; d*ProBA;

    g = 0.2;   d = 0.005;
    a0= 0.3;   a1 = 0.01;
    A = 0;     B = 0;
    ProA = 1;  ProB = 1;
''')

result = r.gillespie(0, 2000000, ["Time", "A"]);
r.plot()
