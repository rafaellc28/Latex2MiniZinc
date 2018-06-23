enum RAWMATERIALS;

array[INDEX_SET_S_1] of set of int: S = array1d(INDEX_SET_S_1, [1..avail[r] | r in RAWMATERIALS]);

enum PRODUCTS;

array[INDEX_SET_Q_1] of set of int: Q = array1d(INDEX_SET_Q_1, [1..demand[p] | p in PRODUCTS]);

array[int] of float: rLength;

array[int] of int: demand;

array[int] of float: pLength;

float: bigM;

array[int] of int: avail;


array[INDEX_SET_u_1, INDEX_SET_u_2] of var bool: u;

array[INDEX_SET_y_1, INDEX_SET_y_2, INDEX_SET_y_3, INDEX_SET_y_4] of var bool: y;

array[INDEX_SET_w_1, INDEX_SET_w_2] of var float: w;

set of int: INDEX_SET_Q_1;

set of int: INDEX_SET_S_1;

set of int: INDEX_SET_u_1 = RAWMATERIALS;

set of int: INDEX_SET_u_2;

set of int: INDEX_SET_w_1 = RAWMATERIALS;

set of int: INDEX_SET_w_2;

set of int: INDEX_SET_y_1 = PRODUCTS;

set of int: INDEX_SET_y_2;

set of int: INDEX_SET_y_3 = RAWMATERIALS;

set of int: INDEX_SET_y_4;


constraint forall(r in INDEX_SET_w_1, s in INDEX_SET_w_2)(w[r,s] >= 0);

constraint forall(p in PRODUCTS, q in Q[p])(sum(r in RAWMATERIALS, s in S[r])(y[p,q,r,s]) = 1);

constraint forall(p in PRODUCTS)(sum(q in Q[p], r in RAWMATERIALS, s in S[r])(y[p,q,r,s]) = demand[p]);

constraint forall(r in RAWMATERIALS, s in S[r])(sum(p in PRODUCTS, q in Q[p])(pLength[p] * y[p,q,r,s] + w[r,s]) = rLength[r]);

constraint forall(r in RAWMATERIALS, s in S[r])(bigM * u[r,s] >= sum(p in PRODUCTS, q in Q[p])(y[p,q,r,s]));



solve minimize sum(r in RAWMATERIALS, s in S[r])(rLength[r] * s * u[r,s]);




