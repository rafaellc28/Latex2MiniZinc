set of int: cFinal;

set of int: port;

enum nutr;

enum region;

array[plant] of set of int: pPos = array1d(plant, [pCappl_diff_pExceptpl[pl] | pl in plant]);

set of int: cShip;

set of int: cRaw;

set of int: commod = cFinal union cInter union cRaw;

set of int: plant;

array[INDEX_SET_mPos] of set of int: mPos;

set of int: center;

set of int: cInter;

set of int: proc;

enum unit;

array[plant] of set of int: pExcept;

array[commod] of set of int: cPos = array1d(commod, [cpPosc_union_ccPosc[c] | c in commod]);

array[cFinal, nutr] of float: fn;

array[region, nutr] of float: cn75 = array2d(region, nutr, [sum(c in cFinal)(cf75[r,c] * fn[c,n]) | r in region, n in nutr]);

array[region, cFinal] of float: cf75;

array[commod, proc] of float: io;

array[commod] of float: pImp;

array[plant, cRaw] of float: pDom = array2d(plant, cRaw, [if pR[c] > 0 then pR[c] else pPr[pl,c] endif | pl in plant, c in cRaw]);

array[unit, proc] of float: util;

float: utilPct = 0.85;

array[unit, plant] of float: icap = array2d(unit, plant, [0.33 * dcap[pl,u] | u in unit, pl in plant]);

array[plant, region] of float: tranFinal = array2d(plant, region, [if road[r,pl] > 0 then 0.5 + 0.0144 * road[r,pl] else 0 endif | pl in plant, r in region]);

array[region, port] of float: tranImport = array2d(region, port, [if road[r,po] > 0 then 0.5 + 0.0144 * road[r,po] else 0 endif | r in region, po in port]);

array[plant, plant] of float: tranInter = array2d(plant, plant, [if rail[p1,p2] > 0 then 3.5 + 0.03 * rail[p1,p2] else 0 endif | p1,p2 in plant]);

array[plant] of float: tranRaw = array1d(plant, [(if impdBarg[pl] > 0 then 1.0 + 0.0030 * impdBarg[pl] else 0 endif) + (if impdRoad[pl] > 0 then 0.5 + 0.0144 * impdRoad[pl] else 0 endif) | pl in plant]);

float: exch = 0.4;

array[region, center] of float: road;

array[plant, plant] of float: railHalf;

array[plant, plant] of float: rail = array2d(plant, plant, [if railHalf[p1,p2] > 0 then railHalf[p1,p2] else railHalf[p2,p1] endif | p1,p2 in plant]);

array[plant] of float: impdBarg;

array[plant] of float: impdRoad;

array[cRaw] of float: pR;

array[plant, cRaw] of float: pPr;

array[plant, unit] of float: dcap;

array[plant] of set of int: pCap;

array[commod] of set of int: cpPos;

array[commod] of set of int: ccPos;


var float: Psip;

var float: Psil;

var float: Psii;

array[cFinal, INDEX_SET_Xf_2, region] of var float: Xf;

array[cFinal, region, port] of var float: Vf;

array[plant, INDEX_SET_Z_2] of var float: Z;

array[cShip, INDEX_SET_Xi_2, INDEX_SET_Xi_3] of var float: Xi;

array[cRaw, INDEX_SET_Vr_2] of var float: Vr;

array[cRaw, INDEX_SET_U_2] of var float: U;

set of int: INDEX_SET_U_2;

set of int: INDEX_SET_Vr_2;

set of int: INDEX_SET_Xf_2;

set of int: INDEX_SET_Xi_2;

set of int: INDEX_SET_Xi_3;

set of int: INDEX_SET_Z_2;

set of int: INDEX_SET_cpPosc_union_ccPosc;

set of int: INDEX_SET_mPos;

set of int: INDEX_SET_pCappl_diff_pExceptpl;

array[INDEX_SET_cpPosc_union_ccPosc] of int: cpPosc_union_ccPosc;

array[INDEX_SET_pCappl_diff_pExceptpl] of int: pCappl_diff_pExceptpl;


constraint forall(cf in cFinal, n in nutr)(assert(fn[cf,n] >= 0, "Assertion fn[\(cf),\(n)] >= 0 failed!"));

constraint forall(r in region, cf in cFinal)(assert(cf75[r,cf] >= 0, "Assertion cf75[\(r),\(cf)] >= 0 failed!"));

constraint forall(c in commod)(assert(pImp[c] >= 0, "Assertion pImp[\(c)] >= 0 failed!"));

constraint forall(u in unit, p in proc)(assert(util[u,p] >= 0, "Assertion util[\(u),\(p)] >= 0 failed!"));

constraint forall(r in region, c in center)(assert(road[r,c] >= 0, "Assertion road[\(r),\(c)] >= 0 failed!"));

constraint forall(p1 in plant, p2 in plant)(assert(railHalf[p1,p2] >= 0, "Assertion railHalf[\(p1),\(p2)] >= 0 failed!"));

constraint forall(p in plant)(assert(impdBarg[p] >= 0, "Assertion impdBarg[\(p)] >= 0 failed!"));

constraint forall(p in plant)(assert(impdRoad[p] >= 0, "Assertion impdRoad[\(p)] >= 0 failed!"));

constraint forall(cr in cRaw)(assert(pR[cr] >= 0, "Assertion pR[\(cr)] >= 0 failed!"));

constraint forall(p in plant, cr in cRaw)(assert(pPr[p,cr] >= 0, "Assertion pPr[\(p),\(cr)] >= 0 failed!"));

constraint forall(p in plant, u in unit)(assert(dcap[p,u] >= 0, "Assertion dcap[\(p),\(u)] >= 0 failed!"));

constraint forall(c in cFinal, pl in INDEX_SET_Xf_2, r in region)(Xf[c,pl,r] >= 0);

constraint forall(c in cFinal, r in region, po in port)(Vf[c,r,po] >= 0);

constraint forall(pl in plant, pr in INDEX_SET_Z_2)(Z[pl,pr] >= 0);

constraint forall(c in cShip, p1 in INDEX_SET_Xi_2, p2 in INDEX_SET_Xi_3)(Xi[c,p1,p2] >= 0);

constraint forall(c in cRaw, pl in INDEX_SET_Vr_2)(Vr[c,pl] >= 0);

constraint forall(c in cRaw, pl in INDEX_SET_U_2)(U[c,pl] >= 0);

constraint forall(n in nutr, r in region)(sum(c in cFinal)(fn[c,n] * (sum(po in port)(Vf[c,r,po] + sum(pl in cpPos[c])(Xf[c,pl,r])))) >= cn75[r,n]);

constraint forall(c in cFinal, r in region where cf75[r,c] > 0)(sum(po in port)(Vf[c,r,po] + sum(pl in cpPos[c])(Xf[c,pl,r])) >= cf75[r,c]);

constraint forall(c in commod, pl in plant)(sum(pr in pPos[pl])(io[c,pr] * Z[pl,pr] + (if c in cShip then (if pl in cpPos[c] then sum(p2 in ccPos[c])(Xi[c,pl,p2]) else 0 endif) - (if pl in ccPos[c] then sum(p2 in cpPos[c])(Xi[c,p2,pl]) else 0 endif) else 0 endif) + (if c in cRaw /\ pl in ccPos[c] then ((if pImp[c] > 0 then Vr[c,pl] else 0 endif) + (if pDom[pl,c] > 0 then U[c,pl] else 0 endif)) else 0 endif)) >= if c in cFinal /\ pl in cpPos[c] then sum(r in region)(Xf[c,pl,r]) else 0 endif);

constraint forall(pl in plant, u in mPos[pl])(sum(pr in pPos[pl])(util[to_enum(unit,u),pr] * Z[pl,pr]) <= utilPct * icap[to_enum(unit,u),pl]);

constraint Psip = sum(c in cRaw, pl in ccPos[c])(pDom[pl,c] * U[c,pl]);

constraint Psil = sum(c in cFinal)((sum(pl in cpPos[c], r in region)(tranFinal[pl,r] * Xf[c,pl,r] + sum(po in port, r in region)(tranImport[r,po] * Vf[c,r,po]))) + sum(c in cShip, p1 in cpPos[c], p2 in ccPos[c])(tranInter[p1,p2] * Xi[c,p1,p2] + sum(c in cRaw, pl in ccPos[c] where pImp[c] > 0)(tranRaw[pl] * Vr[c,pl])));

constraint Psii / exch = sum(c in cFinal, r in region, po in port)(pImp[c] * Vf[c,r,po] + sum(c in cRaw, pl in ccPos[c])(pImp[c] * Vr[c,pl]));



solve minimize Psip + Psil + Psii;




