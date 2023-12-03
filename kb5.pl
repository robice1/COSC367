directlyIn(irina, natasha).
directlyIn(natasha, olga).
directlyIn(olga, katarina).

contains(X,Y) :- directlyIn(Y,X).
contains(X,Y) :- directlyIn(Z,X), contains(Z,Y).
