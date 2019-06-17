enum SCENS;

float: c;

array[SCENS] of float: Pr;

float: r;

float: w;

array[SCENS] of float: D;

float: ExD = sum(k in SCENS)(Pr[k] * D[k]);

float: EVM = -c * ExD + sum(k in SCENS)(Pr[k] * (r * min(ExD,D[k]) + w * max(ExD - D[k],0)));

float: EVPI = sum(k in SCENS)(Pr[k] * (r - c) * D[k]);


var float: ExProfit;

var float: x;

array[SCENS] of var float: y;


constraint assert(c >= 0, "Assertion c >= 0 failed!");

constraint forall(s in SCENS)(assert(Pr[s] >= 0, "Assertion Pr[\(s)] >= 0 failed!"));

constraint assert(r >= 0, "Assertion r >= 0 failed!");

constraint assert(w >= 0, "Assertion w >= 0 failed!");

constraint forall(s in SCENS)(assert(D[s] >= 0, "Assertion D[\(s)] >= 0 failed!"));

constraint x >= 0;

constraint forall(k in SCENS)(y[k] >= 0);

constraint ExProfit = -c * x + sum(k in SCENS)(Pr[k] * (r * y[k] + w * (x - y[k])));

constraint forall(k in SCENS)(y[k] <= x);

constraint forall(k in SCENS)(y[k] <= D[k]);



solve maximize ExProfit;




