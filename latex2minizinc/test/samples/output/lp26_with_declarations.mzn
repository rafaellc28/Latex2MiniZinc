enum SCENS;

float: c;

array[int] of float: Pr;

float: r;

float: w;

array[int] of float: D;

float: ExD = sum(k in SCENS)(Pr[k] * D[k]);

float: EVM = -c * ExD + sum(k in SCENS)(Pr[k] * (r * min(ExD,D[k]) + w * max(ExD - D[k],0)));

float: EVPI = sum(k in SCENS)(Pr[k] * (r - c) * D[k]);


var float: ExProfit;

var float: x;

array[int] of var float: y;


constraint x >= 0;

constraint forall(k in SCENS)(y[k] >= 0);

constraint ExProfit = -c * x + sum(k in SCENS)(Pr[k] * (r * y[k] + w * (x - y[k])));

constraint forall(k in SCENS)(y[k] <= x);

constraint forall(k in SCENS)(y[k] <= D[k]);



var float: obj = ExProfit;

solve maximize obj;




