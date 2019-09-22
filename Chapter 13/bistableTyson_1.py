import tellurium as te

r = te.loada ('''
    $X -> R1;  k1*EP + k2*Signal;
    R1 -> $w;  k3*R1;
    EP -> E;   Vm1*EP/(Km + EP);
    E -> EP;   ((Vm2+R1)*E)/(Km + E);

    Vm1 = 12; Vm2 = 6;
    Km = 0.6;
    k1 = 1.6; k2 = 4;
    E = 5; EP = 15;
    k3 = 3; Signal = 0.1;
''')

result = r.simulate(0, 40, 500)
r.plot()
