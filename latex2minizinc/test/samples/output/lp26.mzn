enum SCENS;

float: C;

array[int] of float: Pr;

float: R;

float: W;

array[int] of float: D;


var float: ExProfit;

var float: x;

array[INDEX_SET_y_1] of var float: y;

set of int: INDEX_SET_y_1;


constraint x >= 0;

constraint forall(k in SCENS)(y[k] >= 0);

constraint ExProfit = -C * x + sum(k in SCENS)(Pr[k] * (R * y[k] + W * (x - y[k])));

constraint forall(k in SCENS)(y[k] <= x);

constraint forall(k in SCENS)(y[k] <= D[k]);



solve maximize ExProfit;




