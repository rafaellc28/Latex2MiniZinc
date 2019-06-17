enum PROJECTS;

enum PEOPLE;

array[PEOPLE, PROJECTS] of float: cost;

array[PEOPLE] of float: supply;

array[PROJECTS] of float: demand;

array[PEOPLE, PROJECTS] of float: limit;


array[PEOPLE, PROJECTS] of var float: Assign;

var float: M;


constraint forall(i in PEOPLE, j in PROJECTS)(assert(cost[i,j] >= 0, "Assertion cost[\(i),\(j)] >= 0 failed!"));

constraint forall(p in PEOPLE)(assert(supply[p] >= 0, "Assertion supply[\(p)] >= 0 failed!"));

constraint forall(p in PROJECTS)(assert(demand[p] >= 0, "Assertion demand[\(p)] >= 0 failed!"));

constraint forall(i in PEOPLE, j in PROJECTS)(assert(limit[i,j] >= 0, "Assertion limit[\(i),\(j)] >= 0 failed!"));

constraint forall(i in PEOPLE, j in PROJECTS)(Assign[i,j] <= limit[i,j] /\ Assign[i,j] >= 0);

constraint forall(i in PEOPLE)(M >= sum(j in PROJECTS)(cost[i,j] * Assign[i,j]));

constraint forall(i in PEOPLE)(sum(j in PROJECTS)(Assign[i,j]) = supply[i]);

constraint forall(j in PROJECTS)(sum(i in PEOPLE)(Assign[i,j]) = demand[j]);



solve minimize M;




