enum month;

enum oils;

float: productprice;

array[month, oils] of float: buyingprices;

float: storagecost;

array[oils] of float: oilhardness;

float: M;


array[month] of var float: production;

array[month, oils] of var float: buys;

array[month, oils] of var float: stock;

array[month, oils] of var float: useoil;

array[month, oils] of var bool: useoilb;

oils: OIL1;

oils: OIL2;

oils: OIL3;

oils: VEG1;

oils: VEG2;


constraint assert(productprice >= 0, "Assertion productprice >= 0 failed!");

constraint forall(o in oils)(assert(oilhardness[o] >= 0, "Assertion oilhardness[\(o)] >= 0 failed!"));

constraint assert(M >= 0, "Assertion M >= 0 failed!");

constraint forall(m in month)(production[m] >= 0);

constraint forall(m1 in month, o in oils)(buys[m1,o] >= 0);

constraint forall(m1 in month, o in oils)(stock[m1,o] >= 0);

constraint forall(m in month, o in oils)(useoil[m,o] >= 0);

constraint forall(o in oils)(stock[to_enum(month,1),o] = 500);

constraint forall(o in oils)(stock[to_enum(month,6),o] + buys[to_enum(month,6),o] - useoil[to_enum(month,6),o] >= 500);

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



solve maximize sum(m in month)(productprice * production[m] - sum(m in month, o in oils)(buyingprices[m,o] * buys[m,o] - sum(m in month, o in oils)(storagecost * stock[m,o])));




