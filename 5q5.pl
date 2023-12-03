remove(_, [], []).

remove(X, [X|TailIn], ListOut) :-
    remove(X, TailIn, ListOut).

remove(X, [Head|TailIn], [Head|TailOut]) :-
    X \= Head,
    remove(X, TailIn, TailOut).