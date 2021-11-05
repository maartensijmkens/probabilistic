from create_cnf_file import create_cnf_file
from bayesian_network import network

clauses = []
atomcount = 0
atom_ids = {}
weights = {}

# fetch or create lambda ids for the given atom
def get_lambda_id(atom):
    global atom_ids
    global atomcount 
    if atom not in atom_ids:
        atomcount += 2
        atom_ids[atom] = atomcount
    id = atom_ids[atom]
    return (id-1, id)

# create new rho ids
def get_rho_id():
    global atomcount
    atomcount += 1
    return atomcount

# loop over all nodes in the network to create the indicator clauses and parameter clauses
for node in network:

    probs = network[node].probs
    parents = network[node].parents
    n = len(parents)
    
    # get ids for lambdas of current node
    L = get_lambda_id(node)
    # indicator clauses for lambdas 
    clauses.append([L[0], L[1]])
    clauses.append([-L[0], -L[1]])

    for i,p in enumerate(probs):

        # get ids for rhos of current node
        R = get_rho_id()

        weights[R] = (p, 1-p)
        # start parameter clauses for this rho
        clause1 = [L[0], R]
        clause2 = [L[1], -R]

        # get truth values of CPT
        sign = map(int,"{:b}".format(i).zfill(n))

        # append lambda's of conditionals to parameter clauses
        for s,parent in zip(sign, parents):
            LP = get_lambda_id(parent)
            clause1.append(-LP[s])
            clause2.append(-LP[s])
        
        clauses.append(clause1)
        clauses.append(clause2)

# get id of the query atom
query_atom_id = get_lambda_id("smokes(a)")[1]
# append query clause
clauses.append([query_atom_id])              
# create a cnf file
create_cnf_file(clauses, weights, atomcount, "program_enc2.cnf")