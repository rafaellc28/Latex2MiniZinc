enum prod;

enum fact;

array[INDEX_SET_rt, 1..2] of dctr: rt;

enum dctr;

enum whse;

array[int, int] of float: rpc;

array[int, int] of float: opc;

array[int, int] of float: sc;

array[int] of float: wt;

array[int] of float: tc;

float: rtmin;

array[int, int] of float: pt;

array[int] of float: dp;

array[int] of float: hd;

float: rtmax;

float: otmin;

float: otmax;

array[int] of float: rmin;

array[int] of float: rmax;

array[int] of float: omin;

array[int] of float: omax;

array[INDEX_SET_dem_1, INDEX_SET_dem_2] of float: dem = array2d(INDEX_SET_dem_1, INDEX_SET_dem_2, [dt[p] * ds[p,w]/dstot[p] | p in prod, w in whse]);

array[int] of float: dsr;

array[int] of float: dt;

array[int, int] of float: ds;

float: huge;

array[int] of float: cpp;

array[int, int] of float: msr;

array[INDEX_SET_dstot_1] of float: dstot = array1d(INDEX_SET_dstot_1, [sum(w in whse)(ds[p,w]) | p in prod]);


array[INDEX_SET_Rprod_1, INDEX_SET_Rprod_2] of var float: Rprod;

array[INDEX_SET_Oprod_1, INDEX_SET_Oprod_2] of var float: Oprod;

array[INDEX_SET_Ship_1, INDEX_SET_Ship_2, INDEX_SET_Ship_3] of var float: Ship;

array[INDEX_SET_Trans_1, INDEX_SET_Trans_2] of var float: Trans;

set of int: INDEX_SET_Oprod_1 = prod;

set of int: INDEX_SET_Oprod_2 = fact;

set of int: INDEX_SET_Rprod_1 = prod;

set of int: INDEX_SET_Rprod_2 = fact;

set of int: INDEX_SET_Ship_1 = prod;

set of int: INDEX_SET_Ship_2 = rt;

set of int: INDEX_SET_Ship_3;

set of int: INDEX_SET_Trans_1 = prod;

set of int: INDEX_SET_Trans_2 = dctr;

set of int: INDEX_SET_dem_1;

set of int: INDEX_SET_dem_2;

set of int: INDEX_SET_dstot_1;

set of int: INDEX_SET_rt;


constraint forall(p in INDEX_SET_Rprod_1, f in INDEX_SET_Rprod_2)(Rprod[p,f] >= 0);

constraint forall(p in INDEX_SET_Oprod_1, f in INDEX_SET_Oprod_2)(Oprod[p,f] >= 0);

constraint forall(p in INDEX_SET_Ship_1, v in INDEX_SET_rt)(Ship[p,rt[v,1],rt[v,2]] >= 0);

constraint forall(p in INDEX_SET_Trans_1, d in INDEX_SET_Trans_2)(Trans[p,d] >= 0);

constraint sum(p in prod, f in fact)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) <= rtmax /\ sum(p in prod, f in fact)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) >= rtmin;

constraint sum(p in prod, f in fact)(pt[p,f] * Oprod[p,f]) <= otmax /\ sum(p in prod, f in fact)(pt[p,f] * Oprod[p,f]) >= otmin;

constraint forall(f in fact)(sum(p in prod)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) <= rmax[f] /\ sum(p in prod)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) >= rmin[f]);

constraint forall(f in fact)(sum(p in prod)(pt[p,f] * Oprod[p,f]) <= omax[f] /\ sum(p in prod)(pt[p,f] * Oprod[p,f]) >= omin[f]);

constraint forall(p in prod, w in whse)(sum(v in INDEX_SET_rt)(Ship[p,rt[v,1],rt[v,2]] + (if rt[v,2] in fact then Rprod[p,rt[v,2]] + Oprod[p,rt[v,2]] else 0 endif)) = dem[p,w] + (if w in dctr then sum(w in INDEX_SET_rt)(Ship[p,rt[w,1],rt[w,2]]) else 0 endif));

constraint forall(p in prod, d in dctr)(Trans[p,d] >= sum(d in INDEX_SET_rt)(Ship[p,rt[d,1],rt[d,2]] - (if rt[d,1] in fact then Rprod[p,rt[d,1]] + Oprod[p,rt[d,1]] else 0 endif)));



solve minimize sum(p in prod, f in fact)(rpc[p,f] * Rprod[p,f] + sum(p in prod, f in fact)(opc[p,f] * Oprod[p,f] + sum(p in prod, d in INDEX_SET_rt)(sc[rt[d,1],rt[d,2]] * wt[p] * Ship[p,rt[d,1],rt[d,2]] + sum(p in prod, d in dctr)(tc[p] * Trans[p,rt[d,1]]))));




