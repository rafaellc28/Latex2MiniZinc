enum PROJECTS;

enum PEOPLE;

array[int, int] of float: cost;

array[int] of float: supply;

array[int] of float: demand;

array[int, int] of float: limit;


array[INDEX_SET_Assign_1, INDEX_SET_Assign_2] of var float: Assign;

var float: M;

set of int: INDEX_SET_Assign_1 = PEOPLE;

set of int: INDEX_SET_Assign_2 = PROJECTS;


constraint forall(i in INDEX_SET_Assign_1, j in INDEX_SET_Assign_2)(Assign[i,j] <= limit[i,j] /\ Assign[i,j] >= 0);

constraint forall(i in PEOPLE)(M >= sum(j in PROJECTS)(cost[i,j] * Assign[i,j]));

constraint forall(i in PEOPLE)(sum(j in PROJECTS)(Assign[i,j]) = supply[i]);

constraint forall(j in PROJECTS)(sum(i in PEOPLE)(Assign[i,j]) = demand[j]);



solve minimize M;




