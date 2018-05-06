enum ACT;

enum PROD;

array[int] of float: cost;

array[int] of float: Level;

array[int, int] of float: io;

array[int] of float: demand;

array[int] of float: level_min;

array[int] of float: level_max;


constraint forall(i in PROD)(sum(j in ACT)(io[i,j] * Level[j]) >= demand[i]);



solve minimize sum(j in ACT)(cost[j] * Level[j]);




