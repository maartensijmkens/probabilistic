from problog.program import PrologString
from problog.cnf_formula import CNF
from create_cnf_file import create_cnf_file

# load the program
p = PrologString(open("program_grounded.pl").read())

# convert to CNF  
cnf = CNF.create_from(p) 
weights = {k: (float(w), 1-float(w)) for k, w in cnf._weights.items()}

query1 = []
query2 = []

# add the query clause and put weights of conditionals on (1,0)
for name, atom in cnf.get_names():
    if str(name) == "smokes(a)":
        query1.append([atom])
    if str(name) == "friends(a,b)" or str(name) == "friends(a,c)":
        query1.append([atom])
        query2.append([atom])

create_cnf_file(cnf._clauses + query1, weights, cnf._atomcount, "program_cond1.cnf")
create_cnf_file(cnf._clauses + query2, weights, cnf._atomcount, "program_cond2.cnf")