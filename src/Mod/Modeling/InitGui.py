import sys
with open(Dir + '/Common/Init.py', 'r') as f1:
    s1 = f1.read()
    exec(s1)

with open(Dir + '/Modeling2D/InitGui2D.py', 'r') as f1:
    s1 = f1.read()
    exec(s1)

