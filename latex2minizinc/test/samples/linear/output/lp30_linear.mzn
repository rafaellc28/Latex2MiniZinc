set of int: time = first..last;

enum prod;

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

array[INDEX_SET_iil_1, INDEX_SET_iil_2] of float: iil = array2d(INDEX_SET_iil_1, INDEX_SET_iil_2, [if iinv[p] < sum(v in first..t)(dem[p,v]) then 0 else iinv[p] - sum(v in first..t)(dem[p,v]) endif | p in prod, t in time]);

int: last;

array[INDEX_SET_minv_1, INDEX_SET_minv_2] of float: minv = array2d(INDEX_SET_minv_1, INDEX_SET_minv_2, [dem[p,t + 1] * (if pro[p,t + 1] = true then pir else rir endif) | p in prod, t in time]);

float: rir;

float: pir;

array[int, int] of bool: pro;


array[INDEX_SET_Crews_1] of var float: Crews;

array[INDEX_SET_Hire_1] of var float: Hire;

array[INDEX_SET_Layoff_1] of var float: Layoff;

array[INDEX_SET_Rprod_1, INDEX_SET_Rprod_2] of var float: Rprod;

array[INDEX_SET_Oprod_1, INDEX_SET_Oprod_2] of var float: Oprod;

array[INDEX_SET_Short_1, INDEX_SET_Short_2] of var float: Short;

array[INDEX_SET_Inv_1, INDEX_SET_Inv_2, INDEX_SET_Inv_3] of var float: Inv;

set of int: INDEX_SET_Crews_1 = floor(first - 1)..last;

set of int: INDEX_SET_Hire_1 = time;

set of int: INDEX_SET_Inv_1 = prod;

set of int: INDEX_SET_Inv_2 = time;

set of int: INDEX_SET_Inv_3 = 1..life;

set of int: INDEX_SET_Layoff_1 = time;

set of int: INDEX_SET_Oprod_1 = prod;

set of int: INDEX_SET_Oprod_2 = time;

set of int: INDEX_SET_Rprod_1 = prod;

set of int: INDEX_SET_Rprod_2 = time;

set of int: INDEX_SET_Short_1 = prod;

set of int: INDEX_SET_Short_2 = time;

set of int: INDEX_SET_iil_1;

set of int: INDEX_SET_iil_2;

set of int: INDEX_SET_minv_1;

set of int: INDEX_SET_minv_2;


constraint forall(t in time)(assert(hc[t] >= 0, "Assertion hc[\(t)] >= 0 failed!"));

constraint forall(t in time)(assert(lc[t] >= 0, "Assertion lc[\(t)] >= 0 failed!"));

constraint forall(t in time)(assert(ol[t] >= 0, "Assertion ol[\(t)] >= 0 failed!"));

constraint assert(iw >= 0, "Assertion iw >= 0 failed!");

constraint forall(t in time)(assert(cmin[t] >= 0, "Assertion cmin[\(t)] >= 0 failed!"));

constraint forall(t in time)(assert(cmax[t] >= cmin[t], "Assertion cmax[\(t)] >= cmin[\(t)] failed!"));

constraint forall(p in prod, i in first..floor(last + 1))(assert(dem[p,i] >= 0, "Assertion dem[\(p),\(i)] >= 0 failed!"));

constraint forall(p in prod)(assert(iinv[p] >= 0, "Assertion iinv[\(p)] >= 0 failed!"));

constraint assert(rir >= 0, "Assertion rir >= 0 failed!");

constraint assert(pir >= 0, "Assertion pir >= 0 failed!");

constraint forall(i in INDEX_SET_Crews_1)(Crews[i] >= 0);

constraint forall(t in INDEX_SET_Hire_1)(Hire[t] >= 0);

constraint forall(t in INDEX_SET_Layoff_1)(Layoff[t] >= 0);

constraint forall(p in INDEX_SET_Rprod_1, t in INDEX_SET_Rprod_2)(Rprod[p,t] >= 0);

constraint forall(p in INDEX_SET_Oprod_1, t in INDEX_SET_Oprod_2)(Oprod[p,t] >= 0);

constraint forall(p in INDEX_SET_Short_1, t in INDEX_SET_Short_2)(Short[p,t] >= 0);

constraint forall(p in INDEX_SET_Inv_1, t in INDEX_SET_Inv_2, j in INDEX_SET_Inv_3)(Inv[p,t,j] >= 0);

constraint forall(t in time)(sum(p in prod)(pt[p] * Rprod[p,t]) != 0 <- sl * dpp[t] * Crews[t] != 0);

constraint forall(t in time)(sum(p in prod)(pt[p] * Oprod[p,t]) <= ol[t]);

constraint Crews[first - 1] = iw;

constraint forall(t in time)(Crews[t] = Crews[t - 1] + Hire[t] - Layoff[t]);

constraint forall(t in time)(Crews[t] <= cmax[t] /\ Crews[t] >= cmin[t]);

constraint forall(p in prod)(Rprod[p,first] + Oprod[p,first] + Short[p,first] - Inv[p,first,1] = if dem[p,first] < iinv[p] then 0 else dem[p,first] - iinv[p] endif);

constraint forall(p in prod, t in floor(first + 1)..last)(Rprod[p,t] + Oprod[p,t] + Short[p,t] - Short[p,t - 1] + sum(a in 1..life)((Inv[p,t - 1,a] - Inv[p,t,a])) = if dem[p,t] < iil[p,t - 1] then 0 else dem[p,t] - iil[p,t - 1] endif);

constraint forall(p in prod, t in time)(sum(a in 1..life)(Inv[p,t,a] + iil[p,t]) >= minv[p,t]);

constraint forall(p in prod, v in 1..floor(life - 1), a in floor(v + 1)..life)(Inv[p,first + v - 1,a] = 0);

constraint forall(p in prod, t in time)(Inv[p,t,1] <= Rprod[p,t] + Oprod[p,t]);

constraint forall(p in prod, t in floor(first + 1)..last, a in 2..life)(Inv[p,t,a] <= Inv[p,t - 1,a - 1]);



solve minimize sum(t in time)(rtr * sl * dpp[t] * cs * Crews[t] + sum(t in time)(hc[t] * Hire[t] + sum(t in time)(lc[t] * Layoff[t] + sum(t in time, p in prod)(otr * cs * pt[p] * Oprod[p,t] + sum(t in time, p in prod, a in 1..life)(cri[p] * pc[p] * Inv[p,t,a] + sum(t in time, p in prod)(crs[p] * pc[p] * Short[p,t]))))));




