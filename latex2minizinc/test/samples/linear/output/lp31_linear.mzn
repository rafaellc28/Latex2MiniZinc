enum prod;

enum fact;

array[INDEX_SET_rt, 1..2] of dctr: rt;

enum dctr;

enum whse;

array[prod, fact] of float: rpc;

array[prod, fact] of float: opc;

array[dctr, whse] of float: sc;

array[prod] of float: wt;

array[prod] of float: tc;

float: rtmin;

array[prod, fact] of float: pt;

array[fact] of float: dp;

array[fact] of float: hd;

float: rtmax;

float: otmin;

float: otmax;

array[fact] of float: rmin;

array[fact] of float: rmax;

array[fact] of float: omin;

array[fact] of float: omax;

array[prod, whse] of float: dem = array2d(prod, whse, [dt[p] * ds[p,w]/dstot[p] | p in prod, w in whse]);

array[dctr] of float: dsr;

array[prod] of float: dt;

array[prod, whse] of float: ds;

float: huge;

array[prod] of float: cpp;

array[dctr, whse] of float: msr;

array[prod] of float: dstot = array1d(prod, [sum(w in whse)(ds[p,w]) | p in prod]);


array[prod, fact] of var float: Rprod;

array[prod, fact] of var float: Oprod;

array[prod, INDEX_SET_Ship_2, INDEX_SET_Ship_3] of var float: Ship;

array[prod, dctr] of var float: Trans;

set of int: INDEX_SET_Ship_2 = rt;

set of int: INDEX_SET_Ship_3;

set of int: INDEX_SET_rt;


constraint forall(p in prod, f in fact)(assert(rpc[p,f] >= 0, "Assertion rpc[\(p),\(f)] >= 0 failed!"));

constraint forall(p in prod, f in fact)(assert(opc[p,f] >= 0, "Assertion opc[\(p),\(f)] >= 0 failed!"));

constraint forall(d in dctr, w in whse)(assert(sc[d,w] >= 0, "Assertion sc[\(d),\(w)] >= 0 failed!"));

constraint forall(p in prod)(assert(wt[p] > 0, "Assertion wt[\(p)] > 0 failed!"));

constraint forall(p in prod)(assert(tc[p] >= 0, "Assertion tc[\(p)] >= 0 failed!"));

constraint assert(rtmin >= 0, "Assertion rtmin >= 0 failed!");

constraint forall(p in prod, f in fact)(assert(pt[p,f] >= 0, "Assertion pt[\(p),\(f)] >= 0 failed!"));

constraint forall(f in fact)(assert(dp[f] > 0, "Assertion dp[\(f)] > 0 failed!"));

constraint forall(f in fact)(assert(hd[f] >= 0, "Assertion hd[\(f)] >= 0 failed!"));

constraint assert(otmin >= 0, "Assertion otmin >= 0 failed!");

constraint forall(f in fact)(assert(rmin[f] >= 0, "Assertion rmin[\(f)] >= 0 failed!"));

constraint forall(f in fact)(assert(omin[f] >= 0, "Assertion omin[\(f)] >= 0 failed!"));

constraint forall(d in dctr)(assert(dsr[d] >= 0, "Assertion dsr[\(d)] >= 0 failed!"));

constraint forall(p in prod)(assert(dt[p] >= 0, "Assertion dt[\(p)] >= 0 failed!"));

constraint forall(p in prod, w in whse)(assert(ds[p,w] >= 0, "Assertion ds[\(p),\(w)] >= 0 failed!"));

constraint assert(huge > 0, "Assertion huge > 0 failed!");

constraint forall(p in prod)(assert(cpp[p] > 0, "Assertion cpp[\(p)] > 0 failed!"));

constraint forall(p in prod, f in fact)(Rprod[p,f] >= 0);

constraint forall(p in prod, f in fact)(Oprod[p,f] >= 0);

constraint forall(p in prod, v in INDEX_SET_rt)(Ship[p,rt[v,1],rt[v,2]] >= 0);

constraint forall(p in prod, d in dctr)(Trans[p,d] >= 0);

constraint sum(p in prod, f in fact)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) <= rtmax /\ sum(p in prod, f in fact)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) >= rtmin;

constraint sum(p in prod, f in fact)(pt[p,f] * Oprod[p,f]) <= otmax /\ sum(p in prod, f in fact)(pt[p,f] * Oprod[p,f]) >= otmin;

constraint forall(f in fact)(sum(p in prod)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) <= rmax[f] /\ sum(p in prod)((pt[p,f] * Rprod[p,f])/(dp[f] * hd[f])) >= rmin[f]);

constraint forall(f in fact)(sum(p in prod)(pt[p,f] * Oprod[p,f]) <= omax[f] /\ sum(p in prod)(pt[p,f] * Oprod[p,f]) >= omin[f]);

constraint forall(p in prod, w in whse)(sum(v in INDEX_SET_rt)(Ship[p,rt[v,1],rt[v,2]] + (if rt[v,2] in fact then Rprod[p,to_enum(fact,rt[v,2])] + Oprod[p,to_enum(fact,rt[v,2])] else 0 endif)) = dem[p,w] + (if w in dctr then sum(w in INDEX_SET_rt)(Ship[p,rt[w,1],rt[w,2]]) else 0 endif));

constraint forall(p in prod, d in dctr)(Trans[p,d] >= sum(d in INDEX_SET_rt)(Ship[p,rt[d,1],rt[d,2]] - (if rt[d,1] in fact then Rprod[p,to_enum(fact,rt[d,1])] + Oprod[p,to_enum(fact,rt[d,1])] else 0 endif)));



solve minimize sum(p in prod, f in fact)(rpc[p,f] * Rprod[p,f] + sum(p in prod, f in fact)(opc[p,f] * Oprod[p,f] + sum(p in prod, d in INDEX_SET_rt)(sc[rt[d,1],to_enum(whse,rt[d,2])] * wt[p] * Ship[p,rt[d,1],rt[d,2]] + sum(p in prod, d in dctr)(tc[p] * Trans[p,rt[d,1]]))));




