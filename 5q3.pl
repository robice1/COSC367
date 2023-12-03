listtran([], []).

listtran([Head1|Tail1], [Head2|Tail2]) :-
    tran(Head1, Head2),
    listtran(Tail1, Tail2).