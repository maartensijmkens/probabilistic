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

# create new theta ids
def get_theta_id():
    global atomcount
    atomcount += 2
    return (atomcount-1, atomcount)

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
        # get ids for thetas of current parent of the current node
        T = get_theta_id()  
        # set weights of thetas
        weights[T[0]] = (1-p, 1)
        weights[T[1]] = (p, 1)
        # parameter clauses of current node (theta -> lambda)
        clauses.append([-T[0], L[0]])
        clauses.append([-T[1], L[1]])
        # get truth values of CPT
        sign = map(int,"{:b}".format(i).zfill(n))
        # start parameter clauses (lambdas -> theta)
        clause1 = [T[0], -L[0]]
        clause2 = [T[1], -L[1]]
        for s,parent in zip(sign, parents):
            # get ids of current parent lambdas
            LP = get_lambda_id(parent)
            # extend parameter clauses with lambda of current parent (lambdas -> theta)
            clause1.append(-LP[s])
            clause2.append(-LP[s])
            # parameter clauses of conditional (theta -> lambda)
            clauses.append([-T[0], LP[s]])
            clauses.append([-T[1], LP[s]])
        clauses.append(clause1)
        clauses.append(clause2)

# get id of the query atom
query_atom_id = get_lambda_id("smokes(a)")[1]
# append query clause
clauses.append([query_atom_id])              
# create a cnf file
create_cnf_file(clauses, weights, atomcount, "program_enc1.cnf")