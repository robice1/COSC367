split_odd_even([], [], []).

split_odd_even([X], [X], []).

split_odd_even([X, Y | TailIn], [X|TailA], [Y|TailB]) :-
    split_odd_even(TailIn, TailA, TailB).