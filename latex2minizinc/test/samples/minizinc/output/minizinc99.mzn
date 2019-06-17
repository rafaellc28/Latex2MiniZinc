set of ELITE: archer;

set of ELITE: cavalry;

set of ELITE: infantry;

enum ELITE;

array[ELITE] of int: liuValue;

array[ELITE] of int: guanValue;

array[ELITE] of int: zhangValue;


var int: obj = (sum(e in Liu)(liuValue[to_enum(ELITE,e)])) + (sum(e in Guan)(guanValue[to_enum(ELITE,e)])) + (sum(e in Zhang)(zhangValue[to_enum(ELITE,e)]));

var set of ELITE: Liu;

var set of ELITE: Guan;

var set of ELITE: Zhang;


include "all_disjoint.mzn";

constraint all_disjoint([Liu,Guan,Zhang]);

constraint card(Liu intersect archer) >= 1;

constraint card(Liu intersect cavalry) >= 2;

constraint card(Liu intersect infantry) >= 2;

constraint card(Liu) = 6;

constraint card(Guan intersect archer) >= 1;

constraint card(Guan intersect cavalry) >= 2;

constraint card(Guan intersect infantry) >= 2;

constraint card(Guan) = 6;

constraint card(Zhang intersect archer) >= 1;

constraint card(Zhang intersect cavalry) >= 2;

constraint card(Zhang intersect infantry) >= 2;

constraint card(Zhang) = 6;



solve maximize obj;




