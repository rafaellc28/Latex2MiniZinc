enum ELITE;

set of ELITE: archer;

set of ELITE: cavalry;

set of ELITE: infantry;

float: obj = (sum(e in Liu)(liuValue[e])) + (sum(e in Guan)(guanValue[e])) + (sum(e in Zhang)(zhangValue[e]));

array[int] of int: liuValue;

array[int] of int: guanValue;

array[int] of int: zhangValue;


var set of ELITE: Liu;

var set of ELITE: Guan;

var set of ELITE: Zhang;


include "all_disjoint.mzn";

constraint all_disjoint([Liu,Guan,Zhang]);

predicate form(var set of ELITE: aTeam) =
	card(aTeam intersect archer) >= 1 /\ card(aTeam intersect cavalry) >= 2 /\ card(aTeam intersect infantry) >= 2 /\ card(aTeam) = 6;

constraint form(Liu);

constraint form(Guan);

constraint form(Zhang);



solve maximize obj;




