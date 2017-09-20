enum month;

enum oils;

float: productprice;

array[int, int] of float: buyingprices;

float: storagecost;

array[int] of float: oilhardness;

float: M;


array[INDEX_SET_production_1] of var float: production;

array[INDEX_SET_buys_1, INDEX_SET_buys_2] of var float: buys;

array[INDEX_SET_stock_1, INDEX_SET_stock_2] of var float: stock;

array[INDEX_SET_useoil_1, INDEX_SET_useoil_2] of var float: useoil;

array[INDEX_SET_useoilb_1, INDEX_SET_useoilb_2] of var bool: useoilb;

set of int: INDEX_SET_buys_1;

set of int: INDEX_SET_buys_2;

set of int: INDEX_SET_production_1;

set of int: INDEX_SET_stock_1;

set of int: INDEX_SET_stock_2;

set of int: INDEX_SET_useoil_1;

set of int: INDEX_SET_useoil_2;

set of int: INDEX_SET_useoilb_1;

set of int: INDEX_SET_useoilb_2;

oils: OIL1;

oils: OIL2;

oils: OIL3;

oils: VEG1;

oils: VEG2;


constraint forall(m in month)(production[m] >= 0);

constraint forall(m1 in month, o in oils)(buys[m1,o] >= 0);

constraint forall(m1 in month, o in oils)(stock[m1,o] >= 0);

constraint forall(m in month, o in oils)(useoil[m,o] >= 0);

constraint forall(o in oils)(stock[1,o] = 500);

constraint forall(o in oils)(stock[6,o] + buys[6,o] - useoil[6,o] >= 500);

constraint forall(m in month, o in oils)(stock[m,o] <= 1000);

constraint forall(m in month, o in oils)(useoil[m,o] <= stock[m,o] + buys[m,o]);

constraint forall(m1 in month, m2 in month, o in oils where m2 = m1 + 1)(stock[m2,o] = stock[m1,o] + buys[m1,o] - useoil[m1,o]);

constraint forall(m in month)(sum(o in oils)(oilhardness[o] * useoil[m,o]) >= 3 * production[m]);

constraint forall(m in month)(sum(o in oils)(oilhardness[o] * useoil[m,o]) <= 6 * production[m]);

constraint forall(m in month)(production[m] = sum(o in oils)(useoil[m,o]));

constraint forall(m in month)(useoil[m,VEG1] + useoil[m,VEG2] <= 200);

constraint forall(m in month)(useoil[m,OIL1] + useoil[m,OIL2] + useoil[m,OIL3] <= 250);

constraint forall(m in month, o in oils)(M * useoilb[m,o] >= useoil[m,o]);

constraint forall(m in month)(sum(o in oils)(useoilb[m,o]) <= 3);

constraint forall(m in month, o in oils)(20 * useoilb[m,o] <= useoil[m,o]);

constraint forall(m in month)(useoilb[m,VEG1] <= useoilb[m,OIL3]);

constraint forall(m in month)(useoilb[m,VEG2] <= useoilb[m,OIL3]);



var float: obj = sum(m in month)(productprice * production[m] - sum(m in month, o in oils)(buyingprices[m,o] * buys[m,o] - sum(m in month, o in oils)(storagecost * stock[m,o])));

solve maximize obj;




