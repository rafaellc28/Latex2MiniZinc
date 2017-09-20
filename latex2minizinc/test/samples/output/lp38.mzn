array[INDEX_SET_CONTRACTS, 1..2] of int: CONTRACTS;

enum MARKETS;

enum EVENTS;

array[int, int] of float: Price;

array[int, int] of float: Payout;


var float: minpayout;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_CONTRACTS;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint minpayout >= 0;

constraint forall(m in MARKETS, e in EVENTS)(x[m,e] >= 0);

constraint sum(m in INDEX_SET_CONTRACTS)(Price[CONTRACTS[m,1],CONTRACTS[m,2]] * x[CONTRACTS[m,1],CONTRACTS[m,2]]) <= 1000;

constraint forall(e in EVENTS)(sum(m in MARKETS)(Payout[m,e] * x[m,e]) >= minpayout);



var float: obj = minpayout;

solve maximize obj;




