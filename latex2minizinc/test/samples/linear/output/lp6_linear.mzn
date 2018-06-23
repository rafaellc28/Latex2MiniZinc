enum ACT;

enum PROD;

array[int] of float: cost;

array[int, int] of float: io;

array[int] of float: demand;


array[INDEX_SET_Level_1] of var float: Level;

set of int: INDEX_SET_Level_1 = ACT;


constraint forall(j in INDEX_SET_Level_1)(Level[j] >= 0);

constraint forall(i in PROD)(sum(j in ACT)(io[i,j] * Level[j]) >= demand[i]);



solve minimize sum(j in ACT)(cost[j] * Level[j]);




