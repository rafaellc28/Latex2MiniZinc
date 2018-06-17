set of int: c_final;

enum port;

set of int: plant;

array[INDEX_SET_cp_pos, 1..2] of plant: cp_pos;

enum nutr;

enum region;

set of int: proc;

array[INDEX_SET_p_pos, 1..2] of int: p_pos = p_cap_diff_p_except;

enum c_ship;

array[INDEX_SET_cc_pos, 1..2] of c_final: cc_pos;

set of int: c_raw;

set of int: commod = c_final union c_inter union c_raw;

array[INDEX_SET_m_pos, 1..2] of int: m_pos;

enum center;

set of int: c_inter;

set of int: p_except;

set of int: p_cap;

enum unit;

array[int, int] of float: fn;

array[INDEX_SET_cn75_1, INDEX_SET_cn75_2] of float: cn75 = array2d(INDEX_SET_cn75_1, INDEX_SET_cn75_2, [sum(c in c_final)(cf75[r,c] * fn[c,n]) | r in region, n in nutr]);

array[int, int] of float: cf75;

array[int, int] of float: io;

array[int] of float: p_imp;

array[INDEX_SET_p_dom_1, INDEX_SET_p_dom_2] of float: p_dom = array2d(INDEX_SET_p_dom_1, INDEX_SET_p_dom_2, [if p_r[c] > 0 then p_r[c] else p_pr[pl,c] endif | pl in plant, c in c_raw]);

array[int, int] of float: util;

float: util_pct = 0.85;

array[INDEX_SET_icap_1, INDEX_SET_icap_2] of float: icap = array2d(INDEX_SET_icap_1, INDEX_SET_icap_2, [0.33 * dcap[pl,u] | u in unit, pl in plant]);

array[INDEX_SET_tran_final_1, INDEX_SET_tran_final_2] of float: tran_final = array2d(INDEX_SET_tran_final_1, INDEX_SET_tran_final_2, [if road[r,pl] > 0 then (0.5 + 0.0144 * road[r,pl]) else 0 endif | pl in plant, r in region]);

array[INDEX_SET_tran_import_1, INDEX_SET_tran_import_2] of float: tran_import = array2d(INDEX_SET_tran_import_1, INDEX_SET_tran_import_2, [if road[r,po] > 0 then (0.5 + 0.0144 * road[r,po]) else 0 endif | r in region, po in port]);

array[INDEX_SET_tran_inter_1, INDEX_SET_tran_inter_2] of float: tran_inter = array2d(INDEX_SET_tran_inter_1, INDEX_SET_tran_inter_2, [if rail[p1,p2] > 0 then (3.5 + 0.03 * rail[p1,p2]) else 0 endif | p1 in plant, p2 in plant]);

array[INDEX_SET_tran_raw_1] of float: tran_raw = array1d(INDEX_SET_tran_raw_1, [(if impd_barg[pl] > 0 then (1.0 + 0.0030 * impd_barg[pl]) else 0 endif) + (if impd_road[pl] > 0 then (0.5 + 0.0144 * impd_road[pl]) else 0 endif) | pl in plant]);

float: exch = 0.4;

array[int, int] of float: road;

array[int] of float: impd_barg;

array[int] of float: impd_road;

array[int, int] of float: rail_half;

array[int] of float: p_r;

array[int, int] of float: p_pr;

array[int, int] of float: dcap;

array[INDEX_SET_rail_1, INDEX_SET_rail_2] of float: rail = array2d(INDEX_SET_rail_1, INDEX_SET_rail_2, [rail_half[p1,p2] + rail_half[p2,p1] | p1 in plant, p2 in plant]);


array[INDEX_SET_Z_1, INDEX_SET_Z_2] of var float: Z;

array[INDEX_SET_Xf_1, INDEX_SET_Xf_2, INDEX_SET_Xf_3] of var float: Xf;

array[INDEX_SET_Xi_1, INDEX_SET_Xi_2, INDEX_SET_Xi_3] of var float: Xi;

array[INDEX_SET_Vf_1, INDEX_SET_Vf_2, INDEX_SET_Vf_3] of var float: Vf;

array[INDEX_SET_Vr_1, INDEX_SET_Vr_2] of var float: Vr;

array[INDEX_SET_U_1, INDEX_SET_U_2] of var float: U;

var float: Psip;

var float: Psil;

var float: Psii;

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

set of int: INDEX_SET_cc_pos;

set of int: INDEX_SET_cn75_1;

set of int: INDEX_SET_cn75_2;

set of int: INDEX_SET_cp_pos;

set of int: INDEX_SET_icap_1;

set of int: INDEX_SET_icap_2;

set of int: INDEX_SET_m_pos;

set of int: INDEX_SET_p_cap_diff_p_except;

set of int: INDEX_SET_p_dom_1;

set of int: INDEX_SET_p_dom_2;

set of int: INDEX_SET_p_pos;

set of int: INDEX_SET_rail_1;

set of int: INDEX_SET_rail_2;

set of int: INDEX_SET_tran_final_1;

set of int: INDEX_SET_tran_final_2;

set of int: INDEX_SET_tran_import_1;

set of int: INDEX_SET_tran_import_2;

set of int: INDEX_SET_tran_inter_1;

set of int: INDEX_SET_tran_inter_2;

set of int: INDEX_SET_tran_raw_1;

array[INDEX_SET_p_cap_diff_p_except] of int: p_cap_diff_p_except;


constraint forall(pr in proc, pl in plant)(Z[pr,pl] >= 0);

constraint forall(c in INDEX_SET_cp_pos, r in region)(Xf[cp_pos[c,1],r,r] >= 0);

constraint forall(c in INDEX_SET_cp_pos, p2 in plant)(Xi[cp_pos[c,1],p2,p2] >= 0);

constraint forall(cf in c_final, r in region, p in port)(Vf[cf,r,p] >= 0);

constraint forall(c in INDEX_SET_cc_pos)(Vr[cc_pos[c,1],cc_pos[c,2]] >= 0);

constraint forall(c in INDEX_SET_cc_pos)(U[cc_pos[c,1],cc_pos[c,2]] >= 0);

constraint forall(n in nutr, r in region)(sum(c in c_final)(fn[c,n] * (sum(po in port)(Vf[c,r,po] + sum(pl in plant where c in INDEX_SET_cp_pos)(Xf[c,pl,r])))) >= cn75[r,n]);

constraint forall(c in c_final, r in region where cf75[r,c] > 0)(sum(po in port)(Vf[c,r,po] + sum(pl in plant where c in INDEX_SET_cp_pos)(Xf[c,pl,r])) >= cf75[r,c]);

constraint forall(c in commod, pl in plant)(sum(pr in proc where pr in INDEX_SET_p_pos)(io[c,pr] * Z[pr,pl] + (if (c in c_ship) then sum(p2 in plant)(((if c in INDEX_SET_cp_pos /\ c in INDEX_SET_cc_pos then Xi[c,p2,pl] else 0 endif) - (if c in INDEX_SET_cc_pos /\ c in INDEX_SET_cp_pos then Xi[c,pl,p2] else 0 endif))) else 0 endif) + (if (c in c_raw /\ c in INDEX_SET_cc_pos) then ((if p_imp[c] > 0 then Vr[c,pl] else 0 endif) + (if p_dom[pl,c] > 0 then U[c,pl] else 0 endif)) else 0 endif)) >= if (c in c_final /\ c in INDEX_SET_cp_pos) then sum(r in region)(Xf[c,pl,r]) else 0 endif);

constraint forall(u in INDEX_SET_m_pos)(sum(pr in proc where pr in INDEX_SET_p_pos)(util[m_pos[u,1],pr] * Z[pr,m_pos[u,2]]) <= util_pct * icap[m_pos[u,1],m_pos[u,2]]);

constraint Psip = sum(c in INDEX_SET_cc_pos where cc_pos[c,1] in c_raw)(p_dom[cc_pos[c,2],cc_pos[c,1]] * U[cc_pos[c,1],cc_pos[c,2]]);

constraint Psil = sum(c in c_final)((sum(pl in plant, r in region where c in INDEX_SET_cp_pos)(tran_final[pl,r] * Xf[c,pl,r] + sum(po in port, r in region)(tran_import[r,po] * Vf[c,r,po]))) + sum(c in c_ship, p1 in plant, p2 in plant where c in INDEX_SET_cp_pos /\ c in INDEX_SET_cc_pos)(tran_inter[p1,p2] * Xi[c,p1,p2] + sum(c in c_raw, pl in plant where c in INDEX_SET_cc_pos /\ p_imp[c] > 0)(tran_raw[pl] * Vr[c,pl])));

constraint Psii/exch = sum(c in c_final, r in region, po in port)(p_imp[c] * Vf[c,r,po] + sum(c in c_raw, pl in plant where c in INDEX_SET_cc_pos)(p_imp[c] * Vr[c,pl]));



solve minimize Psip + Psil + Psii;




