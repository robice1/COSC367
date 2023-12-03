twice([], []).

twice([Head|TailIn], [Head, Head|TailOut]) :-
    twice(TailIn, TailOut).