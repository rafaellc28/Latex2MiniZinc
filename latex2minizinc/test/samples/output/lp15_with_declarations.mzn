enum RAWMATERIALS;

array[INDEX_SET_S_1] of set of int: S = array1d(INDEX_SET_S_1, [1..avail[r] | r in RAWMATERIALS]);

enum PRODUCTS;

array[INDEX_SET_Q_1] of set of int: Q = array1d(INDEX_SET_Q_1, [1..demand[p] | p in PRODUCTS]);

array[int] of float: rLength;

array[int] of int: demand;

array[int] of float: pLength;

float: bigM;

array[int] of int: avail;

set of int: INDEX_SET_Q_1;

set of int: INDEX_SET_S_1;


array[int, int] of var bool: u;

array[int, int, int, int] of var bool: y;

array[int, int] of var float: w;


constraint forall(r in RAWMATERIALS, s in S[r])(w[r,s] >= 0);

constraint forall(p in PRODUCTS, q in Q[p])(sum(r in RAWMATERIALS, s in S[r])(y[p,to_enum(PRODUCTS,q),r,to_enum(RAWMATERIALS,s)]) = 1);

constraint forall(p in PRODUCTS)(sum(q in Q[p], r in RAWMATERIALS, s in S[r])(y[p,to_enum(PRODUCTS,q),r,to_enum(RAWMATERIALS,s)]) = demand[p]);

constraint forall(r in RAWMATERIALS, s in S[r])(sum(p in PRODUCTS, q in Q[p])(pLength[p] * y[p,to_enum(PRODUCTS,q),r,to_enum(RAWMATERIALS,s)] + w[r,to_enum(RAWMATERIALS,s)]) = rLength[r]);

constraint forall(r in RAWMATERIALS, s in S[r])(bigM * u[r,to_enum(RAWMATERIALS,s)] >= sum(p in PRODUCTS, q in Q[p])(y[p,to_enum(PRODUCTS,q),r,to_enum(RAWMATERIALS,s)]));



var float: obj = sum(r in RAWMATERIALS, s in S[r])(rLength[r] * to_enum(RAWMATERIALS,s) * u[r,to_enum(RAWMATERIALS,s)]);

solve minimize obj;




