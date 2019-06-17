set of int: PREC = index_set_1of2(prec);

enum PERSON;

set of int: TIME = 0..total;

array[int, 1..2] of PERSON: prec;

array[PERSON] of int: duration;

array[int] of int: weekends = [t | t in TIME where floor((t + starting_day)) mod 7 = 5];

array[int] of int: weekdur = [duration[t] | t in PERSON where on_weekend[t] = false];

array[int] of int: weekend_dur = [2 | t in TIME where floor((t + starting_day)) mod 7 = 5];

array[PERSON] of int: rank;

array[PERSON] of bool: on_weekend;

0..6: starting_day;

int: total = sum(duration) + 7 * sum(p in PERSON)(on_weekend[p] = false);


array[PERSON] of var TIME: start;

var TIME: end;

array[INDEX_SET_weekday_1] of var TIME: weekday = [start[t] | t in PERSON where on_weekend[t] = false];

var int: rank_violation;

set of int: INDEX_SET_weekday_1;


include "disjunctive.mzn";

constraint forall(p in PREC)(start[prec[p,1]] + duration[prec[p,1]] <= start[prec[p,2]]);

constraint disjunctive(start,duration);

constraint disjunctive(weekday ++ weekends,weekdur ++ weekend_dur);

constraint forall(p in PERSON)(start[p] + duration[p] <= end);

constraint rank_violation = sum(p1,p2 in PERSON where rank[p1] < rank[p2])(start[p1] > start[p2]);



solve minimize card(PERSON) * card(PERSON) * end + rank_violation;




