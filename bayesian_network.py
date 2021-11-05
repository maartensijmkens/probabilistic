class Node:
  def __init__(self, parents, gate, noise=1.):
    self.parents = parents
    n = 2**len(parents)-1
    if gate == "or":
        self.probs = [0.] + [noise] * n
    if gate == "and":
        self.probs = [0.] * n + [noise]

network = {
    "stress(a)":    Node(["c7"], "and"),
    "stress(b)":    Node(["c9"], "and"), 
    "stress(c)":    Node(["c11"], "and"), 
    "friends(a,b)": Node(["c8"], "and"), 
    "friends(a,c)": Node(["c13"], "and"), 
    "friends(b,c)": Node(["c10"], "and"), 
    "friends(c,b)": Node(["c14"], "and"),
    "smokes(a)":    Node(["c0","c6","c4"], "or"),
    "smokes(b)":    Node(["c12","c3"], "or"),
    "smokes(c)":    Node(["c5","c15"], "or"),
    "smokes_0(b)":  Node(["c1"], "and"),
    "smokes_0(c)":  Node(["c2"], "and"),
    "c0":    Node(["stress(a)"], "and", noise=0.3), 
    "c1":    Node(["stress(b)"], "and", noise=0.3),
    "c2":    Node(["stress(c)"], "and", noise=0.3),
    "c3":    Node(["smokes_0(c)","friends(b,c)"], "and", noise=0.4), 
    "c4":    Node(["smokes(b)","friends(a,b)"], "and", noise=0.4), 
    "c5":    Node(["smokes_0(b)","friends(c,b)"], "and", noise=0.4), 
    "c6":    Node(["smokes(c)","friends(a,c)"], "and", noise=0.4), 
    "c7":    Node([], "and", noise=0.2), 
    "c8":    Node([], "and", noise=0.1), 
    "c9":    Node([], "and", noise=0.2), 
    "c10":   Node([], "and", noise=0.1),  
    "c11":   Node([], "and", noise=0.2), 
    "c12":   Node(["smokes_0(b)"], "and"), 
    "c13":   Node([], "and", noise=0.1),   
    "c14":   Node([], "and", noise=0.1),  
    "c15":   Node(["smokes_0(c)"], "and"), 
}

# print the CPT of a node
def print_CPT(node):
    parents = network[node].parents
    n = len(parents)
    probs = network[node].probs
    print("\t\t".join(parents + ["Pr"]))
    for i,p in enumerate(probs):
        v = "{:b}".format(i).zfill(n)
        print("\t\t".join(v) + "\t\t" + str(p))
    print()

# print_CPT("smokes(a)")
# print_CPT("c6")