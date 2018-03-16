enum cFinal;

enum port;

array[INDEX_SET_cpPos] of set of int: cpPos;

enum nutr;

enum region;

array[INDEX_SET_pPos] of set of int: pPos;

enum cShip;

array[INDEX_SET_ccPos] of set of int: ccPos;

enum cRaw;

enum commod;

enum plant;

array[INDEX_SET_mPos] of set of int: mPos;

enum unit;

enum proc;

array[int, int] of float: Fn;

array[int, int] of float: Cn75;

array[int, int] of float: Cf75;

array[int, int] of float: Io;

array[int] of float: PImp;

array[int, int] of float: PDom;

array[int, int] of float: Util;

float: UtilPct;

array[int, int] of float: Icap;

array[int, int] of float: TranFinal;

array[int, int] of float: TranImport;

array[int, int] of float: TranInter;

array[int] of float: TranRaw;

float: Exch;


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

set of int: INDEX_SET_ccPos;

set of int: INDEX_SET_cpPos;

set of int: INDEX_SET_mPos;

set of int: INDEX_SET_pPos;


constraint forall(c in cFinal, pl in cpPos[c], r in region)(Xf[c,pl,r] >= 0);

constraint forall(c in cFinal, r in region, po in port)(Vf[c,r,po] >= 0);

constraint forall(pl in plant, pr in pPos[pl])(Z[pl,pr] >= 0);

constraint forall(c in cShip, p1 in cpPos[c], p2 in ccPos[c])(Xi[c,p1,p2] >= 0);

constraint forall(c in cRaw, pl in ccPos[c])(Vr[c,pl] >= 0);

constraint forall(c in cRaw, pl in ccPos[c])(U[c,pl] >= 0);

constraint forall(n in nutr, r in region)(sum(c in cFinal)(Fn[c,n] * (sum(po in port)(Vf[c,r,po] + sum(pl in cpPos[c])(Xf[c,pl,r])))) >= Cn75[r,n]);

constraint forall(c in cFinal, r in region where Cf75[r,c] > 0)(sum(po in port)(Vf[c,r,po] + sum(pl in cpPos[c])(Xf[c,pl,r])) >= Cf75[r,c]);

constraint forall(c in commod, pl in plant)(sum(pr in pPos[pl])(Io[c,pr] * Z[pl,pr] + (if c in cShip then (if pl in cpPos[c] then sum(p2 in ccPos[c])(Xi[c,pl,p2]) else 0 endif) - (if pl in ccPos[c] then sum(p2 in cpPos[c])(Xi[c,p2,pl]) else 0 endif) else 0 endif) + (if c in cRaw /\ pl in ccPos[c] then ((if PImp[c] > 0 then Vr[c,pl] else 0 endif) + (if PDom[pl,c] > 0 then U[c,pl] else 0 endif)) else 0 endif)) >= if c in cFinal /\ pl in cpPos[c] then sum(r in region)(Xf[c,pl,r]) else 0 endif);

constraint forall(pl in plant, u in mPos[pl])(sum(pr in pPos[pl])(Util[u,pr] * Z[pl,pr]) <= UtilPct * Icap[u,pl]);

constraint Psip = sum(c in cRaw, pl in ccPos[c])(PDom[pl,c] * U[c,pl]);

constraint Psil = sum(c in cFinal)((sum(pl in cpPos[c], r in region)(TranFinal[pl,r] * Xf[c,pl,r] + sum(po in port, r in region)(TranImport[r,po] * Vf[c,r,po]))) + sum(c in cShip, p1 in cpPos[c], p2 in ccPos[c])(TranInter[p1,p2] * Xi[c,p1,p2] + sum(c in cRaw, pl in ccPos[c] where PImp[c] > 0)(TranRaw[pl] * Vr[c,pl])));

constraint Psii / Exch = sum(c in cFinal, r in region, po in port)(PImp[c] * Vf[c,r,po] + sum(c in cRaw, pl in ccPos[c])(PImp[c] * Vr[c,pl]));

constraint forall(pl in plant)(TranRaw[pl] >= 0);

constraint forall(p1 in plant, p2 in plant)(TranInter[p1,p2] >= 0);

constraint forall(pl in plant, r in region)(TranFinal[pl,r] >= 0);

constraint forall(u in unit, p in proc)(Util[u,p] >= 0);

constraint forall(c in commod, p in proc)(Io[c,p] <= 1);

constraint forall(u in unit, pl in plant)(Icap[u,pl] >= 0);

constraint forall(pl in plant, r in cRaw)(PDom[pl,r] >= 0);

constraint forall(c in commod)(PImp[c] >= 0);

constraint forall(c in commod)(sum(pl in cpPos[c])(1) >= 0);

constraint forall(c in commod)(sum(pl in ccPos[c])(1) >= 0);



solve minimize Psip + Psil + Psii;




