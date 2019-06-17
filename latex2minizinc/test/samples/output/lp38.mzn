array[INDEX_SET_CONTRACTS, 1..2] of int: CONTRACTS;

enum MARKETS;

enum EVENTS;

array[int, int] of float: Price;

array[MARKETS, EVENTS] of float: Payout;


var float: minpayout;

array[MARKETS, EVENTS] of var float: x;

set of int: INDEX_SET_CONTRACTS;


constraint minpayout >= 0;

constraint forall(m in MARKETS, e in EVENTS)(x[m,e] >= 0);

constraint sum(m in INDEX_SET_CONTRACTS)(Price[CONTRACTS[m,1],CONTRACTS[m,2]] * x[to_enum(MARKETS,CONTRACTS[m,1]),to_enum(EVENTS,CONTRACTS[m,2])]) <= 1000;

constraint forall(e in EVENTS)(sum(m in MARKETS)(Payout[m,e] * x[m,e]) >= minpayout);



solve maximize minpayout;




