import tellurium as te

r = te.loada ('''
    J0:  $src -> X;    k1*S;
    J1:  X -> R;       (kop + ko*EP)*X;
    J2:  R -> $waste;  k2*R;
    J3:  E -> EP;      Vmax_1*R*E/(Km_1 + E);
    J4:  EP -> E;      Vmax_2*EP/(Km_2 + EP);

    src = 0;      kop = 0.01;
    ko =  0.4;    k1 = 1;
    k2 = 1;       R = 1;
    EP = 1;       S = 0.2;
    Km_1 = 0.05;  Km_2 = 0.05;
    Vmax_2 = 0.3; Vmax_1 = 1;
    KS4 = 0.5;
''')

result = r.simulate(0, 500, 1000)
r.plot()
