enum time;

enum prd;

float: Rtr;

float: Sl;

array[int] of float: Dpp;

array[int] of float: Hc;

array[int] of float: Lc;

float: Otr;

array[int] of float: Pt;

array[int] of float: Cri;

array[int] of float: Pc;

array[int] of float: Crs;

int: Cs;

array[int] of float: Ol;

time: First;

int: Iw;

array[int] of float: Cmin;

array[int] of float: Cmax;

array[int, int] of float: Dem;

array[int] of float: Iinv;

array[int, int] of float: Iil;

int: Last;

int: Life;

array[int, int] of float: Minv;


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


constraint forall(t in floor(First - 1)..Last)(Crews[t] >= 0);

constraint forall(t in time)(Hire[t] >= 0);

constraint forall(t in time)(Layoff[t] >= 0);

constraint forall(p in prd, t in time)(Oprd[p,t] >= 0);

constraint forall(p in prd, t in time, a in 1..Life)(Inv[p,t,a] >= 0);

constraint forall(p in prd, t in time)(Short[p,t] >= 0);

constraint forall(p in prd, t in time)(Rprd[p,t] >= 0);

constraint forall(t in time)(sum(p in prd)(Pt[p] * Rprd[p,t]) <= Sl * Dpp[t] * Crews[t]);

constraint forall(t in time)(sum(p in prd)(Pt[p] * Oprd[p,t]) <= Ol[t]);

constraint Crews[First - 1] = Iw;

constraint forall(t in time)(Crews[t] = Crews[t - 1] + Hire[t] - Layoff[t]);

constraint forall(t in time)(Crews[t] <= Cmax[t] /\ Crews[t] >= Cmin[t]);

constraint forall(p in prd)(Rprd[p,First] + Oprd[p,First] + Short[p,First] - Inv[p,First,1] = Dem[p,First] less Iinv[p]);

constraint forall(p in prd, t in floor(First + 1)..Last)(Rprd[p,to_enum(time,t)] + Oprd[p,to_enum(time,t)] + Short[p,to_enum(time,t)] - Short[p,to_enum(time,t) - 1] + sum(a in 1..Life)((Inv[p,to_enum(time,t) - 1,a] - Inv[p,to_enum(time,t),a])) = Dem[p,t] less Iil[p,to_enum(time,t) - 1]);

constraint forall(p in prd, t in time)(sum(a in 1..Life)(Inv[p,t,a] + Iil[p,t]) >= Minv[p,t]);

constraint forall(p in prd, v in 1..floor(Life - 1), a in floor(v + 1)..Life)(Inv[p,First + to_enum(time,v) - 1,a] = 0);

constraint forall(p in prd, t in time)(Inv[p,t,1] <= Rprd[p,t] + Oprd[p,t]);

constraint forall(p in prd, t in floor(First + 1)..Last, a in 2..Life)(Inv[p,to_enum(time,t),a] <= Inv[p,to_enum(time,t) - 1,a - 1]);

constraint forall(p in prd, t in time, a in 1..Life)(Inv[p,t,a] >= 0);

constraint forall(p in prd, t in time)(Short[p,t] >= 0);

constraint forall(t in floor(First - 1)..Last)(Crews[t] >= 0);

constraint forall(p in prd, t in First..floor(Last + 1))(Dem[p,t] >= 0);



var float: obj = sum(t in time)(Rtr * Sl * Dpp[t] * Cs * Crews[t] + sum(t in time)(Hc[t] * Hire[t] + sum(t in time)(Lc[t] * Layoff[t] + sum(t in time, p in prd)(Otr * Cs * Pt[p] * Oprd[p,t] + sum(t in time, p in prd, a in 1..Life)(Cri[p] * Pc[p] * Inv[p,t,a] + sum(t in time, p in prd)(Crs[p] * Pc[p] * Short[p,t]))))));

solve minimize obj;




