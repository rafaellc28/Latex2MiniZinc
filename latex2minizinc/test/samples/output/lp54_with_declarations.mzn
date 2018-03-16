set of int: cFinal;

enum port;

array[INDEX_SET_cpPos] of set of int: cpPos;

enum nutr;

enum region;

array[INDEX_SET_pPos_1] of set of int: pPos = array1d(INDEX_SET_pPos_1, [pCappl_diff_pExceptpl[pl] | pl in plant]);

enum cShip;

array[INDEX_SET_ccPos] of set of int: ccPos;

set of int: cRaw;

set of int: commod = cFinal union cInter union cRaw;

enum plant;

array[INDEX_SET_mPos] of set of int: mPos;

enum center;

set of int: cInter;

enum proc;

enum unit;

array[int] of set of int: pCap;

array[int] of set of int: pExcept;

array[INDEX_SET_cPos_1] of set of int: cPos = array1d(INDEX_SET_cPos_1, [cpPosc_union_ccPosc[c] | c in commod]);

array[int, int] of float: fn;

array[INDEX_SET_cn75_1, INDEX_SET_cn75_2] of float: cn75 = array2d(INDEX_SET_cn75_1, INDEX_SET_cn75_2, [sum(c in cFinal)(cf75[r,c] * fn[c,n]) | r in region, n in nutr]);

array[int, int] of float: cf75;

array[int, int] of float: io;

array[int] of float: pImp;

array[INDEX_SET_pDom_1, INDEX_SET_pDom_2] of float: pDom = array2d(INDEX_SET_pDom_1, INDEX_SET_pDom_2, [if pR[c] > 0 then pR[c] else pPr[pl,c] endif | pl in plant, c in cRaw]);

array[int, int] of float: util;

float: utilPct = 0.85;

array[INDEX_SET_icap_1, INDEX_SET_icap_2] of float: icap = array2d(INDEX_SET_icap_1, INDEX_SET_icap_2, [0.33 * dcap[pl,u] | u in unit, pl in plant]);

array[INDEX_SET_tranFinal_1, INDEX_SET_tranFinal_2] of float: tranFinal = array2d(INDEX_SET_tranFinal_1, INDEX_SET_tranFinal_2, [if road[r,pl] > 0 then 0.5 + 0.0144 * road[r,pl] else 0 endif | pl in plant, r in region]);

array[INDEX_SET_tranImport_1, INDEX_SET_tranImport_2] of float: tranImport = array2d(INDEX_SET_tranImport_1, INDEX_SET_tranImport_2, [if road[r,po] > 0 then 0.5 + 0.0144 * road[r,po] else 0 endif | r in region, po in port]);

array[INDEX_SET_tranInter_1, INDEX_SET_tranInter_2] of float: tranInter = array2d(INDEX_SET_tranInter_1, INDEX_SET_tranInter_2, [if rail[p1,p2] > 0 then 3.5 + 0.03 * rail[p1,p2] else 0 endif | p1,p2 in plant]);

array[INDEX_SET_tranRaw_1] of float: tranRaw = array1d(INDEX_SET_tranRaw_1, [(if impdBarg[pl] > 0 then 1.0 + 0.0030 * impdBarg[pl] else 0 endif) + (if impdRoad[pl] > 0 then 0.5 + 0.0144 * impdRoad[pl] else 0 endif) | pl in plant]);

float: exch = 0.4;

array[int, int] of float: road;

array[int, int] of float: railHalf;

array[INDEX_SET_rail_1, INDEX_SET_rail_2] of float: rail = array2d(INDEX_SET_rail_1, INDEX_SET_rail_2, [if railHalf[p1,p2] > 0 then railHalf[p1,p2] else railHalf[p2,p1] endif | p1,p2 in plant]);

array[int] of float: impdBarg;

array[int] of float: impdRoad;

array[int] of float: pR;

array[int, int] of float: pPr;

array[int, int] of float: dcap;


var float: Psip;

var float: Psil;

var float: Psii;

array[INDEX_SET_Xf_1, INDEX_SET_Xf_2, INDEX_SET_Xf_3] of var float: Xf;

array[INDEX_SET_Vf_1, INDEX_SET_Vf_2, INDEX_SET_Vf_3] of var float: Vf;

array[INDEX_SET_Z_1, INDEX_SET_Z_2] of var float: Z;

array[INDEX_SET_Xi_1, INDEX_SET_Xi_2, INDEX_SET_Xi_3] of var float: Xi;

array[INDEX_SET_Vr_1, INDEX_SET_Vr_2] of var float: Vr;

array[INDEX_SET_U_1, INDEX_SET_U_2] of var float: U;

set of int: INDEX_SET_U_1;

set of int: INDEX_SET_U_2;

set of int: INDEX_SET_Vf_1;

set of int: INDEX_SET_Vf_2;

set of int: INDEX_SET_Vf_3;

set of int: INDEX_SET_Vr_1;

set of int: INDEX_SET_Vr_2;

set of int: INDEX_SET_Xf_1;

set of int: INDEX_SET_Xf_2;

set of int: INDEX_SET_Xf_3;

set of int: INDEX_SET_Xi_1;

set of int: INDEX_SET_Xi_2;

set of int: INDEX_SET_Xi_3;

set of int: INDEX_SET_Z_1;

set of int: INDEX_SET_Z_2;

set of int: INDEX_SET_cPos_1;

set of int: INDEX_SET_ccPos;

set of int: INDEX_SET_cn75_1;

set of int: INDEX_SET_cn75_2;

set of int: INDEX_SET_cpPos;

set of int: INDEX_SET_cpPosc_union_ccPosc;

set of int: INDEX_SET_icap_1;

set of int: INDEX_SET_icap_2;

set of int: INDEX_SET_mPos;

set of int: INDEX_SET_pCappl_diff_pExceptpl;

set of int: INDEX_SET_pDom_1;

set of int: INDEX_SET_pDom_2;

set of int: INDEX_SET_pPos_1;

set of int: INDEX_SET_rail_1;

set of int: INDEX_SET_rail_2;

set of int: INDEX_SET_tranFinal_1;

set of int: INDEX_SET_tranFinal_2;

set of int: INDEX_SET_tranImport_1;

set of int: INDEX_SET_tranImport_2;

set of int: INDEX_SET_tranInter_1;

set of int: INDEX_SET_tranInter_2;

set of int: INDEX_SET_tranRaw_1;

array[INDEX_SET_cpPosc_union_ccPosc] of int: cpPosc_union_ccPosc;

array[INDEX_SET_pCappl_diff_pExceptpl] of int: pCappl_diff_pExceptpl;


constraint forall(c in cFinal, pl in cpPos[c], r in region)(Xf[c,pl,r] >= 0);

constraint forall(c in cFinal, r in region, po in port)(Vf[c,r,po] >= 0);

constraint forall(pl in plant, pr in pPos[pl])(Z[pl,pr] >= 0);

constraint forall(c in cShip, p1 in cpPos[c], p2 in ccPos[c])(Xi[c,p1,p2] >= 0);

constraint forall(c in cRaw, pl in ccPos[c])(Vr[c,pl] >= 0);

constraint forall(c in cRaw, pl in ccPos[c])(U[c,pl] >= 0);

constraint forall(n in nutr, r in region)(sum(c in cFinal)(fn[c,n] * (sum(po in port)(Vf[c,r,po] + sum(pl in cpPos[c])(Xf[c,pl,r])))) >= cn75[r,n]);

constraint forall(c in cFinal, r in region where cf75[r,c] > 0)(sum(po in port)(Vf[c,r,po] + sum(pl in cpPos[c])(Xf[c,pl,r])) >= cf75[r,c]);

constraint forall(c in commod, pl in plant)(sum(pr in pPos[pl])(io[c,pr] * Z[pl,pr] + (if c in cShip then (if pl in cpPos[c] then sum(p2 in ccPos[c])(Xi[c,pl,p2]) else 0 endif) - (if pl in ccPos[c] then sum(p2 in cpPos[c])(Xi[c,p2,pl]) else 0 endif) else 0 endif) + (if c in cRaw /\ pl in ccPos[c] then ((if pImp[c] > 0 then Vr[c,pl] else 0 endif) + (if pDom[pl,c] > 0 then U[c,pl] else 0 endif)) else 0 endif)) >= if c in cFinal /\ pl in cpPos[c] then sum(r in region)(Xf[c,pl,r]) else 0 endif);

constraint forall(pl in plant, u in mPos[pl])(sum(pr in pPos[pl])(util[u,pr] * Z[pl,pr]) <= utilPct * icap[u,pl]);

constraint Psip = sum(c in cRaw, pl in ccPos[c])(pDom[pl,c] * U[c,pl]);

constraint Psil = sum(c in cFinal)((sum(pl in cpPos[c], r in region)(tranFinal[pl,r] * Xf[c,pl,r] + sum(po in port, r in region)(tranImport[r,po] * Vf[c,r,po]))) + sum(c in cShip, p1 in cpPos[c], p2 in ccPos[c])(tranInter[p1,p2] * Xi[c,p1,p2] + sum(c in cRaw, pl in ccPos[c] where pImp[c] > 0)(tranRaw[pl] * Vr[c,pl])));

constraint Psii / exch = sum(c in cFinal, r in region, po in port)(pImp[c] * Vf[c,r,po] + sum(c in cRaw, pl in ccPos[c])(pImp[c] * Vr[c,pl]));



solve minimize Psip + Psil + Psii;




