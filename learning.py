from problog.program import PrologString
from problog.cnf_formula import CNF
from create_cnf_file import create_cnf_string

from pysdd.sdd import SddManager


program = open("tolearn_tpl.pl").read()
data = open("data.pl").readlines()

query = ["friends(a,b)","friends(a,c)","friends(b,a)","friends(b,c)","friends(c,a)","friends(c,b)"]
query_ids = [0, 0, 0, 0, 0, 0]
query_p = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

evidence = ["stress(a)","stress(b)","stress(c)","smokes(a)","smokes(b)","smokes(c)"]
evidence_ids = [0, 0, 0, 0, 0, 0]

def get_example(i):
    r = [1, 1, 1, 1, 1, 1]
    for i in range(7*i,7*i+6):
        for j,e in enumerate(evidence):
            if "\+"+e in data[i]:
                r[j] = 0
    return r

# load the program
p = PrologString(program)
# convert to CNF  
cnf = CNF.create_from(p) 
weights = {k: (float(w), 1-float(w)) for k, w in cnf._weights.items()}

# retrieve atom ids of predicates
for name, atom in cnf.get_names():
    name = str(name)
    if name in query:
        i = query.index(name)
        query_ids[i] = atom
    if name in evidence:
        i = evidence.index(name)
        evidence_ids[i] = atom

cnf_string = create_cnf_string(cnf._clauses, weights, cnf._atomcount)
sdd, root = SddManager.from_cnf_string(cnf_string)
wmc = root.wmc(log_mode=False)
sdd.set_prevent_transformation(prevent=False)
for i in range(sdd.var_count()):
    lit = sdd.literal(i+1)
    if i+1 in weights:
        wp, wn = weights[i+1]
        wmc.set_literal_weight(lit, wp)
        wmc.set_literal_weight(-lit, wn)


M = 2000
episodes = 100
eps = 0.01

for epoch in range(episodes):

    # update the weights to the current estimate
    for k,id in enumerate(query_ids):
        lit = sdd.literal(id)
        wmc.set_literal_weight(lit, query_p[k])
        wmc.set_literal_weight(-lit, 1-query_p[k])           

    # new estimate
    new_p = [0,0,0,0,0,0]

    for m in range(M):
        # get evidence example
        r = get_example(m)
        # compute wmc for given evidence P(E)
        for k,id in enumerate(evidence_ids):
            lit = sdd.literal(id)
            wmc.set_literal_weight(lit, r[k])
            wmc.set_literal_weight(-lit, 1-r[k])
        pe = wmc.propagate()

        # compute wmc for every query atom with given evidence P(E|Q)
        for j,id in enumerate(query_ids):
            lit = sdd.literal(id)
            # save weights of current query atom
            wp = wmc.literal_weight(lit)
            wn = wmc.literal_weight(-lit)
            # set current query
            wmc.set_literal_weight(lit, 1)
            wmc.set_literal_weight(-lit, 0)
            # calculate probability P(E|Q)
            pq = wmc.propagate()
            # restore weights of current query atom
            wmc.set_literal_weight(lit, wp)
            wmc.set_literal_weight(-lit, wn)
            # calculate probability with bayes P(Q|E) = P(E|Q) * P(Q) / P(E)
            p = pq * query_p[j] / pe
            new_p[j] += p/M 

    # update probabilities to new  
    stop = True

    # stop if all probabilities changed less then epsilon
    for qp,np in zip(query_p, new_p):
        if abs(qp - np) > eps:
            stop = False
    if stop:
        break

    # set the current estimate to the new
    query_p = new_p   

for qn, qp in zip(query,query_p):
    print(qn, ":", qp)