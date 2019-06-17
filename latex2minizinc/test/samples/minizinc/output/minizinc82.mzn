enum HERO = {GUANYU,ZHANGLIAO,XUHUANG};

set of SPOT: LO = {TIANSHU,YONGQUAN};

set of SPOT: HI = SPOT diff LO;

enum SPOT = {BAIHUI,DANZHONG,QUCHI,TIANSHU,YONGQUAN};

array[HERO, SPOT] of int: damage;


array[HERO] of var SPOT: pos1;

array[HERO] of var SPOT: pos2;


include "alldifferent.mzn";

constraint alldifferent(pos1);

constraint alldifferent(pos2);

constraint forall(h in HERO)(pos1[h] != BAIHUI /\ (pos1[h] in LO -> pos2[h] in HI));



solve maximize sum(h in HERO)(damage[h,pos1[h]] + damage[h,pos2[h]]);




