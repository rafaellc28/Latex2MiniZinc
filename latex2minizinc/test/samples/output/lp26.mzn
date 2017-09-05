enum SCENS;

float: C;

array[int] of float: Pr;

float: R;

float: W;

array[int] of float: D;


var float: ExProfit;

var float: x;

array[int] of var float: y;


constraint x >= 0;

constraint forall(k in SCENS)(y[k] >= 0);

constraint ExProfit = -C * x + sum(k in SCENS)(Pr[k] * (R * y[k] + W * (x - y[k])));

constraint forall(k in SCENS)(y[k] <= x);

constraint forall(k in SCENS)(y[k] <= D[k]);



var float: obj = ExProfit;

solve maximize obj;




