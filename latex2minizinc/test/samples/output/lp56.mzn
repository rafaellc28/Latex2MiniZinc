enum month;

enum oils;

float: Productprice;

array[month, oils] of float: Buyingprices;

float: Storagecost;

array[oils] of float: Oilhardness;

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


constraint forall(m in month)(production[m] >= 0);

constraint forall(m1 in month, o in oils)(buys[m1,o] >= 0);

constraint forall(m1 in month, o in oils)(stock[m1,o] >= 0);

constraint forall(m in month, o in oils)(useoil[m,o] >= 0);

constraint forall(o in oils)(stock[to_enum(month,1),o] = 500);

constraint forall(o in oils)(stock[to_enum(month,6),o] + buys[to_enum(month,6),o] - useoil[to_enum(month,6),o] >= 500);

constraint forall(m in month, o in oils)(stock[m,o] <= 1000);

constraint forall(m in month, o in oils)(useoil[m,o] <= stock[m,o] + buys[m,o]);

constraint forall(m1 in month, m2 in month, o in oils where m2 = m1 + 1)(stock[m2,o] = stock[m1,o] + buys[m1,o] - useoil[m1,o]);

constraint forall(m in month)(sum(o in oils)(Oilhardness[o] * useoil[m,o]) >= 3 * production[m]);

constraint forall(m in month)(sum(o in oils)(Oilhardness[o] * useoil[m,o]) <= 6 * production[m]);

constraint forall(m in month)(production[m] = sum(o in oils)(useoil[m,o]));

constraint forall(m in month)(useoil[m,VEG1] + useoil[m,VEG2] <= 200);

constraint forall(m in month)(useoil[m,OIL1] + useoil[m,OIL2] + useoil[m,OIL3] <= 250);

constraint forall(m in month, o in oils)(M * useoilb[m,o] >= useoil[m,o]);

constraint forall(m in month)(sum(o in oils)(useoilb[m,o]) <= 3);

constraint forall(m in month, o in oils)(20 * useoilb[m,o] <= useoil[m,o]);

constraint forall(m in month)(useoilb[m,VEG1] <= useoilb[m,OIL3]);

constraint forall(m in month)(useoilb[m,VEG2] <= useoilb[m,OIL3]);



solve maximize sum(m in month)(Productprice * production[m] - sum(m in month, o in oils)(Buyingprices[m,o] * buys[m,o] - sum(m in month, o in oils)(Storagecost * stock[m,o])));




