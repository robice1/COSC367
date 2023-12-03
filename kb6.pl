word(astante, a,s,t,a,n,t,e).
word(astoria, a,s,t,o,r,i,a).
word(baratto, b,a,r,a,t,t,o).
word(cobalto, c,o,b,a,l,t,o).
word(pistola, p,i,s,t,o,l,a).
word(statale, s,t,a,t,a,l,e).

solution(V1,V2,V3,H1,H2,H3) :-
    word(V1,_,V1A,_,V1B,_,V1C,_),
    word(V2,_,V2A,_,V2B,_,V2C,_),
    word(V3,_,V3A,_,V3B,_,V3C,_),
    word(H1,_,V1A,_,V2A,_,V3A,_),
    word(H2,_,V1B,_,V2B,_,V3B,_),
    word(H3,_,V1C,_,V2C,_,V3C,_).
