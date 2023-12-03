asbs([]).

asbs([a]).

asbs([a|Rest]) :-
    asbs(Rest).

asbs([a,b|Rest]) :-
    bs(Rest).

bs([]).

bs([b|Rest]) :-
    bs(Rest).