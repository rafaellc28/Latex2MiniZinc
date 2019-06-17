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

array[cFinal, nutr] of float: Fn;

array[region, nutr] of float: Cn75;

array[region, cFinal] of float: Cf75;

array[commod, proc] of float: Io;

array[commod] of float: PImp;

array[plant, cRaw] of float: PDom;

array[unit, proc] of float: Util;

float: UtilPct;

array[unit, plant] of float: Icap;

array[plant, region] of float: TranFinal;

array[region, port] of float: TranImport;

array[plant, plant] of float: TranInter;

array[plant] of float: TranRaw;

float: Exch;


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

set of int: INDEX_SET_ccPos;

set of int: INDEX_SET_cpPos;

set of int: INDEX_SET_mPos;

set of int: INDEX_SET_pPos;


constraint forall(c in cFinal, pl in INDEX_SET_Xf_2, r in region)(Xf[c,pl,r] >= 0);

constraint forall(c in cFinal, r in region, po in port)(Vf[c,r,po] >= 0);

constraint forall(pl in plant, pr in INDEX_SET_Z_2)(Z[pl,pr] >= 0);

constraint forall(c in cShip, p1 in INDEX_SET_Xi_2, p2 in INDEX_SET_Xi_3)(Xi[c,p1,p2] >= 0);

constraint forall(c in cRaw, pl in INDEX_SET_Vr_2)(Vr[c,pl] >= 0);

constraint forall(c in cRaw, pl in INDEX_SET_U_2)(U[c,pl] >= 0);

constraint forall(n in nutr, r in region)(sum(c in cFinal)(Fn[to_enum(cFinal,c),n] * (sum(po in port)(Vf[to_enum(cFinal,c),r,po] + sum(pl in cpPos[c])(Xf[to_enum(cFinal,c),pl,r])))) >= Cn75[r,n]);

constraint forall(c in cFinal, r in region where Cf75[r,to_enum(cFinal,c)] > 0)(sum(po in port)(Vf[to_enum(cFinal,c),r,po] + sum(pl in cpPos[c])(Xf[to_enum(cFinal,c),pl,r])) >= Cf75[r,to_enum(cFinal,c)]);

constraint forall(c in commod, pl in plant)(sum(pr in pPos[pl])(Io[c,to_enum(proc,pr)] * Z[pl,pr] + (if c in cShip then (if pl in cpPos[c] then sum(p2 in ccPos[c])(Xi[to_enum(cShip,c),pl,p2]) else 0 endif) - (if pl in ccPos[c] then sum(p2 in cpPos[c])(Xi[to_enum(cShip,c),p2,pl]) else 0 endif) else 0 endif) + (if c in cRaw /\ pl in ccPos[c] then ((if PImp[c] > 0 then Vr[to_enum(cRaw,c),pl] else 0 endif) + (if PDom[pl,to_enum(cRaw,c)] > 0 then U[to_enum(cRaw,c),pl] else 0 endif)) else 0 endif)) >= if c in cFinal /\ pl in cpPos[c] then sum(r in region)(Xf[to_enum(cFinal,c),pl,r]) else 0 endif);

constraint forall(pl in plant, u in mPos[pl])(sum(pr in pPos[pl])(Util[to_enum(unit,u),to_enum(proc,pr)] * Z[pl,pr]) <= UtilPct * Icap[to_enum(unit,u),pl]);

constraint Psip = sum(c in cRaw, pl in ccPos[c])(PDom[to_enum(plant,pl),c] * U[c,pl]);

constraint Psil = sum(c in cFinal)((sum(pl in cpPos[c], r in region)(TranFinal[to_enum(plant,pl),r] * Xf[to_enum(cFinal,c),pl,r] + sum(po in port, r in region)(TranImport[r,po] * Vf[to_enum(cFinal,c),r,po]))) + sum(c in cShip, p1 in cpPos[c], p2 in ccPos[c])(TranInter[to_enum(plant,p1),to_enum(plant,p2)] * Xi[c,p1,p2] + sum(c in cRaw, pl in ccPos[c] where PImp[to_enum(commod,c)] > 0)(TranRaw[to_enum(plant,pl)] * Vr[c,pl])));

constraint Psii / Exch = sum(c in cFinal, r in region, po in port)(PImp[to_enum(commod,c)] * Vf[to_enum(cFinal,c),r,po] + sum(c in cRaw, pl in ccPos[c])(PImp[to_enum(commod,c)] * Vr[c,pl]));

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




