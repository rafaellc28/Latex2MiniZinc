enum RAWMATERIALS;

array[INDEX_SET_S] of set of int: S;

enum PRODUCTS;

array[INDEX_SET_Q] of set of int: Q;

array[int] of float: RLength;

array[int] of float: Demand;

array[int] of float: PLength;

float: BigM;


array[INDEX_SET_y_1, INDEX_SET_y_2, INDEX_SET_y_3, INDEX_SET_y_4] of var bool: y;

array[INDEX_SET_w_1, INDEX_SET_w_2] of var float: w;

array[INDEX_SET_u_1, INDEX_SET_u_2] of var bool: u;

set of int: INDEX_SET_Q;

set of int: INDEX_SET_S;

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

constraint forall(p in PRODUCTS)(sum(q in Q[p], r in RAWMATERIALS, s in S[r])(y[p,q,r,s]) = Demand[p]);

constraint forall(r in RAWMATERIALS, s in S[r])(sum(p in PRODUCTS, q in Q[p])(PLength[p] * y[p,q,r,s] + w[r,s]) = RLength[r]);

constraint forall(r in RAWMATERIALS, s in S[r])(BigM * u[r,s] >= sum(p in PRODUCTS, q in Q[p])(y[p,q,r,s]));



solve minimize sum(r in RAWMATERIALS, s in S[r])(RLength[r] * s * u[r,s]);




