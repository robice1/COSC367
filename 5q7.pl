preorder(leaf(X), [X]) :-
    \+ leaf = tree(_,_,_).

preorder(tree(Root, Left, Right), [Root | Tail]) :-
    preorder(Left, LeftTraversal),
    preorder(Right, RightTraversal),
    append(LeftTraversal, RightTraversal, Tail).