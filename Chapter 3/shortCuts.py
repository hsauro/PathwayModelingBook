import tellurium as te     
r = te.loada ('''          
   J1: A -> B; k1*A - k2*B;
   J2: B -> C; k3*B - k4*C;
   k1 = 0.1; k2 = 0.02;    
   k3 = 0.3; k4 = 0.04;    
   A  = 10;  B  = 0; C = 0;
''')                       
print (r.sm())               
print (r.rs())               
print (r.fs())    
