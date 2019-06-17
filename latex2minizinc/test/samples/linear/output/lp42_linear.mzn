enum proc;

set of int: m_raw;

set of int: crude;

set of int: m_purch;

array[INDEX_SET_blend, 1..2] of m_inter: blend;

set of int: m_inter;

set of int: m_final;

enum qual;

enum unit;

array[m_raw union m_inter, crude, proc] of float: io;

array[m_inter, crude, qual] of float: attr = array3d(m_inter, crude, qual, [if attr_crude[mi,c,q] > 0 then attr_crude[mi,c,q] else attr_both[mi,q] endif | mi in m_inter, c in crude, q in qual]);

array[m_final, qual] of float: attr_min;

array[m_final, qual] of float: attr_max;

array[unit, proc] of float: util;

array[unit] of float: cap;

array[crude] of float: purch_max;

array[crude union m_purch union m_final] of float: price;

array[proc] of float: cost;

array[m_final, qual] of float: attr_both;

array[m_inter, crude, qual] of float: attr_crude;


array[crude] of var float: InCr;

array[m_purch, crude] of var float: InInt;

array[proc, crude] of var float: LevPr;

array[INDEX_SET_LevBl_1, INDEX_SET_LevBl_2, crude] of var float: LevBl;

array[m_final] of var float: Out;

var float: Revenue;

var float: PurchCost;

var float: OperCost;

set of int: INDEX_SET_LevBl_1 = blend;

set of int: INDEX_SET_LevBl_2 = crude;

set of int: INDEX_SET_blend;

set of int: INDEX_SET_m_raw_union_m_inter;

array[INDEX_SET_m_raw_union_m_inter] of int: m_raw_union_m_inter;


constraint forall(mf in m_final, q in qual)(assert(attr_min[mf,q] >= 0, "Assertion attr_min[\(mf),\(q)] >= 0 failed!"));

constraint forall(mf in m_final, q in qual)(assert(attr_max[mf,q] >= 0, "Assertion attr_max[\(mf),\(q)] >= 0 failed!"));

constraint forall(u in unit)(assert(cap[u] >= 0, "Assertion cap[\(u)] >= 0 failed!"));

constraint forall(c in crude)(assert(purch_max[c] > 0, "Assertion purch_max[\(c)] > 0 failed!"));

constraint forall(cm in crude union m_purch union m_final)(assert(price[cm] > 0, "Assertion price[\(cm)] > 0 failed!"));

constraint forall(p in proc)(assert(cost[p] > 0, "Assertion cost[\(p)] > 0 failed!"));

constraint forall(mf in m_final, q in qual)(assert(attr_both[mf,q] >= 0, "Assertion attr_both[\(mf),\(q)] >= 0 failed!"));

constraint forall(mi in m_inter, c in crude, q in qual)(assert(attr_crude[mi,c,q] >= 0, "Assertion attr_crude[\(mi),\(c),\(q)] >= 0 failed!"));

constraint forall(c in crude)(InCr[c] >= 0);

constraint forall(mp in m_purch, c in crude)(InInt[mp,c] >= 0);

constraint forall(p in proc, c in crude)(LevPr[p,c] >= 0);

constraint forall(i in INDEX_SET_blend, c in INDEX_SET_LevBl_2)(LevBl[blend[i,1],c,c] >= 0);

constraint forall(mf in m_final)(Out[mf] >= 0);

constraint forall(mr in m_raw, c in crude)(sum(p in proc)(io[mr,c,p] * LevPr[p,c] + InCr[c]) >= 0);

constraint forall(mi in m_inter, c in crude)(sum(p in proc)(io[mi,c,p] * LevPr[p,c] + (if mi in m_purch then InInt[mi,c] else 0 endif)) >= sum(mf in INDEX_SET_blend)(LevBl[blend[mf,1],blend[mf,2],c]));

constraint forall(mf in m_final)(Out[mf] = sum(mf in INDEX_SET_blend, c in crude)(LevBl[blend[mf,1],blend[mf,2],c]));

constraint forall(mf in m_final, q in qual where attr_min[mf,q] != 0)(sum(mi in m_inter, c in crude where mf in INDEX_SET_blend)(attr[mi,c,q] * LevBl[mf,mi,c]) >= attr_min[mf,q] * Out[mf]);

constraint forall(mf in m_final, q in qual where attr_max[mf,q] != 0)(sum(mi in m_inter, c in crude where mf in INDEX_SET_blend)(attr[mi,c,q] * LevBl[mf,mi,c]) <= attr_max[mf,q] * Out[mf]);

constraint forall(u in unit)(sum(p in proc)((util[u,p] * sum(c in crude)(LevPr[p,c]))) <= cap[u]);

constraint forall(c in crude)(InCr[c] <= purch_max[c]);

constraint Revenue = sum(mf in m_final)(price[mf] * Out[mf]);

constraint PurchCost = sum(c in crude)(price[c] * InCr[c] + sum(mp in m_purch, c in crude)(price[mp] * InInt[mp,c]));

constraint OperCost = sum(p in proc)((cost[p] * sum(c in crude)(LevPr[p,c])));



solve maximize Revenue - PurchCost - OperCost;




