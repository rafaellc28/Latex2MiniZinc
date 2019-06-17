enum PROD;

enum WEEKS;

array[PROD, WEEKS] of float: revenue;

array[PROD, WEEKS] of float: Sell;

array[PROD] of float: prodcost;

array[PROD, WEEKS] of float: Make;

array[PROD] of float: invcost;

array[PROD, WEEKS] of float: Inv;

array[PROD] of float: rate;

array[WEEKS] of float: avail;

array[PROD] of float: inv0;

array[PROD, WEEKS] of float: market;


constraint forall(p in PROD, w in WEEKS)(assert(revenue[p,w] >= 0, "Assertion revenue[\(p),\(w)] >= 0 failed!"));

constraint forall(p in PROD, w in WEEKS)(assert(Sell[p,w] <= market[p,w] /\ Sell[p,w] >= 0, "Assertion Sell[\(p),\(w)] <= market[\(p),\(w)] /\\ Sell[\(p),\(w)] >= 0 failed!"));

constraint forall(p in PROD)(assert(prodcost[p] >= 0, "Assertion prodcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD, w in WEEKS)(assert(Make[p,w] >= 0, "Assertion Make[\(p),\(w)] >= 0 failed!"));

constraint forall(p in PROD)(assert(invcost[p] >= 0, "Assertion invcost[\(p)] >= 0 failed!"));

constraint forall(p in PROD, w in WEEKS)(assert(Inv[p,w] >= 0, "Assertion Inv[\(p),\(w)] >= 0 failed!"));

constraint forall(w in WEEKS)(assert(avail[w] >= 0, "Assertion avail[\(w)] >= 0 failed!"));

constraint forall(p in PROD)(assert(inv0[p] >= 0, "Assertion inv0[\(p)] >= 0 failed!"));

constraint forall(p in PROD, w in WEEKS)(assert(market[p,w] >= 0, "Assertion market[\(p),\(w)] >= 0 failed!"));

constraint forall(t in WEEKS)(sum(p in PROD)((1/rate[p]) * Make[p,t]) <= avail[t]);

constraint forall(p in PROD)(Make[p,WEEKS[0]] + inv0[p] = Sell[p,WEEKS[0]] + Inv[p,WEEKS[0]]);

constraint forall(p in PROD, t in WEEKS where t > 1)(Make[p,t] + Inv[p,enum_prev(WEEKS,t)] = Sell[p,t] + Inv[p,t]);

constraint forall(p in PROD)(rate[p] > 0);



solve maximize sum(p in PROD, t in WEEKS)((revenue[p,t] * Sell[p,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]));




