import tellurium as te

r = te.loada ('''
    // Transcription binding/unbinding step
    TR + Gene1 -> TR_B; k1*TR*Gene1;
    TR_B -> TR + Gene1; k2*TR_B;
    // Protein synthesis
    $g -> product; Vm*TR_B;
    // Protein degradation
    product -> $w; k3*product;

    // TR = free transcription factor;
    // TR_B = bound transcription factor
    Gene1 = 1;  TR = 1;     Vm = 1;
    k1 = 0.01; k2 = 0.01;  k3 = 0.04;
    TR_B = 0;  product = 0;
''')

seed = 1.22012
m = r.gillespie(0, 2000, ["time", "TR_B", "product"], seed)
r.plot()
