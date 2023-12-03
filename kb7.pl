mirror(leaf(A), leaf(A)).

mirror(tree(Left1, Right1), tree(Left2, Right2)) :-
    mirror(Left1, Right2),
    mirror(Right1, Left2).
