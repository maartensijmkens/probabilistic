stress(a) :- p(1,a).
stress(b) :- p(1,b).
stress(c) :- p(1,c).
friends(a,b) :- p(2,a,b).
friends(a,c) :- p(2,a,c).
friends(b,c) :- p(2,b,c).
friends(c,b) :- p(2,c,b).
smokes(a) :- stress(a), p(3,a).
smokes(a) :- friends(a,b), smokes(b), p(4,a,b).
smokes(a) :- friends(a,c), smokes(c), p(4,a,c).
smokes_0(b) :- stress(b), p(3,b).
smokes(b) :- smokes_0(b).
smokes(b) :- friends(b,c), smokes_0(c), p(4,b,c).
smokes_0(c) :- stress(c), p(3,c).
smokes(c) :- smokes_0(c).
smokes(c) :- friends(c,b), smokes_0(b), p(4,c,b).

0.2::p(1,X).
0.1::p(2,X,Y).
0.3::p(3,X).
0.4::p(4,X,Y).

query(smokes(a)).
query(friends(a,b)).
query(friends(a,c)).
