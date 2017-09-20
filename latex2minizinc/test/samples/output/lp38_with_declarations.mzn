array[INDEX_SET_CONTRACTS, 1..2] of int: CONTRACTS;

set of int: MARKETS = [CONTRACTS[m,1]| m in INDEX_SET_CONTRACTS];

set of int: EVENTS = [CONTRACTS[m,2]| m in INDEX_SET_CONTRACTS];

array[int, int] of float: price;

array[int, int] of float: payout;


var float: minpayout;

array[INDEX_SET_x_1, INDEX_SET_x_2] of var float: x;

set of int: INDEX_SET_CONTRACTS;

set of int: INDEX_SET_x_1;

set of int: INDEX_SET_x_2;


constraint minpayout >= 0;

constraint forall(m in MARKETS, e in EVENTS)(x[m,e] >= 0);

constraint sum(m in INDEX_SET_CONTRACTS)(price[CONTRACTS[m,1],CONTRACTS[m,2]] * x[CONTRACTS[m,1],CONTRACTS[m,2]]) <= 1000;

constraint forall(e in EVENTS)(sum(m in MARKETS)(payout[m,e] * x[m,e]) >= minpayout);



var float: obj = minpayout;

solve maximize obj;




