set of int: time = first..last;

enum prd;

float: rtr;

float: sl;

array[int] of float: dpp;

int: cs;

array[int] of float: hc;

array[int] of float: lc;

float: otr;

array[int] of float: pt;

int: life;

array[int] of float: cri;

array[int] of float: pc;

array[int] of float: crs;

array[int] of float: ol;

int: first;

int: iw;

array[int] of float: cmin;

array[int] of float: cmax;

array[int, int] of float: dem;

array[int] of float: iinv;

array[INDEX_SET_iil_1, INDEX_SET_iil_2] of float: iil = array2d(INDEX_SET_iil_1, INDEX_SET_iil_2, [iinv[p] less sum(v in first..t)(dem[p,v]) | p in prd, t in time]);

int: last;

array[INDEX_SET_minv_1, INDEX_SET_minv_2] of float: minv = array2d(INDEX_SET_minv_1, INDEX_SET_minv_2, [dem[p,t + 1] * (if pro[p,t + 1] = true then pir else rir endif) | p in prd, t in time]);

array[int, int] of float: pro;

float: rir;

float: pir;


array[INDEX_SET_Crews_1] of var float: Crews;

array[INDEX_SET_Hire_1] of var float: Hire;

array[INDEX_SET_Layoff_1] of var float: Layoff;

array[INDEX_SET_Oprd_1, INDEX_SET_Oprd_2] of var float: Oprd;

array[INDEX_SET_Inv_1, INDEX_SET_Inv_2, INDEX_SET_Inv_3] of var float: Inv;

array[INDEX_SET_Short_1, INDEX_SET_Short_2] of var float: Short;

array[INDEX_SET_Rprd_1, INDEX_SET_Rprd_2] of var float: Rprd;

set of int: INDEX_SET_Crews_1;

set of int: INDEX_SET_Hire_1;

set of int: INDEX_SET_Inv_1;

set of int: INDEX_SET_Inv_2;

set of int: INDEX_SET_Inv_3;

set of int: INDEX_SET_Layoff_1;

set of int: INDEX_SET_Oprd_1;

set of int: INDEX_SET_Oprd_2;

set of int: INDEX_SET_Rprd_1;

set of int: INDEX_SET_Rprd_2;

set of int: INDEX_SET_Short_1;

set of int: INDEX_SET_Short_2;

set of int: INDEX_SET_iil_1;

set of int: INDEX_SET_iil_2;

set of int: INDEX_SET_minv_1;

set of int: INDEX_SET_minv_2;


constraint forall(t in floor(first - 1)..last)(Crews[t] >= 0);

constraint forall(t in time)(Hire[t] >= 0);

constraint forall(t in time)(Layoff[t] >= 0);

constraint forall(p in prd, t in time)(Oprd[p,t] >= 0);

constraint forall(p in prd, t in time, a in 1..life)(Inv[p,t,a] >= 0);

constraint forall(p in prd, t in time)(Short[p,t] >= 0);

constraint forall(p in prd, t in time)(Rprd[p,t] >= 0);

constraint forall(t in time)(sum(p in prd)(pt[p] * Rprd[p,t]) <= sl * dpp[t] * Crews[t]);

constraint forall(t in time)(sum(p in prd)(pt[p] * Oprd[p,t]) <= ol[t]);

constraint Crews[first - 1] = iw;

constraint forall(t in time)(Crews[t] = Crews[t - 1] + Hire[t] - Layoff[t]);

constraint forall(t in time)(Crews[t] <= cmax[t] /\ Crews[t] >= cmin[t]);

constraint forall(p in prd)(Rprd[p,first] + Oprd[p,first] + Short[p,first] - Inv[p,first,1] = dem[p,first] less iinv[p]);

constraint forall(p in prd, t in floor(first + 1)..last)(Rprd[p,t] + Oprd[p,t] + Short[p,t] - Short[p,t - 1] + sum(a in 1..life)((Inv[p,t - 1,a] - Inv[p,t,a])) = dem[p,t] less iil[p,t - 1]);

constraint forall(p in prd, t in time)(sum(a in 1..life)(Inv[p,t,a] + iil[p,t]) >= minv[p,t]);

constraint forall(p in prd, v in 1..floor(life - 1), a in floor(v + 1)..life)(Inv[p,first + v - 1,a] = 0);

constraint forall(p in prd, t in time)(Inv[p,t,1] <= Rprd[p,t] + Oprd[p,t]);

constraint forall(p in prd, t in floor(first + 1)..last, a in 2..life)(Inv[p,t,a] <= Inv[p,t - 1,a - 1]);



var float: obj = sum(t in time)(rtr * sl * dpp[t] * cs * Crews[t] + sum(t in time)(hc[t] * Hire[t] + sum(t in time)(lc[t] * Layoff[t] + sum(t in time, p in prd)(otr * cs * pt[p] * Oprd[p,t] + sum(t in time, p in prd, a in 1..life)(cri[p] * pc[p] * Inv[p,t,a] + sum(t in time, p in prd)(crs[p] * pc[p] * Short[p,t]))))));

solve minimize obj;




