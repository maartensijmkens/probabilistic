# create a cnf file of given clauses with given weights and atoms
def create_cnf_file(clauses, weights, atomcount, filename):
    dimacs = create_cnf_string(clauses, weights, atomcount)
    file = open(filename, "w")
    file.write(dimacs)
    file.close()

# create a cnf file of given clauses with given weights and atoms
def create_cnf_string(clauses, weights, atomcount):
    clausecount = len(clauses)
    dimacs = to_dimacs(clauses, weights, atomcount, clausecount)
    return dimacs


# return the weights of x as string
def get_atom_weights(x, weights):
    if x in weights:
        return " ".join(map(str,weights[x]))         
    else:
        return "1 1"

# put cnf in dimacs format
def to_dimacs(clauses, weights, atomcount, clausecount):
    dimacs = []
    dimacs.append("c weights " + " ".join([get_atom_weights(x+1, weights) for x in range(atomcount)]))
    dimacs.append("p cnf " + str(atomcount) + " " + str(clausecount))
    for clause in clauses:
        dimacs.append(" ".join(map(str,clause + [0])))
    return "\n".join(dimacs)

