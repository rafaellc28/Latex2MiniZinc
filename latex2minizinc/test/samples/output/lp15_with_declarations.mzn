enum RAWMATERIALS;

array[RAWMATERIALS] of set of int: S = array1d(RAWMATERIALS, [1..avail[r] | r in RAWMATERIALS]);

enum PRODUCTS;

array[PRODUCTS] of set of int: Q = array1d(PRODUCTS, [1..demand[p] | p in PRODUCTS]);

array[RAWMATERIALS] of float: rLength;

array[PRODUCTS] of int: demand;

array[PRODUCTS] of float: pLength;

float: bigM;

array[RAWMATERIALS] of int: avail;


array[RAWMATERIALS, INDEX_SET_u_2] of var bool: u;

array[PRODUCTS, INDEX_SET_y_2, RAWMATERIALS, INDEX_SET_y_4] of var bool: y;

array[RAWMATERIALS, INDEX_SET_w_2] of var float: w;

set of int: INDEX_SET_u_2;

set of int: INDEX_SET_w_2;

set of int: INDEX_SET_y_2;

set of int: INDEX_SET_y_4;


constraint forall(r in RAWMATERIALS, s in INDEX_SET_w_2)(w[r,s] >= 0);

constraint forall(p in PRODUCTS, q in Q[p])(sum(r in RAWMATERIALS, s in S[r])(y[p,q,r,s]) = 1);

constraint forall(p in PRODUCTS)(sum(q in Q[p], r in RAWMATERIALS, s in S[r])(y[p,q,r,s]) = demand[p]);

constraint forall(r in RAWMATERIALS, s in S[r])(sum(p in PRODUCTS, q in Q[p])(pLength[p] * y[p,q,r,s] + w[r,s]) = rLength[r]);

constraint forall(r in RAWMATERIALS, s in S[r])(bigM * u[r,s] >= sum(p in PRODUCTS, q in Q[p])(y[p,q,r,s]));



solve minimize sum(r in RAWMATERIALS, s in S[r])(rLength[r] * s * u[r,s]);




