set of int: D_CITY;

array[INDEX_SET_DW_LINKS, 1..2] of W_CITY: DW_LINKS;

set of int: W_CITY;

array[D_CITY] of float: pd_cost;

array[int, int] of float: dw_cost;

float: p_supply;

array[W_CITY] of float: w_demand;

array[D_CITY] of float: pd_cap;

array[int, int] of float: dw_cap;


array[D_CITY] of var float: PD_Ship;

array[INDEX_SET_DW_Ship_1, INDEX_SET_DW_Ship_2] of var float: DW_Ship;

set of int: INDEX_SET_DW_LINKS;

set of int: INDEX_SET_DW_Ship_1 = DW_LINKS;

set of int: INDEX_SET_DW_Ship_2;


constraint forall(dc in D_CITY)(assert(pd_cost[dc] >= 0, "Assertion pd_cost[\(dc)] >= 0 failed!"));

constraint forall(dl1 in INDEX_SET_DW_LINKS)(assert(dw_cost[DW_LINKS[dl1,1],DW_LINKS[dl1,2]] >= 0, "Assertion dw_cost[\(DW_LINKS[dl1,1]),\(DW_LINKS[dl1,2])] >= 0 failed!"));

constraint assert(p_supply >= 0, "Assertion p_supply >= 0 failed!");

constraint forall(wc in W_CITY)(assert(w_demand[wc] >= 0, "Assertion w_demand[\(wc)] >= 0 failed!"));

constraint forall(dc in D_CITY)(assert(pd_cap[dc] >= 0, "Assertion pd_cap[\(dc)] >= 0 failed!"));

constraint forall(dl1 in INDEX_SET_DW_LINKS)(assert(dw_cap[DW_LINKS[dl1,1],DW_LINKS[dl1,2]] >= 0, "Assertion dw_cap[\(DW_LINKS[dl1,1]),\(DW_LINKS[dl1,2])] >= 0 failed!"));

constraint forall(i in D_CITY)(PD_Ship[i] <= pd_cap[i] /\ PD_Ship[i] >= 0);

constraint forall(i in INDEX_SET_DW_LINKS)(DW_Ship[DW_LINKS[i,1],DW_LINKS[i,2]] <= dw_cap[DW_LINKS[i,1],DW_LINKS[i,2]] /\ DW_Ship[DW_LINKS[i,1],DW_LINKS[i,2]] >= 0);

constraint sum(i in D_CITY)(PD_Ship[i]) = p_supply;

constraint forall(i in D_CITY)(PD_Ship[i] = sum(i in INDEX_SET_DW_LINKS)(DW_Ship[DW_LINKS[i,1],DW_LINKS[i,2]]));

constraint forall(j in W_CITY)(sum(i in INDEX_SET_DW_LINKS)(DW_Ship[DW_LINKS[i,1],DW_LINKS[i,2]]) = w_demand[j]);



solve minimize sum(i in D_CITY)(pd_cost[i] * PD_Ship[i] + sum(i in INDEX_SET_DW_LINKS)(dw_cost[DW_LINKS[i,1],DW_LINKS[i,2]] * DW_Ship[DW_LINKS[i,1],DW_LINKS[i,2]]));




