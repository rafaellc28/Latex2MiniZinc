set of int: PREC = 1..m;

set of int: FIRE = 1..n;

array[int] of int: pre;

array[int] of int: post;

array[int] of int: d;

array[int] of int: reqW;

int: w;

array[int] of int: best;

int: n;

int: m;

int: maxt = sum(f in FIRE)(d[f]);


var int: obj = sum(f in FIRE)(abs(s[f] - best[f]));

array[INDEX_SET_s_1] of var 0..maxt: s;

array[INDEX_SET_e_1] of var 0..maxt: e = [s[f] + d[f] | f in FIRE];

set of int: INDEX_SET_e_1 = FIRE;

set of int: INDEX_SET_s_1 = FIRE;


include "cumulative.mzn";

constraint forall(i in PREC)(e[pre[i]] <= s[post[i]]);

constraint cumulative(s,d,reqW,w);



solve minimize obj;




