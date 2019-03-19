set of int: TABLE = 1..T;

enum SCHOLAR;

int: S;

array[int, int] of SCHOLAR: enemies;

array[int, int] of SCHOLAR: friends;

array[int] of int: reputation;

float: obj1;

float: obj2;

int: T;

int: maxreputation = max(reputation);


array[INDEX_SET_table_1] of var set of SCHOLAR: table;

set of int: INDEX_SET_table_1 = TABLE;


constraint forall(t in TABLE)(card(table[t]) != 1);

predicate not_same_table(SCHOLAR: p1, SCHOLAR: p2) =
	forall(t in TABLE)(not ({p1,p2} subset table[t]));

constraint forall(t in TABLE)(card(table[t]) <= S);

constraint forall(p in SCHOLAR)(exists(t in TABLE)((p in table[t])));

constraint forall(t1,t2 in TABLE where t1 < t2)(table[t1] intersect table[t2] = {});

constraint forall(c in index_set_1of2(enemies))(not_same_table(enemies[c,1],enemies[c,2]));

constraint forall(c in index_set_1of2(friends))(not (not_same_table(friends[c,1],friends[c,2])));

constraint forall(p1,p2 in SCHOLAR where p1 < p2 /\ reputation[p1] = 10 /\ reputation[p2] = 10)(not_same_table(p1,p2));

constraint obj1 = sum(t in TABLE)(card(table[t]) != 0);

constraint obj2 = sum(t in TABLE)(let {var int: minRep = min([reputation[p] * (p in table[t]) + maxreputation * (1 - (p in table[t])) | p in SCHOLAR]); var int: maxRep = max([reputation[p] * (p in table[t]) | p in SCHOLAR])} in
	if minRep = maxreputation then 0 else maxRep - minRep endif);



solve minimize (obj1 * 100 + obj2);




