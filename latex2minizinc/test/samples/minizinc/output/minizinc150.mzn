set of int: PREC = 1..m;

set of int: FIRE = 1..n;

array[PREC] of int: pre;

array[PREC] of int: post;

array[FIRE] of int: d;

array[FIRE] of int: reqW;

int: w;

array[FIRE] of int: best;

int: n;

int: m;

int: maxt = sum(f in FIRE)(d[f]);


var int: obj = sum(f in FIRE)(abs(s[f] - best[f]));

array[FIRE] of var 0..maxt: s;

array[FIRE] of var 0..maxt: e = [s[f] + d[f] | f in FIRE];


include "cumulative.mzn";

constraint forall(i in PREC)(e[pre[i]] <= s[post[i]]);

constraint cumulative(s,d,reqW,w);



solve minimize obj;




