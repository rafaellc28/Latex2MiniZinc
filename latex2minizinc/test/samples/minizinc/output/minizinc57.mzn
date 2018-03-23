enum SPOT = {DAZHUI,TAODAOO,SHENZHU,LINGTAI,ZHIYANG,ZHONGSHU,JIZHONG,XUANSHU,YAOYANGGUAN,YAOYU};

int: c;

int: m;


array[INDEX_SET_point_1, INDEX_SET_point_2] of var SPOT: point;

array[INDEX_SET_stage_1] of var set of SPOT: stage;

set of int: INDEX_SET_point_1 = 1..m;

set of int: INDEX_SET_point_2 = 1..c;

set of int: INDEX_SET_stage_1 = 1..m;


constraint forall(i in 1..m)(card(stage[i]) = c);

constraint forall(i in 1..m, j in 1..floor(c - 1))(point[i,j] < point[i,j + 1]);

constraint forall(i1,i2,i3 in 1..m where i1 < i2 /\ i2 < i3)((stage[i1] intersect stage[i2] intersect stage[i3]) = {});

constraint forall(i in 1..floor(m - 1), j in 1..c)(point[i,j] < point[i + 1,j]);

constraint sum(i in 1..m)(ZHIYANG in stage[i]) <= 1;

constraint sum(i in 1..m)(ZHONGSHU in stage[i]) <= 1;

constraint forall(i in 1..m, s in SPOT)((s in stage[i]) -> exists(j in 1..c)(point[i,j] = s));

constraint forall(i in 1..m, j in 1..c)(point[i,j] in stage[i]);

solve satisfy;


