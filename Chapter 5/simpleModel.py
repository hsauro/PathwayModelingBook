import tellurium as te

r = te.loada ('''
    $Xo -> y1; vo;
     y1 -> y2; k1*y1;
     y2 -> $waste; k2*y2;

    vo = 10; k1 = 0.5; k2 = 0.35;
    y1 = 0; y2 = 0;
''')
