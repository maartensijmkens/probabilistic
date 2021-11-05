from problog.program import PrologString
from problog.cnf_formula import CNF
from create_cnf_file import create_cnf_file

# load the program
p = PrologString(open("program_grounded.pl").read())

# convert to CNF  
cnf = CNF.create_from(p)  
weights = {k: (float(w), 1-float(w)) for k, w in cnf._weights.items()}     
   
# add query clause to CNF
for name, atom in cnf.get_names():
    if str(name) == "smokes(a)":
        cnf.add_clause(atom,[])

create_cnf_file(cnf._clauses, weights, cnf._atomcount, "program.cnf")