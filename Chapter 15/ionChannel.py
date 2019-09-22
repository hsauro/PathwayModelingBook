import tellurium as te
import pylab

# Bursting in a simple ion channel model
r = te.loada ('''
    open -> closed; k1*open;
    closed -> open; k2*closed;

    $ligand + open -> closedLigand; k3*ligand*open;
    LigandBlocked -> $ligand + open; k4*LigandBlocked;

    open = 1;
    closed = 0;
    LigandBlocked = 0;
    ligand = 1E-7;
    k1 = 400; k2 = 75;
    k3 = 8E8;
    k4 = 3000;
''')

result = r.gillespie(0, .2, ["time", "open"])
# Plot and set the x and y axes limits
r.plot (xlim=(0,0.1),ylim=(0,2))
