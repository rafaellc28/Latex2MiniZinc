enum SPOT = {DAZHUI,TAODAOO,SHENZHU,LINGTAI,ZHIYANG,ZHONGSHU,JIZHONG,XUANSHU,YAOYANGGUAN,YAOYU};

int: c;

int: m;


array[1..m, 1..c] of var SPOT: point;

array[1..m] of var set of SPOT: stage;


include "global_cardinality_low_up.mzn";

constraint forall(i in 1..m)(card(stage[i]) = c);

constraint forall(i in 1..m, j in 1..floor(c - 1))(point[i,j] < point[i,j + 1]);

constraint forall(i1,i2,i3 in 1..m where i1 < i2 /\ i2 < i3)((stage[i1] intersect stage[i2] intersect stage[i3]) = {});

constraint forall(i in 1..floor(m - 1), j in 1..c)(point[i,j] < point[i + 1,j]);

constraint sum(i in 1..m)(ZHIYANG in stage[i]) <= 1;

constraint sum(i in 1..m)(ZHONGSHU in stage[i]) <= 1;

constraint forall(i in 1..m, s in SPOT)((s in stage[i]) -> exists(j in 1..c)(point[i,j] = s));

constraint forall(i in 1..m, j in 1..c)(point[i,j] in stage[i]);

constraint global_cardinality_low_up([point[i,j] | i in 1..m, j in 1..c],[ZHIYANG,ZHONGSHU],[0,0],[1,1]);

solve satisfy;


