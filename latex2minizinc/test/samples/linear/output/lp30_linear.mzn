set of int: time = first..last;

enum prod;

float: rtr;

float: sl;

array[time] of float: dpp;

int: cs;

array[time] of float: hc;

array[time] of float: lc;

float: otr;

array[prod] of float: pt;

int: life;

array[prod] of float: cri;

array[prod] of float: pc;

array[prod] of float: crs;

array[time] of float: ol;

int: first;

int: iw;

array[time] of float: cmin;

array[time] of float: cmax;

array[prod, first..floor(last + 1)] of float: dem;

array[prod] of float: iinv;

array[prod, time] of float: iil = array2d(prod, time, [if iinv[p] < sum(v in first..t)(dem[p,v]) then 0 else iinv[p] - sum(v in first..t)(dem[p,v]) endif | p in prod, t in time]);

int: last;

array[prod, time] of float: minv = array2d(prod, time, [dem[p,t + 1] * (if pro[p,t + 1] = true then pir else rir endif) | p in prod, t in time]);

float: rir;

float: pir;

array[prod, first..floor(last + 1)] of bool: pro;


array[floor(first - 1)..last] of var float: Crews;

array[time] of var float: Hire;

array[time] of var float: Layoff;

array[prod, time] of var float: Rprod;

array[prod, time] of var float: Oprod;

array[prod, time] of var float: Short;

array[prod, time, 1..life] of var float: Inv;


constraint assert(rtr > 0, "Assertion rtr > 0 failed!");

constraint assert(sl > 0, "Assertion sl > 0 failed!");

constraint forall(t in time)(assert(dpp[t] > 0, "Assertion dpp[\(t)] > 0 failed!"));

constraint assert(cs > 0, "Assertion cs > 0 failed!");

constraint forall(t in time)(assert(hc[t] >= 0, "Assertion hc[\(t)] >= 0 failed!"));

constraint forall(t in time)(assert(lc[t] >= 0, "Assertion lc[\(t)] >= 0 failed!"));

constraint assert(otr > rtr, "Assertion otr > rtr failed!");

constraint forall(p in prod)(assert(pt[p] > 0, "Assertion pt[\(p)] > 0 failed!"));

constraint assert(life > 0, "Assertion life > 0 failed!");

constraint forall(p in prod)(assert(cri[p] > 0, "Assertion cri[\(p)] > 0 failed!"));

constraint forall(p in prod)(assert(pc[p] > 0, "Assertion pc[\(p)] > 0 failed!"));

constraint forall(p in prod)(assert(crs[p] > 0, "Assertion crs[\(p)] > 0 failed!"));

constraint forall(t in time)(assert(ol[t] >= 0, "Assertion ol[\(t)] >= 0 failed!"));

constraint assert(first > 0, "Assertion first > 0 failed!");

constraint assert(iw >= 0, "Assertion iw >= 0 failed!");

constraint forall(t in time)(assert(cmin[t] >= 0, "Assertion cmin[\(t)] >= 0 failed!"));

constraint forall(t in time)(assert(cmax[t] >= cmin[t], "Assertion cmax[\(t)] >= cmin[\(t)] failed!"));

constraint forall(p in prod, i in first..floor(last + 1))(assert(dem[p,i] >= 0, "Assertion dem[\(p),\(i)] >= 0 failed!"));

constraint forall(p in prod)(assert(iinv[p] >= 0, "Assertion iinv[\(p)] >= 0 failed!"));

constraint assert(last > first, "Assertion last > first failed!");

constraint assert(rir >= 0, "Assertion rir >= 0 failed!");

constraint assert(pir >= 0, "Assertion pir >= 0 failed!");

constraint forall(i in floor(first - 1)..last)(Crews[i] >= 0);

constraint forall(t in time)(Hire[t] >= 0);

constraint forall(t in time)(Layoff[t] >= 0);

constraint forall(p in prod, t in time)(Rprod[p,t] >= 0);

constraint forall(p in prod, t in time)(Oprod[p,t] >= 0);

constraint forall(p in prod, t in time)(Short[p,t] >= 0);

constraint forall(p in prod, t in time, j in 1..life)(Inv[p,t,j] >= 0);

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




